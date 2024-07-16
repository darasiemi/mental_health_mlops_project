from typing import Dict, List, Tuple, Union

# from sklearn.feature_extraction import DictVectorizer
# from xgboost import Booster

import pandas as pd

# from mlops.utils.data_preparation.feature_engineering import combine_features
from mlops.utils.models.xgboost import build_data
from sklearn.feature_extraction.text import CountVectorizer
from mlops.utils.mental_health_pipeline.feature_engineering import feature_transformation

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom

# numerical_columns = ['lex_liwc_Tone',
#             'lex_liwc_negemo',
#             'lex_liwc_i',
#             'lex_liwc_Clout',
#             'sentiment']
# categorical_columns = ['text']

# DEFAULT_INPUTS = [
#     {
#         # target = "duration": 11.5
#         'DOLocationID': 239,
#         'PULocationID': 236,
#         'trip_distance': 1.98,
#     },
#     {
#         # target = "duration" 20.8666666667
#         'DOLocationID': '170',
#         'PULocationID': '65',
#         'trip_distance': 6.54,
#     },
# ]


@custom
def predict(
    sklearn_set,
    **kwargs,
) -> List[float]:
    # inputs: List[Dict[str, Union[float, int]]] = kwargs.get('inputs', DEFAULT_INPUTS)
    # inputs = combine_features(inputs)

    print(len(sklearn_set["sklearn_model"]))
    # model, model_info, vect, _, _, _ = sklearn_set['sklearn_model']
    vect = 0
    print(vect)
    df = pd.read_csv("/home/src/mlops/data/dreaddit-test.csv")
    print(df)
    test = df[0]
    # DOLocationID = kwargs.get('DOLocationID')
    # PULocationID = kwargs.get('PULocationID')
    # trip_distance = kwargs.get('trip_distance')

    # if DOLocationID is not None or PULocationID is not None or trip_distance is not None:
    #     inputs = [
    #         {
    #             'DOLocationID': DOLocationID,
    #             'PULocationID': PULocationID,
    #             'trip_distance': trip_distance,
    #         },
    #     ]

    x_features, vect = prepare_features(df, vect)
    
    # model, vectorizer = model_settings['xgboost']
    # vectors = vectorizer.transform(inputs)

    predictions = model.predict(build_data(vectors))

    # for idx, input_feature in enumerate(inputs):
    #     print(f'Prediction of duration using these features: {predictions[idx]}')
    #     for key, value in inputs[idx].items():
    #         print(f'\t{key}: {value}')

    return predictions.tolist()
