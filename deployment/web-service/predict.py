#!/usr/bin/env python
# pylint: disable=line-too-long
import os
import re
import pickle

import numpy as np
import pandas as pd

import nltk

import warnings

warnings.filterwarnings("ignore")

# Download the stopwords resource
nltk.download("stopwords")

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

stopwords = stopwords.words("english")
# import string

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

import string

# Get a list of punctuations
punct = []
for char in string.punctuation:
    punct.append(char)

import mlflow
from mlflow.tracking import MlflowClient
import boto3
import pickle
from io import BytesIO

from flask import Flask, request, jsonify

RUN_ID = os.getenv("RUN_ID", "57342ae687254eeeac28602bb8d42aca")
s3_location = "mlflows-artifacts-remote"


def load_model_n_vect(RUN_ID):
    logged_model = f"s3://{s3_location}/3/{RUN_ID}/artifacts/model"
    # logged_model = f'runs:/{RUN_ID}/model'
    model = mlflow.pyfunc.load_model(logged_model)

    # Initialize a session using Amazon S3
    s3 = boto3.client("s3", region_name="eu-north-1")

    # Define the S3 bucket and the file path
    # bucket_name = 'mlflows-artifacts-remote'
    key = f"3/{RUN_ID}/artifacts/vectorizer/vectorizer.b"

    # Download the file from S3 into memory
    response = s3.get_object(Bucket=s3_location, Key=key)
    file_content = response["Body"].read()

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
    text = re.sub("https?://\S+|www\.\S+", "", text)
    text = re.sub("<.*?>+", "", text)
    text = re.sub("\w*\d\w*", "", text)
    text = [w for w in text.split(" ") if w not in stopwords]
    text = " ".join(text)
    text = [stemmer.stem(word) for word in text.split(" ")]
    text = " ".join(text)
    return text


def process_categorical_features(df, vect=None):
    posts = df[["text"]]
    posts["text"] = posts["text"].apply(removal)
    X = posts["text"]
    if vect:
        X = vect.transform(X)
    else:
        vect = CountVectorizer(stop_words="english")
        X = vect.fit_transform(X)
    return X, vect


def prepare_features(df, vect=None):
    numerical_columns = [
        "lex_liwc_Tone",
        "lex_liwc_i",
        "lex_liwc_negemo",
        "lex_liwc_Clout",
        "sentiment",
    ]
    scaler = StandardScaler()

    X_categorical, vect = process_categorical_features(df, vect)
    X_numerical = process_numerical_features(df, numerical_columns, scaler)
    X_features = np.hstack((X_categorical.toarray(), X_numerical))

    return X_features


def predict(features):
    preds = model.predict(features)
    return int(preds[0])


model, vect = load_model_n_vect(RUN_ID)

app = Flask("stress-prediction")


@app.route("/predict", methods=["POST"])
def predict_endpoint():
    stress_data = request.get_json()
    stress_data = pd.DataFrame([stress_data])

    features = prepare_features(stress_data, vect)
    pred = predict(features)

    result = {"prediction": pred, "model_version": RUN_ID}

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=9696)
    # RUN_ID = os.getenv('RUN_ID',"57342ae687254eeeac28602bb8d42aca")
    # load_model_n_vect(RUN_ID)
