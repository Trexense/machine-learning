from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")
genai.configure(api_key= os.getenv("GEMINI_API_KEY"))

try:
    # Setup MongoDB
    db = SQLAlchemy(app)
    print("Connected to Postgresql")
except Exception as e:
    print("Error connecting to Postgresql:", e)

from application import routes