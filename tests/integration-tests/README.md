Install deepdiff as a development package
```bash
pipenv install --dev deepdiff
```

To download the model artifcat locally,
```bash
RUN_ID="57342ae687254eeeac28602bb8d42aca"
EXPERIMENT_ID=3
MODEL_BUCKET="mlflows-artifacts-remote"
aws s3 cp --recursive s3://$MODEL_BUCKET/$EXPERIMENT_ID/$RUN_ID/artifacts/model/ model
```

To download the vectorizer artifact locally,
```bash
aws s3 cp --recursive s3://$MODEL_BUCKET/$EXPERIMENT_ID/$RUN_ID/artifacts/vectorizer/ vectorizer
```
To make `run.sh` executable,
```bash
chmod +x run.sh
```
To build docker image,
```bash
docker build -t stream-model-stress:v2 .
```
To run docker container
```bash
docker run -it --rm \
    -p 8080:8080 \
    -e PREDICTIONS_STREAM_NAME="stress_predictions" \
    -e RUN_ID="57342ae687254eeeac28602bb8d42aca" \
    -e MODEL_LOCATION="/app/model" \
    -e TEST_RUN="True" \
    -e AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}" \
    -e AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}" \
    -e AWS_DEFAULT_REGION="eu-north-1" \
    -v $(pwd)/model:/app/model \
    stream-model-stress:v2
```

To check list of streams in localstack
```bash
aws --endpoint-url=http://localhost:4566 \
    kinesis list-streams
```

To create stream in localstack
```bash
aws --endpoint-url=http://localhost:4566 \
    kinesis create-stream \
    --stream-name stress_predictions \
    --shard-count 1
```

To get shard iterator from kinesis
```bash
export PREDICTIONS_STREAM_NAME="ride_predictions"
export SHARD='shardId-000000000000'
aws  --endpoint-url=http://localhost:4566 \
    kinesis     get-shard-iterator \
    --shard-id ${SHARD} \
    --shard-iterator-type TRIM_HORIZON \
    --stream-name ${PREDICTIONS_STREAM_NAME} \
    --query 'ShardIterator'
```

To get records
```bash
aws  --endpoint-url=http://localhost:4566 \
    kinesis     get-records \
    --shard-iterator "AAAAAAAAAAHebXZfJF+ip5pICTTimTJrH3nDHrcq2uvIwSBoiSV6mbmJGs7l7eHF6YjuDWcd83eV93YnlwBGhdDkNwFGVa6qibalZBwWhh3pPJUwlk/njd1c3tHhpXnBCLhkCLxFN0u6pi9xEGDdgNL16iOeGml6YvhxInhhEhJwgSi2kAG7XTqMZoDcl/4RUCzDRWGGmCwCSwzzbCJQJEV60vuGKVeV"
```
