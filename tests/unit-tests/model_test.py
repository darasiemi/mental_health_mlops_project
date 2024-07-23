# import lambda_function

from pathlib import Path

import sys
import os
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import utils.model as model_manager
from utils.model_loader import model, vect
from utils.encoders import prepare_features


def read_text(file):
    test_directory = Path(__file__).parent

    with open(test_directory / file, 'rt', encoding='utf-8') as f_in:
        return f_in.read().strip()


def test_base64_decode():
    base64_input = read_text('data.b64')

    actual_result = model_manager.base64_decode(base64_input)
    expected_result = {
                    "text": "Its like that, if you want or not. ME: I have no problem, if it takes longer. But you asked my friend for help and let him wait for one hour and then you haven’t prepared anything. Thats not what you asked for. Instead of 3 hours, he helped you for 10 hours till 5am...",
                    "lex_liwc_Tone": 5.95,
                    "lex_liwc_i": 5.45,
                    "lex_liwc_negemo": 1.82,
                    "lex_liwc_Clout": 57.22,
                    "sentiment": 0.0
                }


    assert actual_result == expected_result

def test_prepare_features():
    input =    {
                    "text": "Its like that, if you want or not. ME: I have no problem, if it takes longer. But you asked my friend for help and let him wait for one hour and then you haven’t prepared anything. Thats not what you asked for. Instead of 3 hours, he helped you for 10 hours till 5am...",
                    "lex_liwc_Tone": 5.95,
                    "lex_liwc_i": 5.45,
                    "lex_liwc_negemo": 1.82,
                    "lex_liwc_Clout": 57.22,
                    "sentiment": 0.0
                }
    input = pd.DataFrame([input])
    features, _ = prepare_features(input, vect)
    actual_feature_shape = features.shape[1]
    expected_feature_shape = 9453

    assert actual_feature_shape == expected_feature_shape

def test_predict():
    model_service = model_manager.ModelService(model)

    input =    {
                    "text": "Its like that, if you want or not. ME: I have no problem, if it takes longer. But you asked my friend for help and let him wait for one hour and then you haven’t prepared anything. Thats not what you asked for. Instead of 3 hours, he helped you for 10 hours till 5am...",
                    "lex_liwc_Tone": 5.95,
                    "lex_liwc_i": 5.45,
                    "lex_liwc_negemo": 1.82,
                    "lex_liwc_Clout": 57.22,
                    "sentiment": 0.0
                }
    input = pd.DataFrame([input])
    features, _ = prepare_features(input, vect)
    prediction = model_service.predict(features)

    assert prediction in [0, 1], f"Prediction is not 0 or 1: {prediction}"

def test_lambda_handler():
    model_version = '123'
    model_service = model_manager.ModelService(model, model_version)

    base64_input = read_text('data.b64')

    event = {
        "Records": [
            {
                "kinesis": {
                    "data": base64_input,
                },
            }
        ]
    }

    actual_predictions = model_service.lambda_handler(event)
    expected_predictions = {
        'predictions': [
            {
                'model': 'stress_prediction_model',
                'version': model_version,
                'prediction': {
                   'stress_prediction': 0
                },
            }
        ]
    }

    assert actual_predictions == expected_predictions


