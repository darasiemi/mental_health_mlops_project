import pandas as pd

def feature_transformation(df):
    date_column = ['social_timestamp']
    numerical_columns = ['lex_liwc_Tone',
            'lex_liwc_negemo',
            'lex_liwc_i',
            'lex_liwc_Clout',
            'sentiment']
    categorical_columns = ['text']
    target = ["label"]

    df = df[date_column + numerical_columns + categorical_columns + target]
    df['social_timestamp'] = pd.to_datetime(df['social_timestamp'], unit='s')

    return df