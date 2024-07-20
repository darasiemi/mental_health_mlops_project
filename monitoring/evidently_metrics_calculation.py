import datetime
import time
# import random
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.model_loader import model, vect
from utils.feature_engineering import feature_transformation
from utils.encoders import prepare_features

import logging 
import uuid
import pytz
import pandas as pd
import io
import psycopg
import joblib

import random

from prefect import task, flow

from evidently.report import Report
from evidently import ColumnMapping
from evidently.metrics import ColumnDriftMetric, DatasetDriftMetric, DatasetMissingValuesMetric,TextDescriptorsDriftMetric

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")

SEND_TIMEOUT = 10
rand = random.Random()

create_table_statement = """
drop table if exists metrics_table;
create table metrics_table(
	timestamp timestamp,
	prediction_drift float,
	num_drifted_columns integer,
	number_of_different_missing_values integer,
	oov_drift_score float
)
"""

raw_data = pd.read_csv('../data/dreaddit-test.csv')
reference_data = pd.read_parquet("../data/reference.parquet")

numerical_columns = ["lex_liwc_Tone", "lex_liwc_i", "lex_liwc_negemo", "lex_liwc_Clout", "sentiment"]
categorical_columns = ["text"]
column_mapping = ColumnMapping(
    target=None,
    prediction='predictions',
    numerical_features=numerical_columns,
    text_features = categorical_columns
    # categorical_features=categorical_columns
)

report = Report(
   metrics=[
       ColumnDriftMetric('predictions'),
       DatasetDriftMetric(),
       DatasetMissingValuesMetric(),
       TextDescriptorsDriftMetric(column_name= "text")
       
   ]
)
begin = datetime.datetime.today()
# begin = datetime.datetime(2022, 2, 1, 0, 0)

@task
def prep_db():
	with psycopg.connect("host=localhost port=5432 user=postgres password=example", autocommit=True) as conn:
		res = conn.execute("SELECT 1 FROM pg_database WHERE datname='test'")
		if len(res.fetchall()) == 0:
			conn.execute("create database test;")
		with psycopg.connect("host=localhost port=5432 dbname=test user=postgres password=example") as conn:
			conn.execute(create_table_statement)

@task
def calculate_metrics_postgresql(curr, i):
	print(i)
	batch_size = 5
	batch_end = min(i + batch_size, len(raw_data))

	# current_data = feature_transformation(raw_data)
	current_data = raw_data.iloc[i:batch_end]
	features, _ = prepare_features(current_data, vect)

	current_data['predictions'] = model.predict(features)
	# print(current_data['predictions'])

	report.run(reference_data = reference_data, current_data = current_data,
		column_mapping=column_mapping)

	result = report.as_dict()

	prediction_drift = result["metrics"][0]["result"]["drift_score"]
	num_drifted_columns = result['metrics'][1]['result']['number_of_drifted_columns']
	number_of_different_missing_values = result["metrics"][2]["result"]["current"]["number_of_different_missing_values"]
	oov_drift_score = result["metrics"][3]["result"]["drift_by_columns"]["OOV %"]["drift_score"]

	curr.execute(
		"insert into metrics_table(timestamp, prediction_drift, num_drifted_columns, number_of_different_missing_values, oov_drift_score) values (%s, %s, %s, %s, %s)",
		(begin + datetime.timedelta(i), prediction_drift, num_drifted_columns, number_of_different_missing_values, oov_drift_score)
	)

@flow
def batch_monitoring_backfill():
	prep_db()
	last_send = datetime.datetime.now() - datetime.timedelta(seconds=10)
	with psycopg.connect("host=localhost port=5432 dbname=test user=postgres password=example", autocommit=True) as conn:
		for i in range(0, 27):
			with conn.cursor() as curr:
				calculate_metrics_postgresql(curr, i)

			new_send = datetime.datetime.now()
			seconds_elapsed = (new_send - last_send).total_seconds()
			if seconds_elapsed < SEND_TIMEOUT:
				time.sleep(SEND_TIMEOUT - seconds_elapsed)
			while last_send < new_send:
				last_send = last_send + datetime.timedelta(seconds=10)
			logging.info("data sent")

if __name__ == '__main__':
	batch_monitoring_backfill()