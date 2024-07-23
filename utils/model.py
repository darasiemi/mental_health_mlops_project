import os
import json
import base64

import boto3
import mlflow

import sys
import os
import pandas as pd

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.model_loader import vect
from utils.model_loader import load_model_n_vect
# from feature_engineering import feature_transformation
from utils.encoders import prepare_features

def base64_decode(encoded_data):
    decoded_data = base64.b64decode(encoded_data).decode('utf-8')
    ride_event = json.loads(decoded_data)
    return ride_event


class ModelService:
    def __init__(self, model, model_version=None, callbacks=None):
        self.model = model
        self.model_version = model_version
        self.callbacks = callbacks or []

    def predict(self, features):
        pred = self.model.predict(features)
        return int(pred[0])

    def lambda_handler(self, event):    
        predictions_events = []
        predictions = []
        
        for record in event['Records']:
            encoded_data = record['kinesis']['data']
            decoded_data = base64.b64decode(encoded_data).decode('utf-8')
            # print(decoded_data)
            
            stress_event = json.loads(decoded_data)
            stress_event  = pd.DataFrame([stress_event])
            #print(stress_event)
        
            features, _ = prepare_features(stress_event, vect)
            prediction = self.predict(features)

            predictions.append({
                'stress_prediction': prediction })
            
            prediction_event = {
                'model': 'stress_prediction_model',
                'version': '123',
                'prediction': {
                    'stress_prediction': prediction,  
                }
            }

            for callback in self.callbacks:
                callback(prediction_event)

            predictions_events.append(prediction_event)

            return {'predictions': predictions_events}

class KinesisCallback:
    def __init__(self, kinesis_client, prediction_stream_name):
        self.kinesis_client = kinesis_client
        self.prediction_stream_name = prediction_stream_name

    def put_record(self, prediction_event):
        # ride_id = prediction_event['prediction']['ride_id']

        self.kinesis_client.put_record(
            StreamName=self.prediction_stream_name,
            Data=json.dumps(prediction_event)
        )


def create_kinesis_client():
    endpoint_url = os.getenv('KINESIS_ENDPOINT_URL')

    if endpoint_url is None:
        return boto3.client('kinesis')

    return boto3.client('kinesis', endpoint_url=endpoint_url)


def init(prediction_stream_name: str, run_id: str, test_run: bool):
    model, _ = load_model_n_vect(run_id)

    callbacks = []
    print(test_run)

    if not test_run:
        kinesis_client = create_kinesis_client()
        kinesis_callback = KinesisCallback(kinesis_client, prediction_stream_name)
        callbacks.append(kinesis_callback.put_record)

    model_service = ModelService(model=model, model_version=run_id, callbacks=callbacks)

    return model_service
