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

To run the model as a web service, first create a deployment environment 
```bash
pipenv install scikit-learn==1.4.2 flask nltk==3.8.1 mlflow==2.12.2 --python=3.11
``` 
To launch pip environment
```bash
pipenv shell
```

To launch web-service 
```bash
python predict.py
```
To send requests to the service and get predictions
```bash
python test.py
```
In case there is ModuleNotFound error for requests, run
```bash
pipenv install --dev requests
```

To run in production server
```bash
gunicorn --bind=0.0.0.0:9696 predict:app
```
To build image
```bash
docker build -t stress-prediction-service:v1 .
```

To run docker image
```bash
docker run -e AWS_ACCESS_KEY_ID=your_access_key -e AWS_SECRET_ACCESS_KEY=your_secret_key -it --rm -p 9696:9696  stress-prediction-service:v1
```