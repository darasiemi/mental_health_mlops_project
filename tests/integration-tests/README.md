Install deepdill as a development package
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