from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_community.vectorstores import Chroma
from langchain_google_vertexai import VertexAIEmbeddings
import os
import shutil
# from oauth2client.client import GoogleCredentials
# import google.generativeai as genai
from dotenv import load_dotenv
import base64
import json
import tempfile
import vertexai

load_dotenv()

service_acc_string = os.getenv("GCP_SERVICE_ACCOUNT_KEY")
service_acc_decoded = base64.b64decode(service_acc_string).decode('utf-8')
service_acc_json = json.loads(service_acc_decoded)
service_acc_json = json.dumps(service_acc_json)

with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
    temp_file.write(service_acc_json)
    temp_file_path = temp_file.name

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = temp_file_path
# genai.configure(api_key=os.environ["GEMINI_API_KEY"])
project_id = os.getenv("PROJECT_ID")
location = os.getenv("LOCATION")

vertexai.init(project=project_id, location=location)

CHROMA_PATH = "chroma"
DATA_PATH = "data"

def main():
    generate_data_store()


def generate_data_store():
    documents = load_documents()
    chunks = split_text(documents)
    save_to_chroma(chunks)


def load_documents():
    loader = DirectoryLoader(DATA_PATH, glob="*.md")
    documents = loader.load()
    return documents


def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=300,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    document = chunks[10]
    print(document.page_content)
    print(document.metadata)

    return chunks


def save_to_chroma(chunks: list[Document]):
    # Clear out the database first.
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    # Create a new DB from the documents.
    db = Chroma.from_documents(
        chunks, VertexAIEmbeddings(model="text-embedding-004"), persist_directory=CHROMA_PATH
    )
    db.persist()
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")


if __name__ == "__main__":
    main()