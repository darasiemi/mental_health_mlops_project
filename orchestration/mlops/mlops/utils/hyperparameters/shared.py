from typing import Callable, Dict, List, Tuple, Union

from hyperopt import hp, tpe
from hyperopt.pyll import scope
# from sklearn.ensemble import (
#     ExtraTreesRegressor,
#     GradientBoostingRegressor,
#     RandomForestRegressor,
# )
# from sklearn.linear_model import Lasso, LinearRegression
# from sklearn.svm import LinearSVR
from xgboost import Booster
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier


def build_hyperparameters_space(
    model_class: Callable[
        ...,
        Union[
            RandomForestClassifier,
            DecisionTreeClassifier,
            Booster,
        ],
    ],
    random_state: int = 42,
    **kwargs,
) -> Tuple[Dict, Dict[str, List]]:
    params = {}
    choices = {}

    if RandomForestClassifier is model_class:
        params = dict(
            n_estimators =scope.int(hp.quniform('n_estimators', 10, 200, 1)),
            min_samples_split= scope.int(hp.quniform('min_samples_split', 2, 5, 1)),
            random_state= random_state,
        )

    if DecisionTreeClassifier is model_class:
         params = dict(
            max_depth=scope.int(hp.quniform('max_depth', 1, 20, 1)),
            min_samples_split=scope.int(hp.quniform('min_samples_split', 2, 5, 1)),
            min_samples_leaf=scope.int(hp.quniform('min_samples_leaf', 1, 5, 1)),
            random_state=random_state,
        )

    if Booster is model_class:
        params = dict(
            # Controls the fraction of features (columns) that will be randomly sampled for each tree.
            colsample_bytree=hp.uniform('colsample_bytree', 0.5, 1.0),
            # Minimum loss reduction required to make a further partition on a leaf node of the tree.
            gamma=hp.uniform('gamma', 0.1, 1.0),
            learning_rate=hp.loguniform('learning_rate', -3, 0),
            # Maximum depth of a tree.
            max_depth=scope.int(hp.quniform('max_depth', 4, 100, 1)),
            min_child_weight=hp.loguniform('min_child_weight', -1, 3),
            # Number of gradient boosted trees. Equivalent to number of boosting rounds.
            # n_estimators=hp.choice('n_estimators', range(100, 1000))
            num_boost_round=hp.quniform('num_boost_round', 500, 1000, 10),
            objective='reg:squarederror',
            # Preferred over seed.
            random_state=random_state,
            # L1 regularization term on weights (xgb’s alpha).
            reg_alpha=hp.loguniform('reg_alpha', -5, -1),
            # L2 regularization term on weights (xgb’s lambda).
            reg_lambda=hp.loguniform('reg_lambda', -6, -1),
            # Fraction of samples to be used for each tree.
            subsample=hp.uniform('subsample', 0.1, 1.0),
        )

    for key, value in choices.items():
        params[key] = hp.choice(key, value)

    if kwargs:
        for key, value in kwargs.items():
            if value is not None:
                kwargs[key] = value

    return params, choices
