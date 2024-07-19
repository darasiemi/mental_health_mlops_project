I have explored the modes of deploying the stress prediction model, specifically batch processing, web service deployment, and real-time streaming.

## Table of Contents
- [Batch](#batch)
- [Web Service](#web-service)
- [Streaming](#streaming)

### Batch
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
### Web Service
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
### Streaming
Create a new file data.json with the content found in `streaming/` folder

Run the command below to encode it
```bash
base64 -w 0 data.json
```
To put record in kinesis
```bash
  KINESIS_STREAM_INPUT=stress_events
  aws kinesis put-record \
     --stream-name ${KINESIS_STREAM_INPUT} \
     --partition-key 1 \
     --data 'ewogICAgInRleHQiOiAiSXRzIGxpa2UgdGhhdCwgaWYgeW91IHdhbnQgb3Igbm90LiBNRTogSSBoYXZlIG5vIHByb2JsZW0sIGlmIGl0IHRha2VzIGxvbmdlci4gQnV0IHlvdSBhc2tlZCBteSBmcmllbmQgZm9yIGhlbHAgYW5kIGxldCBoaW0gd2FpdCBmb3Igb25lIGhvdXIgYW5kIHRoZW4geW91IGhhdmVu4oCZdCBwcmVwYXJlZCBhbnl0aGluZy4gVGhhdHMgbm90IHdoYXQgeW91IGFza2VkIGZvci4gSW5zdGVhZCBvZiAzIGhvdXJzLCBoZSBoZWxwZWQgeW91IGZvciAxMCBob3VycyB0aWxsIDVhbS4uLiIsCiAgICAibGV4X2xpd2NfVG9uZSI6IDUuOTUsCiAgICAibGV4X2xpd2NfaSI6IDUuNDUsCiAgICAibGV4X2xpd2NfbmVnZW1vIjogMS44MiwKICAgICJsZXhfbGl3Y19DbG91dCI6IDU3LjIyLAogICAgInNlbnRpbWVudCI6IDAuMAp9' \
 ```

This is because the data is encoded as base64 in lambda, and we cannot pass string values in the CLI under data. Alternatively, the data can be viewed when we `print(json.dumps(event))` in the lambda function. The output of the record can be found in event.json.

To run the Kinesis stream
```bash
 export PREDICTIONS_STREAM_NAME="stress_predictions"
 export RUN_ID="57342ae687254eeeac28602bb8d42aca"
 export TEST_RUN="True"

python test.py
 ```
 To build the image from the Dockerfile
 ```bash
 docker build -t stream-prediction-model:v1 .
 ```
 To run it as a container. Remember to update the credentials and region with your own parameters. Also update the RUN_ID with your run ID.
```bash
  docker run -it --rm \
    -e AWS_ACCESS_KEY_ID=your_access_key \
    -e AWS_SECRET_ACCESS_KEY=your_secret_key \
    -e AWS_DEFAULT_REGION=your_region \
    -e PREDICTIONS_STREAM_NAME="stress_predictions" \
    -e RUN_ID="57342ae687254eeeac28602bb8d42aca"
    -e TEST_RUN="True"
    -p 8080:8080 \  
    stream-prediction-model:v1 \
```

When this runs, you can then push the image to ECR. First you create the ECR repository to house the Image
To create elastic container registry for docker container
`aws ecr create-repository --repository-name stress-model`

Logging in
`$(aws ecr get-login --no-include-email)`

```bash
 REMOTE_URI="387546586013.dkr.ecr.eu-north-1.amazonaws.com/stress-model"
 REMOTE_TAG="v1"
 REMOTE_IMAGE=${REMOTE_URI}:${REMOTE_TAG}

 LOCAL_IMAGE="stream-prediction-model:v1"
 docker tag ${LOCAL_IMAGE} ${REMOTE_IMAGE}
 docker push ${REMOTE_IMAGE}
 ```

You can then deploy this on AWS. Remember to give your Lambda function access to S3. This will allow it fetch the model artifacts. Also you will have to create a lambda function that is built on the image

To read from the stream
```bash
 KINESIS_STREAM_OUTPUT='stress_predictions'
 SHARD='shardId-000000000000'

 SHARD_ITERATOR=$(aws kinesis \
     get-shard-iterator \
         --shard-id ${SHARD} \
         --shard-iterator-type TRIM_HORIZON \
         --stream-name ${KINESIS_STREAM_OUTPUT} \
         --query 'ShardIterator' \
 )

 RESULT=$(aws kinesis get-records --shard-iterator $SHARD_ITERATOR)

 echo ${RESULT} | jq -r '.Records[0].Data' | base64 --decode
 ```


