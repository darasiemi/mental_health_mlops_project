import json
import os
import json
import boto3
import base64

import mlflow

import pickle

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import nltk
import re
import sys

# Download the stopwords resource
nltk.download('stopwords')

stemmer = nltk.SnowballStemmer("english")

# from textblob import TextBlob
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_selection import mutual_info_classif
from sklearn.preprocessing import StandardScaler
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from nltk.corpus import stopwords
stopwords = stopwords.words('english')
# import string

import matplotlib.pyplot as plt


from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import warnings
warnings.filterwarnings("ignore")

import string
#Get a list of punctuations
punct = []
for char in string.punctuation:
    punct.append(char)

from mlflow.tracking import MlflowClient
import os
from io import BytesIO

import tracemalloc
tracemalloc.start()


kinesis_client = boto3.client('kinesis')

PREDICTIONS_STREAM_NAME = os.getenv('PREDICTIONS_STREAM_NAME', 'stress_predictions')

RUN_ID = os.getenv('RUN_ID',"57342ae687254eeeac28602bb8d42aca")
# RUN_ID = '95182c88ec8040888af37b5f0259e733'

TEST_RUN = os.getenv('TEST_RUN', 'False') == 'True'

# logged_model = f's3://mlflows-artifacts-remote/1/{RUN_ID}/artifacts/model'
# # logged_model = f'runs:/{RUN_ID}/model'
# model = mlflow.pyfunc.load_model(logged_model)

s3_location = "mlflows-artifacts-remote"

def load_model_n_vect(RUN_ID):
    logged_model = f's3://{s3_location}/3/{RUN_ID}/artifacts/model'
    # logged_model = f'runs:/{RUN_ID}/model'
    model = mlflow.pyfunc.load_model(logged_model)

    # Initialize a session using Amazon S3
    s3 = boto3.client('s3', region_name='eu-north-1')

    # Define the S3 bucket and the file path
    # bucket_name = 'mlflows-artifacts-remote'
    key = f'3/{RUN_ID}/artifacts/vectorizer/vectorizer.b'

    # Download the file from S3 into memory
    response = s3.get_object(Bucket=s3_location, Key=key)
    file_content = response['Body'].read()

    # Load the vectorizer using pickle
    vect = pickle.load(BytesIO(file_content))

    print("model and vect loaded successfully")
    
    return model, vect

def process_numerical_features(df, numerical_columns, scaler):
    X_numerical = df[numerical_columns]
    X_numerical = scaler.fit_transform(X_numerical)
    return X_numerical
    

def removal(text):
    text = str(text).lower()
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('\w*\d\w*', '', text)
    text = [w for w in text.split(' ') if w not in stopwords]
    text=" ".join(text)
    text = [stemmer.stem(word) for word in text.split(' ')]
    text=" ".join(text)
    return text

def process_categorical_features(df, vect = None):
    posts = df[["text"]]
    posts["text"] = posts["text"].apply(removal)
    # posts = posts["text"].apply(removal)
    X = posts["text"]
    if vect:
        X = vect.transform(X)
    else:
        vect=CountVectorizer(stop_words="english")
        X=vect.fit_transform(X)
    return X, vect
    
def prepare_features(df, vect=None):
    numerical_columns = ["lex_liwc_Tone", "lex_liwc_i", "lex_liwc_negemo", "lex_liwc_Clout", "sentiment"]
    scaler = StandardScaler()
    
    X_categorical, vect = process_categorical_features(df, vect)
    X_numerical = process_numerical_features(df,numerical_columns, scaler)
    X_features = np.hstack((X_categorical.toarray(), X_numerical))

    return X_features

def predict(features):
    preds = model.predict(features)
    return int(preds[0])

model, vect = load_model_n_vect(RUN_ID)


def lambda_handler(event, context):    
    predictions_events = []
    predictions = []
    
    for record in event['Records']:
        encoded_data = record['kinesis']['data']
        decoded_data = base64.b64decode(encoded_data).decode('utf-8')
        # print(decoded_data)
        
        stress_event = json.loads(decoded_data)
        stress_event  = pd.DataFrame([stress_event])
        # print(stress_event)
    
        features = prepare_features(stress_event, vect)
        prediction = predict(features)
        predictions.append({
            'stress_prediction': prediction })
        
        prediction_event = {
            'model': 'stress_prediction_model',
            'version': '123',
            'prediction': {
                'stress_prediction': prediction,  
            }
        }

        if not TEST_RUN:
            kinesis_client.put_record(
                StreamName=PREDICTIONS_STREAM_NAME,
                Data=json.dumps(prediction_event)
                # PartitionKey=str(ride_id)
            )
            
        predictions_events.append(prediction_event)
   
    return {
        'predictions': predictions_events
    }
