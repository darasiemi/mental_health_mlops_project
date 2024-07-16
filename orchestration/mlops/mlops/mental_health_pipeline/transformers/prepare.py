if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


from mlops.utils.mental_health_pipeline.cleaning import removal
from mlops.utils.mental_health_pipeline.splitters import split_data
from mlops.utils.mental_health_pipeline.feature_engineering import feature_transformation

@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    
    data = feature_transformation(data)

    x_train,x_test,y_train,y_test = split_data(data)
    print("Tranformed successfully")
    
    
    return data, x_train,x_test,y_train,y_test


# @test
# def test_output(output, *args) -> None:
#     """
#     Template code for testing the output of the block.
#     """
#     assert output is not None, 'The output is undefined