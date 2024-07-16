from datetime import datetime

import pandas as pd
import sqlite3

from mlops.utils.logging import DEFAULT_TRACKING_URI


import mlflow
import mlflow.tracking
import pandas as pd
from datetime import datetime

def data_load(*args, **kwargs) -> pd.DataFrame:
    mlflow.set_tracking_uri(DEFAULT_TRACKING_URI)

    client = mlflow.tracking.MlflowClient()
    print("client created successfully")

    experiment_id = kwargs.get('experiment_id', '1')  # Set your experiment ID or provide via kwargs
    runs = client.search_runs(experiment_ids=[experiment_id], filter_string="", run_view_type=1)
    print("read runs successfully")
    processed_rows = []
    for run in runs:
        run_uuid = run.info.run_uuid
        run_id = run.info.run_id
        
        # Retrieve model name from tags
        model = run.data.tags.get("mlflow.runName", "Unknown Model")  # Change this key if you use a different tag for model name
        print("read run model successfully")
        # Check for the specific metrics
        accuracy_combined = run.data.metrics.get("accuracy_combined", None)
        accuracy_text_only = run.data.metrics.get("accuracy_text_only", None)
        
        accuracy = accuracy_combined if accuracy_combined is not None else accuracy_text_only

        accuracy = round(accuracy*100,2)


        data = dict(
            model=model,
            accuracy=accuracy,
            run_id=run_id,
            run_uuid=run_uuid,
        )
        if accuracy is not None:
            data[f'accuracy_{model}'] = accuracy

        processed_rows.append(data)

    return pd.DataFrame(processed_rows)



# def load_data(*args, **kwargs) -> pd.DataFrame:
#     with sqlite3.connect(DEFAULT_TRACKING_URI.split('/')[-1]) as conn:
#         cursor = conn.cursor()

#         cursor.execute(QUERY)

#         rows = cursor.fetchall()
#         processed_rows = []
#         for row in rows:
#             run_uuid, run_id, model, start_time, accuracy = row
#             start_time = datetime.utcfromtimestamp(start_time / 1000)
#             start_time_day = start_time.day
#             start_time_hour = start_time.hour
#             start_time_minute = start_time.minute
#             start_time_format_day = start_time.strftime('%Y-%m-%d')
#             start_time_format_hour = start_time.strftime('%Y-%m-%d %H:%M')
#             start_time_format_minute = start_time.strftime('%H:%MD%d')


#             data = dict(
#                 model=model,
#                 mse=mse,
#                 rmse=rmse,
#                 run_id=run_id,
#                 run_uuid=run_uuid,
#                 start_time=start_time,
#                 start_time_day=start_time_day,
#                 start_time_format_day=start_time_format_day,
#                 start_time_format_hour=start_time_format_hour,
#                 start_time_format_minute=start_time_format_minute,
#                 start_time_hour=start_time_hour,
#                 start_time_minute=start_time_minute,
#             )
#             data[f'mse_{model}'] = mse
#             data[f'rmse_{model}'] = rmse

#             processed_rows.append(data)

#         return pd.DataFrame(processed_rows)
