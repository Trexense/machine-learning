from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import google.generativeai as genai
import psycopg2
from psycopg2 import sql

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")
genai.configure(api_key= os.getenv("GEMINI_API_KEY"))

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