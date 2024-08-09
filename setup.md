To connect with remote host, edit the config and add the IP address of the EC2 instance
```bash
nano ~/.ssh/config
```
Then run this to sign in
```bash
ssh mlopszoomcamp
```

Note that you should create a folder `data` and download the train and test data to this directory in the parent directory (i.e `mental_health_mlops_project/data`). This is done in the `stress_prediction_notebook` under the `model/training` folder

To set Python path for the folder as a variable
```bash
export PYTHONPATH=$PYTHONPATH:~/mental_health_mlops_project
```

To run linting using pylint, first launch pipenv from the parent directory
```bash
pipenv shell
```
Then we rub pylint on particular directories (monitoring and deployment)
```bash
pylint --recursive=y monitoring deployment
```

However, it is not easy to fix the comments by pylint from this result. It is better to include Pylint in your code editor. For VS Code, you can run
`Cmd+Shift+P` and select linter as pylint.

Install development packages
```bash
pipenv install --dev isort black pytest pylint
```
The `pyproject.toml` contains the configuration for black. Also note that black was not configured for Jupyter notebooks in this project, so these are skipped.

To check changes to be made by black for the `monitoring` and `deployment` folders,
```bash
black --diff monitoring deployment
```

Likewise, to reformat
```bash
black monitoring deployment
```

To fix the import order,
```bash
isort [folder]
```

To create a pre-commit hook, run
```bash
pre-commit install
```

To check if this has been created, run
```bash
ls .git/hooks/
```
You will see pre-commit in the hooks

To use Makefile, run `make [target]`, e.g
```bash
make integration-test
```

To setup infrastructure using Terraform,[x].

To deploy manually, first run the deploy-manual script,(assuming you are in the `mental_health_mlops_project`)
```bash
./scripts/deploy-manual.sh
```

To add data to the kinesis stream. Note that we send encoded data because our actual data is multimodal with text and numerical features. I was unable to pass the raw data on the terminal without encoding
```bash
export KINESIS_STREAM_INPUT=stg_stress_events-mental-health-project
aws kinesis put-record \
    --stream-name ${KINESIS_STREAM_INPUT} \
    --partition-key 1 \
    --data 'ewogICAgInRleHQiOiAiSXRzIGxpa2UgdGhhdCwgaWYgeW91IHdhbnQgb3Igbm90LiBNRTogSSBoYXZlIG5vIHByb2JsZW0sIGlmIGl0IHRha2VzIGxvbmdlci4gQnV0IHlvdSBhc2tlZCBteSBmcmllbmQgZm9yIGhlbHAgYW5kIGxldCBoaW0gd2FpdCBmb3Igb25lIGhvdXIgYW5kIHRoZW4geW91IGhhdmVu4oCZdCBwcmVwYXJlZCBhbnl0aGluZy4gVGhhdHMgbm90IHdoYXQgeW91IGFza2VkIGZvci4gSW5zdGVhZCBvZiAzIGhvdXJzLCBoZSBoZWxwZWQgeW91IGZvciAxMCBob3VycyB0aWxsIDVhbS4uLiIsCiAgICAibGV4X2xpd2NfVG9uZSI6IDUuOTUsCiAgICAibGV4X2xpd2NfaSI6IDUuNDUsCiAgICAibGV4X2xpd2NfbmVnZW1vIjogMS44MiwKICAgICJsZXhfbGl3Y19DbG91dCI6IDU3LjIyLAogICAgInNlbnRpbWVudCI6IDAuMAp9'

```

This returns a shard-id if run successfully.

You can now check CloudWatch on AWS to confirm that the Lambda function was triggered and runs successfully.

To move files(a folder) from your local machine to the remote host, run
```bash
scp -r /localhost/path ubuntu@IP_address:remotehost/path
```
