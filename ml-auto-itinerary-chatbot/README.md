# Machine Learning: Vertex AI based Auto-Itinerary Chatbot

## Overview

This Project utilizes Gemini on Vertex AI to build an AI Agent that serves as a chatbot in our application, Trexense. This system uses a Retrieval Augmented Generation (RAG) approach to provide relevant and accurate responses by combining information retrieval with advanced generative capabilities.

## Tech Stack
- Gemini on Vertex AI
- Langchain
- Flask
- ChromaDB


## Getting Started

This code serve as Flask Backend, to using this code, we need to run the flask server.

Below code is for Linux Environment

1. Clone The Repository

   ```
   git clone https://github.com/Trexense/machine-learning
   cd machine-learning
   cd ml-auto-itinerary-chatbot
   ```
2. Create .env file

   .env file consists of this variable

   ```
   GCP_SERVICE_ACCOUNT_KEY = "YOUR-GCP-SERVICE-ACC-KEY"
   PROJECT_ID = "YOUR-PROJECT-ID"
   LOCATION = 'YOUR-LOCATION'

   ```
3. Create Virtual Environment and Install Requirements

   ```
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
4. Run The Server

   ```
   python3 server.py
   ```

## Using The App

Simply do HTTP request to the endpoint. The simplest way is using below curl command

```
curl -X POST http://127.0.0.1:8080/generate -H "Content-Type: application/json" -d '{"prompt": "Your Prompt"}

# Example
curl -X POST http://127.0.0.1:8080/generate -H "Content-Type: application/json" -d '{"prompt": "What is the entrance price for Ubud Bali?"}'
```

## Project Structure

```

ML-AUTO-ITINERARY-CHATBOT/               # Code to run the serverdata-science-project/
│
├── README.md                   	 # Project overview and instructions
├── requirements.txt            	 # Python package dependencies
├── .env		        	 # environment variable file
├── .env.example	        	 # template of environment variable
├── .gitignore                  	 # Git ignore file for unnecessary files
│
├── chroma/                      	 # Vector Database for Retrieval Process
│
├── data/                       	 # Data that used as knowledge for RAG
│   ├── Bali_hotel.md                    # Bali hotel dataset
│   └── Bali_Tourism_2022.md             # Bali travel destination dataset 

├── dataset-raw/                       	 # Raw Dataset
│   └── data.csv                         # CSV dataset of bali travel destination
│
├── notebooks/                  	 # Jupyter notebooks (experimentation and analysis)
│    └──  01_data_preparation.ipynb	 # Code for turn csv data into text data
│
└── run.py                      	 # Code to run the server


```
