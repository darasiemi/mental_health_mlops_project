import os
import mlflow
import boto3
import pickle
from io import BytesIO

# s3_location = os.getenv("MODEL_BUCKET","mlflows-artifacts-remote")

def load_model_n_vect():
    logged_model = f'model'
    model = mlflow.pyfunc.load_model(logged_model)

    with open("vectorizer/vectorizer.b", "rb") as f_in:
        vect = pickle.load(f_in)

    print("model and vect loaded successfully")
    
    return model, vect

model, vect = load_model_n_vect()

print("Model imported successfully")

if __name__ == "__main__":
    model, vect = load_model_n_vect()
    print("Model loaded successfully")

