import os
from utils import model

PREDICTIONS_STREAM_NAME = os.getenv('PREDICTIONS_STREAM_NAME', 'stress_predictions')
RUN_ID = os.getenv('RUN_ID',"57342ae687254eeeac28602bb8d42aca")
TEST_RUN = os.getenv('TEST_RUN', 'False') == 'True'

model_service = model.init(
    prediction_stream_name=PREDICTIONS_STREAM_NAME,
    run_id=RUN_ID,
    test_run=TEST_RUN,
)

def lambda_handler(event, context):
    # pylint: disable=unused-argument
    return model_service.lambda_handler(event)
