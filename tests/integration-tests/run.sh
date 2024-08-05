#!/usr/bin/env bash

cd "$(dirname "$0")"

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
