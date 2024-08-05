import pickle

import mlflow


def load_model_vect():
    "Load data locally"
    logged_model_path = "../model"
    local_model = mlflow.pyfunc.load_model(logged_model_path)

    with open("../vectorizer/vectorizer.b", "rb") as f_in:
        local_vect = pickle.load(f_in)

    print("model and vect loaded successfully")
    return local_model, local_vect


model, vect = load_model_vect()

print("Model imported successfully")

if __name__ == "__main__":
    model, vect = load_model_vect()
    print("Model loaded successfully")
