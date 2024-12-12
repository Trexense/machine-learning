# Machine Learning Deployment

## Overview

This project serves as a **Model-as-a-Service (MaaS)** backend platform, integrating both a **hotel recommendation system** and an **auto-itinerary chatbot** within a Flask application.

## Tech Stack

- Gemini on Vertex AI
- Langchain
- Flask
- ChromaDB
- Tensorflow
- Pandas
- Docker

## Getting Started

This code serve as Flask Backend, to using this code, we need to run the flask server.

Below code is for Linux Environment

1. Clone The Repository

   ```

   git clone https://github.com/Trexense/machine-learning

   cd machine-learning

   cd ml-server

   ```
2. Create .env file

   .env file consists of this variable

   ```
   SQLALCHEMY_DATABASE_URI = "YOUR-SQLALCHEMY-DATABASE-URI"
   GCP_SERVICE_ACCOUNT_KEY = "YOUR-GCP-SERVICE-ACCOUNT-KEY"
   PROJECT_ID = "YOUR-PROJECT-ID"
   LOCATION = '-YOUR-LOCATION'
   ```
3. Create Virtual Environment and Install Requirements

   ```

   python3 -m venv .venv

   source .venv/bin/activate

   pip install -r requirements.txt

   ```
4. Run The Server

   ```

   python3 run.py

   ```

## API Endpoint

### **Hotel Recommendation Endpoints**

| **Method** | **Endpoint**                                  | **Description**                                  |
| ---------------- | --------------------------------------------------- | ------------------------------------------------------ |
| `GET`          | `/recommend-hotel/{userid}`                       | Get all hotel recommendations based on user activity.  |
| `GET`          | `/recommend-hotel/`{`userid`}`/`{`top_n`}`` | Get top_n hotel recommendations based on user activity |

### **Auto Itinerary Chatbot Endpoints**

| **Method** | **Endpoint** | **Description**                        |
| ---------------- | ------------------ | -------------------------------------------- |
| `POST`         | `/generate`      | Generate an itinerary based on user queries. |

## Project Structure

```
ML-AUTO-ITINERARY-CHATBOT/               # Code to run the ml-server/
│
├── README.md                   	 # Project overview and instructions
├── requirements.txt            	 # Python package dependencies
├── .env		        	 # environment variable file
├── .env.example	        	 # template of environment variable
├── .gitignore                  	 # Git ignore file for unnecessary files
├── Dockerfile				 # Docker Configuration
│
├── application/                      	 # Directory of application code
│   ├── __init__.py	                 # Flask and API setup
│   ├── models.py	                 # Models for querying from database
│   └── routes.py            		 # API endpoint routing
│
├── chroma/                      	 # Vector Database for Retrieval Process
│
├── utils/                  	 	 # Function utils
│    └──  generate_user_score.py	 # Code for generate user score based on user activities
│
└── run.py                      	 # Code to run the server
```
