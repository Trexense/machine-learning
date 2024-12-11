from application import app
from application.models import db, UserHotelClick, UserHotelBookmark, Hotel
from utils import generate_user_score
from flask import Flask, jsonify, request
# from dataclasses import dataclass
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql
import pandas as pd
import numpy as np
import tensorflow as tf

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

Do not Generate Any ID (ID: xxxxx) provided to you into the answer expect there are explicit instruction to do so

---

Answer the question based on the above context: {question}
"""

@app.route('/generate', methods=['POST'])
def generate_text():
    data = request.get_json()

    if 'prompt' not in data:
        return jsonify({"error": "No prompt provided"}), 400

    query_text = data['prompt']

    try:
        embedding_function = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        chroma_db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

        results = chroma_db.similarity_search_with_relevance_scores(query_text, k=5)
        if len(results) == 0 or results[0][1] < 0.1:
            print(f"Unable to find matching results.")
            return

        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=context_text, question=query_text)

        model = genai.GenerativeModel("gemini-1.5-flash")
        #===
        response = model.generate_content(prompt)

        # Extract the text content
        response_text = response.candidates[0].content.parts[0].text

        return jsonify({"response": response_text}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route("/recommend-hotel/<userid>", methods = ["GET"])
def recommend_hotel(userid):
    if not userid:
        return jsonify({"error": "No userid provided"}), 400

    try:
        # Get Click Data
        user_click_data = UserHotelClick.query.filter_by(userId=userid).all()
        if not user_click_data:
            return jsonify({"error": "No data found for the given userid"}), 404
        user_click_data_list = [row.to_dict() for row in user_click_data]
        df_click = pd.DataFrame(user_click_data_list)
        # print(df_click.head(1))

        # Get Bookmark Data
        user_bookmark_data = UserHotelBookmark.query.filter_by(userId=userid).all()
        if not user_bookmark_data:
            return jsonify({"error": "No data found for the given userid"}), 404
        user_bookmark_data_list = [row.to_dict() for row in user_bookmark_data]
        df_bookmark = pd.DataFrame(user_bookmark_data_list)
        # print(df_bookmark.head(1))

        # Get Hotel Data
        hotel_data = Hotel.query.all()
        if not hotel_data:
            return jsonify({"error": "No data found for the given userid"}), 404
        hotel_data_list = [row.to_dict() for row in hotel_data]
        df_hotel = pd.DataFrame(hotel_data_list)
        # print(df_hotel.head(1))

        df_user = generate_user_score.generate_user_score(df_click, df_bookmark, df_hotel)


        user_vector = np.array(df_user).reshape(1, -1)
        print(user_vector.dtype)
        hotel_ids = df_hotel['hotelid'].to_numpy()
        print(hotel_ids.dtype)
        hotel_vectors = df_hotel.drop(['hotelid','name'],axis = 1).to_numpy()
        print(hotel_vectors.dtype)
        print(hotel_vectors)

        user_input = np.tile(user_vector, (hotel_vectors.shape[0], 1))

        # Combine inputs for prediction
        prediction_input = [hotel_vectors, user_input]

        # for item in prediction_input:
        #     print(type(item))

        # Predict scores
        model = tf.keras.models.load_model('static/model/model.h5')
        predicted_scores = model.predict(prediction_input).flatten()

        # Rank hotels by predicted scores
        recommendations = sorted(zip(hotel_ids, predicted_scores), key=lambda x: x[1], reverse=True)

        # Convert recommendations to a list of dictionaries, ensuring the scores are native Python float types
        recommendations_dict = [{"hotelid": hotel_id, "predicted_score": float(score)} for hotel_id, score in recommendations]

        # Print recommendations (optional for debugging)
        print(recommendations_dict)

        # Return recommendations as a JSON response
        return jsonify({"recommendation": recommendations_dict}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/recommend-hotel/<userid>/<top_n>", methods = ["GET"])
def recommend_top_n_hotel(userid, top_n):
    if not userid:
        return jsonify({"error": "No userid provided"}), 400

    try:
        # Get Click Data
        user_click_data = UserHotelClick.query.filter_by(userId=userid).all()
        if not user_click_data:
            return jsonify({"error": "No data found for the given userid"}), 404
        user_click_data_list = [row.to_dict() for row in user_click_data]
        df_click = pd.DataFrame(user_click_data_list)
        # print(df_click.head(1))

        # Get Bookmark Data
        user_bookmark_data = UserHotelBookmark.query.filter_by(userId=userid).all()
        if not user_bookmark_data:
            return jsonify({"error": "No data found for the given userid"}), 404
        user_bookmark_data_list = [row.to_dict() for row in user_bookmark_data]
        df_bookmark = pd.DataFrame(user_bookmark_data_list)
        # print(df_bookmark.head(1))

        # Get Hotel Data
        hotel_data = Hotel.query.all()
        if not hotel_data:
            return jsonify({"error": "No data found for the given userid"}), 404
        hotel_data_list = [row.to_dict() for row in hotel_data]
        df_hotel = pd.DataFrame(hotel_data_list)
        # print(df_hotel.head(1))

        df_user = generate_user_score.generate_user_score(df_click, df_bookmark, df_hotel)


        user_vector = np.array(df_user).reshape(1, -1)
        print(user_vector.dtype)
        hotel_ids = df_hotel['hotelid'].to_numpy()
        print(hotel_ids.dtype)
        hotel_vectors = df_hotel.drop(['hotelid','name'],axis = 1).to_numpy()
        print(hotel_vectors.dtype)
        print(hotel_vectors)

        user_input = np.tile(user_vector, (hotel_vectors.shape[0], 1))

        # Combine inputs for prediction
        prediction_input = [hotel_vectors, user_input]

        # for item in prediction_input:
        #     print(type(item))

        # Predict scores
        model = tf.keras.models.load_model('static/model/model.h5')
        predicted_scores = model.predict(prediction_input).flatten()

        # Rank hotels by predicted scores
        recommendations = sorted(zip(hotel_ids, predicted_scores), key=lambda x: x[1], reverse=True)

        #Take only top <top_n>
        recommendations = recommendations[:int(top_n)]

        # Convert recommendations to a list of dictionaries, ensuring the scores are native Python float types
        recommendations_dict = [{"hotelid": hotel_id, "predicted_score": float(score)} for hotel_id, score in recommendations]

        # Print recommendations (optional for debugging)
        print(recommendations_dict)

        # Return recommendations as a JSON response
        return jsonify({"recommendation": recommendations_dict}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/')
def test_api():
    return jsonify({"message":"Ikan, ikan apa yang bisa terbang? Lelelawar"})