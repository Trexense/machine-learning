from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import psycopg2
from psycopg2 import sql
import base64
import json
import tempfile
import vertexai

load_dotenv()

project_id = os.getenv("PROJECT_ID")
location = os.getenv("LOCATION")

service_acc_string = os.getenv("GCP_SERVICE_ACCOUNT_KEY")
service_acc_decoded = base64.b64decode(service_acc_string).decode('utf-8')
service_acc_json = json.loads(service_acc_decoded)
service_acc_json = json.dumps(service_acc_json)

with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
    temp_file.write(service_acc_json)
    temp_file_path = temp_file.name

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = temp_file_path

vertexai.init(project=project_id, location='asia-southeast2')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")


# DB_HOST = os.getenv("DB_HOST")
# DB_NAME = os.getenv("DB_NAME")
# DB_USER = os.getenv("DB_USER")
# DB_PASSWORD = os.getenv("DB_PASSWORD")

# def get_db_connection():
#     return psycopg2.connect(
#         host=DB_HOST,
#         database=DB_NAME,
#         user=DB_USER,
#         password=DB_PASSWORD
#     )

try:
    # Setup Postgres
    db = SQLAlchemy(app)
    # conn = get_db_connection()
    print("Connected to Postgresql")
except Exception as e:
    print("Error connecting to Postgresql:", e)

from application import routes
