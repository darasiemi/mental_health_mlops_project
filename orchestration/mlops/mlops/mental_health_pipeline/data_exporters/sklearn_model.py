from typing import Callable, Dict, Tuple, Union, Any

from pandas import Series
from scipy.sparse._csr import csr_matrix
from sklearn.base import BaseEstimator

from mlops.utils.models.sklearn import load_class, train_model

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

def convert_hyperparams_to_int(hyperparams: Dict[str, Any]) -> Dict[str, Any]:
    for key, value in hyperparams.items():
        if isinstance(value, (int, float)):
            hyperparams[key] = int(value)
    return hyperparams

@data_exporter
def train(
    training_set: Dict[str, Union[Series, csr_matrix]],
    settings: Tuple[
        Dict[str, Union[bool, float, int, str]],
        csr_matrix,
        Series,
        Dict[str, Union[Callable[..., BaseEstimator], str]],
    ],
    **kwargs,
) -> Tuple[BaseEstimator, Dict[str, str]]:
    hyperparameters, X, y, model_info = settings
    print(model_info)

    hyperparameters = convert_hyperparams_to_int(hyperparameters,)

    model_class = model_info['cls']
    model = model_class(**hyperparameters)
    model.fit(X, y)
    vectorizer = training_set['build'][4]

    return model, model_info, vectorizer