First, you need to select your Python interpreter which houses your dependencies. This can be done by `CMD+Shift+P` on VS Code(MacOS). Then enter the path `path-to-you-environment/bin/python`. 


To run pytest, cd to the unit-tests directory. The `--disable-warnings` to avoid warnings that clutter the terminal 
```bash
pytest model_test.py --disable-warnings
```

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
To run integraton test, cd to `tests/integration-tests` and run the command
```bash
./run.sh
```

If you get a No Credentials error, export your AWS credentials
```bash
export AWS_ACCESS_KEY_ID=your_access_key_id
export AWS_SECRET_ACCESS_KEY=your_secret_access_key
```