To convert notebook to python script
```bash
jupyter nbconvert --to script stress_prediction_batch.ipynb
```
Set environment variable for run_id
```bash
export RUN_ID={your_run_id}
```
To run python script
```bash
python stress_prediction_batch.py dreaddit-test.csv output/stress_predictions.parquet
```