#!/usr/bin/env bash

cd "$(dirname "$0")"

RUN_ID="57342ae687254eeeac28602bb8d42aca"
EXPERIMENT_ID=3
MODEL_BUCKET="mlflows-artifacts-remote"
MODEL_DIR="../../model"
VECTORIZER_DIR="../../vectorizer"

#Download Model and Vectorizer
# Function to download model
download_model() {
    echo "Downloading model..."
    aws s3 cp --recursive s3://$MODEL_BUCKET/$EXPERIMENT_ID/$RUN_ID/artifacts/model/ $MODEL_DIR
}

# Function to download vectorizer
download_vectorizer() {
    echo "Downloading vectorizer..."
    aws s3 cp --recursive s3://$MODEL_BUCKET/$EXPERIMENT_ID/$RUN_ID/artifacts/vectorizer/ $VECTORIZER_DIR
}

# Check if model directory exists and is not empty
if [ -d "$MODEL_DIR" ] && [ "$(ls -A $MODEL_DIR)" ]; then
    echo "Model directory already exists and is not empty. Skipping download."
else
    download_model
fi

# Check if vectorizer directory exists and is not empty
if [ -d "$VECTORIZER_DIR" ] && [ "$(ls -A $VECTORIZER_DIR)" ]; then
    echo "Vectorizer directory already exists and is not empty. Skipping download."
else
    download_vectorizer
fi

#Stress predictions
export PREDICTIONS_STREAM_NAME="stress_predictions"
#Set environment variables and build image
if [ "${LOCAL_IMAGE_NAME}" == "" ]; then
    LOCAL_TAG=`date +"%Y-%m-%d-%H-%M"`
    export LOCAL_IMAGE_NAME="stream-model-stress:${LOCAL_TAG}"
    export AWS_DEFAULT_REGION="eu-north-1"
    echo "LOCAL_IMAGE_NAME is not set, building a new image with tag ${LOCAL_IMAGE_NAME}"
    docker build -t ${LOCAL_IMAGE_NAME} ../../
else
    echo "no need to build image ${LOCAL_IMAGE_NAME}"
fi

#Run with tag -d so it can get back the terminal after running docker compose
docker-compose up -d

#To wait for docker compose to run
sleep 5

#To create stream in localstark for integration test
aws --endpoint-url=http://localhost:4566 \
    kinesis create-stream \
    --stream-name ${PREDICTIONS_STREAM_NAME} \
    --shard-count 1

#To check list of streams
aws --endpoint-url=http://localhost:4566 \
    kinesis list-streams

#To run test to put the records in the stream
pipenv run python test_docker.py

#If there is error, stop and remove container
ERROR_CODE=$?

if [ ${ERROR_CODE} != 0 ]; then
    docker-compose logs
    docker-compose down
    exit ${ERROR_CODE}
fi

#To run test to check record in kinesis
pipenv run python test_kinesis.py

#If there is error, stop and remove container
ERROR_CODE=$?

if [ ${ERROR_CODE} != 0 ]; then
    docker-compose logs
    docker-compose down
    exit ${ERROR_CODE}
fi
