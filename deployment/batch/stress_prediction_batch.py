#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Adapted from https://www.kaggle.com/code/ruchitass/predicting-stress-a-machine-learning-approach

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import nltk
import re
import sys

# Download the stopwords resource
nltk.download('stopwords')

stemmer = nltk.SnowballStemmer("english")

from wordcloud import STOPWORDS
from PIL import Image
from wordcloud import WordCloud

# from textblob import TextBlob
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_selection import mutual_info_classif
from sklearn.preprocessing import StandardScaler
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier


# import nltk
# import re
# stemmer = nltk.SnowballStemmer("english")
from nltk.corpus import stopwords
stopwords = stopwords.words('english')
# import string

import matplotlib.pyplot as plt
import kaggle
import pickle


from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
# import warnings
# warnings.filterwarnings("ignore")

import string
#Get a list of punctuations
punct = []
for char in string.punctuation:
    punct.append(char)


# In[4]:


import warnings

# Suppress all warnings
warnings.filterwarnings('ignore')


import mlflow
from mlflow.tracking import MlflowClient
import os

#os.environ["AWS_PROFILE"] = "dara" # fill in with your AWS profile. More info: https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/setup.html#setup-credentials

TRACKING_SERVER_HOST = "ec2-13-53-192-42.eu-north-1.compute.amazonaws.com" # fill in with the public DNS of the EC2 instance
mlflow.set_tracking_uri(f"http://{TRACKING_SERVER_HOST}:5000")

EXPERIMENT_NAME = "random-forest-best-models"
mlflow.set_experiment(EXPERIMENT_NAME)

run_id = os.getenv("RUN_ID", "57342ae687254eeeac28602bb8d42aca")

input_file = "dreaddit-test.csv"
output_file = "output/stress_predictions.parquet"

if not os.path.exists("output"):
    os.makedirs("output")

def read_dataframe(filename):
    # dreaddit-test.csv
    df = pd.read_csv(f"../../data/{filename}")
    
    return df

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
    # posts["sentiment"] = posts["text"].apply(mood)
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
    
def load_model_n_vect(run_id):
    logged_model = f'runs:/{run_id}/model'

    # Load model as a PyFuncModel.
    loaded_model = mlflow.pyfunc.load_model(logged_model)

    client = MlflowClient()

    client.download_artifacts(run_id=run_id, path='vectorizer', dst_path='.')
    
    with open("vectorizer/vectorizer.b", "rb") as f_in:
        vect = pickle.load(f_in)
        
    return loaded_model, vect

def apply_model(input_file, run_id, output_file):

    df = read_dataframe(input_file)
    model, vect = load_model_n_vect(run_id)

    X_test = prepare_features(df, vect)
    assert X_test.shape[1] == 9453, "feature size does not match"
    
    y_pred = model.predict(X_test)
    "lex_liwc_Tone", "lex_liwc_i", "lex_liwc_negemo", "lex_liwc_Clout", "sentiment"
    df_result = pd.DataFrame()
    df_result['text'] = df['text']
    df_result['lex_liwc_Tone'] = df['lex_liwc_Tone']
    df_result['lex_liwc_i'] = df['lex_liwc_i']
    df_result['lex_liwc_negemo'] = df['lex_liwc_negemo']
    df_result['lex_liwc_Clout'] = df['lex_liwc_Clout']
    df_result['sentiment'] = df['sentiment']
    df_result['actual_label'] = df['label']
    df_result['predicted_stress'] = y_pred
    df_result['diff'] = df_result['actual_label'] - df_result['predicted_stress']
    df_result['model_version'] = run_id
    
    df_result.to_parquet(output_file, index=False)


if __name__ == '__main__':
    input_file = sys.argv[1] 
    output_file = sys.argv[2]
    apply_model(input_file=input_file, run_id=run_id, output_file=output_file)
    print("code runs successfully")
    