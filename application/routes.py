from application import app
from application import db
from flask import Flask, jsonify, request
# from dataclasses import dataclass
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

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
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

        results = db.similarity_search_with_relevance_scores(query_text, k=5)
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