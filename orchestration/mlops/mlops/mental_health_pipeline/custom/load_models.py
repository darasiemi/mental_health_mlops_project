if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test



from typing import List, Dict, Tuple

@custom
def models(*args, **kwargs) -> Tuple[List[str], List[Dict[str, str]]]:
    """
    models: comma separated strings
        ensemble.RandomForestClassifier
        tree.DecisionTreeClassifier
    """
    model_names: str = kwargs.get(
        'models', 'linear_model.LogisticRegression,ensemble.RandomForestClassifier,tree.DecisionTreeClassifier,naive_bayes.GaussianNB'
    )
    child_data: List[str] = [
        model_name.strip() for model_name in model_names.split(',')
    ]
    child_metadata: List[Dict] = [
        dict(block_uuid=model_name.split('.')[-1]) for model_name in child_data
    ]

    return child_data, child_metadata

