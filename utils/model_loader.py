import os
import mlflow
import boto3
import pickle
from io import BytesIO

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

RUN_ID = os.getenv('RUN_ID',"57342ae687254eeeac28602bb8d42aca")
model, vect = load_model_n_vect(RUN_ID)

print("Model imported successfully")

if __name__ == "__main__":
    RUN_ID = os.getenv('RUN_ID',"57342ae687254eeeac28602bb8d42aca")
    model, vect = load_model_n_vect(RUN_ID)
    print("Model loaded successfully")

