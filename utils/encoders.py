import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import CountVectorizer

from utils.cleaning import removal

numerical_columns = [
    "lex_liwc_Tone",
    "lex_liwc_negemo",
    "lex_liwc_i",
    "lex_liwc_Clout",
    "sentiment",
]

scaler = StandardScaler()


def process_categorical_features(df, vect=None):
    posts = df[["text"]]
    posts["text"] = posts["text"].apply(removal)
    # posts["sentiment"] = posts["text"].apply(mood)
    X = posts["text"]
    if vect:
        X = vect.transform(X)
    else:
        vect = CountVectorizer(stop_words="english")
        X = vect.fit_transform(X)
    return X, vect


def process_numerical_features(df):
    X_numerical = df[numerical_columns]
    X_numerical = scaler.fit_transform(X_numerical)
    return X_numerical


def prepare_features(df, vect=None):
    X_categorical, vect = process_categorical_features(df, vect)
    X_numerical = process_numerical_features(df)
    X_combined = np.hstack((X_categorical.toarray(), X_numerical))

    return X_combined, vect
