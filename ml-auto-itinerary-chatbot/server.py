from flask import Flask, jsonify, request
from langchain_chroma import Chroma
from langchain_google_vertexai import VertexAIEmbeddings
from langchain.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
import base64
import json
import vertexai
from vertexai.preview.generative_models import GenerativeModel
import tempfile

load_dotenv()

service_acc_string = os.getenv("GCP_SERVICE_ACCOUNT_KEY")
service_acc_decoded = base64.b64decode(service_acc_string).decode('utf-8')
service_acc_json = json.loads(service_acc_decoded)
service_acc_json = json.dumps(service_acc_json)

project_id = os.getenv("PROJECT_ID")
location = os.getenv("LOCATION")

with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
    temp_file.write(service_acc_json)
    temp_file_path = temp_file.name

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

Do not Generate Any ID (ID: xxxxx) provided to you into the answer expect there are explicit instruction to do so

---
=
Answer the question based on the above context: {question}
"""

app = Flask(__name__)

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = temp_file_path

vertexai.init(project=project_id, location=location)

@app.route('/generate', methods=['POST'])
def generate_text():
    data = request.get_json()

    if 'prompt' not in data:
        return jsonify({"error": "No prompt provided"}), 400

    query_text = data['prompt']

    try:
        embedding_function = VertexAIEmbeddings(model_name="text-embedding-004")
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

        results = db.similarity_search_with_relevance_scores(query_text, k=5)
        if len(results) == 0 or results[0][1] < 0.1:
            return jsonify({"error": "No relevant results found"}), 404

        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=context_text, question=query_text)
        print(prompt)
        
        model = GenerativeModel('gemini-pro')
        #===
        response = model.generate_content(prompt)

        # Extract the text content
        try:
            response_text = response.candidates[0].content.parts[0].text
        except (IndexError, AttributeError) as e:
            return jsonify({"error": "Failed to parse the model response"}), 500

        return jsonify({"response": response_text}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
