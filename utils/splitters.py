from sklearn.model_selection import train_test_split


def split_data(df):
    y = df["label"]
    numerical_columns = [
        "lex_liwc_Tone",
        "lex_liwc_negemo",
        "lex_liwc_i",
        "lex_liwc_Clout",
        "sentiment",
    ]
    categorical_columns = ["text"]
    X = df[numerical_columns + categorical_columns]

    x_train, x_test, y_train, y_test = train_test_split(X, y, random_state=43)

    return x_train, x_test, y_train, y_test
