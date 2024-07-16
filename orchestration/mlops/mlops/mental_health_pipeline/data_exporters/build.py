if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

import numpy as np
import pandas as pd
from scipy.sparse._csr import csr_matrix
from pandas import DataFrame, Series

from mlops.utils.mental_health_pipeline.encoders import prepare_features,process_categorical_features,process_numerical_features

@data_exporter
def export_data(data, *args, **kwargs):
    """
    Exports data to some source.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Output (optional):
        Optionally return any object and it'll be logged and
        displayed when inspecting the block run.
    """
    # Specify your data exporting logic here

    df, x_train,x_val,y_train,y_val = data

    x_train_combined, vect = prepare_features(x_train)

    print(x_train_combined.shape)
    x_val_combined, vect = prepare_features(x_val,vect)
    print(x_val_combined.shape)

    print(type(x_train_combined))

    return x_train_combined, x_val_combined, y_train,y_val,vect 

    # print(x_combined)

@test
def test_training_set(
    x_train_combined: csr_matrix,
    x_val_combined: csr_matrix,
    y_train: Series,
    y_val: Series,
    *args,
) -> None:
    print(x_train_combined)
    assert (
        x_train_combined.shape[0] == 2128
    ), f'Training set for training model should have 2128 examples, but has {X_train.shape[0]}'
    assert (
        x_train_combined.shape[1] == 8318
    ), f'Training set for training model should have 8318 features, but has {X_train.shape[1]}'
    assert (
        len(y_train.index) == x_train_combined.shape[0]
    ), f'Training set for training model should have {X_train.shape[0]} examples, but has {len(y_train.index)}'


@test
def test_validation_set(
    x_train_combined: csr_matrix,
    x_val_combined: csr_matrix,
    y_train: Series,
    y_val: Series,
    *args,
) -> None:
    assert (
        x_val_combined.shape[0] == 710
    ), f'Training set for validation should have 710 examples, but has {X_val.shape[0]}'
    assert (
        x_val_combined.shape[1] ==  8318
    ), f'Training set for validation should have 8318 features, but has {X_val.shape[1]}'
    assert (
        len(y_val.index) == x_val_combined.shape[0]
    ), f'Training set for training model should have {X_val.shape[0]} examples, but has {len(y_val.index)}'
