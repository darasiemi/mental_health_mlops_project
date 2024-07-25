In software development for the machine learning cycle, testing is a critical component to ensure that the code performs as expected and meets quality standards. I have explored employs two primary types of tests: Unit Tests and Integration Tests.

Unit Tests focus on individual components of the software, validating that each part works correctly in isolation. These tests are essential for verifying the functionality of specific modules or functions, ensuring they produce the expected output given certain inputs. I implemented 4 unit tests namely testing: base64 decoding, feature shape, prediction output being 0 or 1, and my lambda handler. 

Integration Tests, on the other hand, assess the interactions between different components of the system. They help verify that the integrated units function together as intended, highlighting issues that might arise when different parts of the system communicate and operate together. In this case, I have implemented an integration test to assess the lambda function and kinesis.

Both testing strategies are crucial for maintaining the reliability, efficiency, and overall quality of the software in our machine learning lifecycle. This section contains instructions on how to run the test

## Table of Contents
- [Unit tests](#unit-tests)
- [Integration tests](#integration-tests)

### Unit-tests

First, you need to select your Python interpreter which houses your dependencies. This can be done by `CMD+Shift+P` on VS Code(MacOS). Then enter the path `path-to-you-environment/bin/python`. 


To run pytest, cd to the unit-tests directory. The `--disable-warnings` to avoid warnings that clutter the terminal 
```bash
pytest model_test.py --disable-warnings
```
### Integration tests
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