# Machine Learning: Content Based Filtering Hotel Recommendation System

## Overview

This Project utilizes Tensorflow to build a recommendation system of Hotel in our product, Trexense. The model will recieve user activities on clicking and bookmarking hotel as input and outputs a ranked list of the most relevant hotel recommendations. By analyzing user interactions, the system aims to enhance personalized recommendations, improving user experience and engagement.

## Tech Stack

- Tensorflow
- Pandas

## Getting Started

This code is developed and tested on google colab environment. If you want to test the code, we are **highly suggested** you to do so in this [link](https://colab.research.google.com/drive/1DwCwkWqYzMNqxY6FaWCWxeQkZsBaFPJv?usp=sharing) .

However, if you want to try it locally, follow this code

Below code is for Linux Environment

1. Clone The Repository

   ```

   git clone https://github.com/Trexense/machine-learning

   cd machine-learning

   cd recommendation-system

   ```
2. Create Virtual Environment and Install Requirements

   ```

   python3 -m venv .venv

   source .venv/bin/activate

   pip install -r requirements.txt

   ```
3. Run The ipynb notebook

   ```

   python3 server.py

   ```

## Project Structure

```


recommendation-system/               		 # Code to run the recommendation-system/
│
├── requirements.txt             		 # Python package dependencies
├── data/                         		 # Data that used as knowledge for RAG
│   ├── list_hotel.csv                    	 # Bali hotel dataset
│   └── user_history_dummy_3000_1500.csv         # Bali travel destination dataset 
│
├── model/                           		 # Raw Dataset
│   └── model.h5		             	 # Bali travel destination dataset 
│
├── notebooks/                    		 # Jupyter notebooks (experimentation and analysis)
│    └──  recommendation-system-modeling.ipynb   # Code for turn csv data into text data
└── README.md                    		 # Project overview and instructions


```
