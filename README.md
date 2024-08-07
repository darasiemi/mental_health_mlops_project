# mental_health_mlops_project

Note that you should create a folder `data` and download the train and test data to this directory in the parent directory (i.e `mental_health_mlops_project/data`). This is done in the `stress_prediction_notebook` under the `model/training` folder

To set Python path for the folder as a variable
```bash
export PYTHONPATH=$PYTHONPATH:~/mental_health_mlops_project
```


To run linting using pylint, first launch pipenv
```bash
pipenv shell
```
Then we rub pylint on particular folders (monitoring and deployment)
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


General Guidelines
- After spinning up a docker container, you can run `docker ps` to check information about running containers
- You can work with conda environment for development, but it's easier to use `pip environment` for containerization. If you want to maintain the environment using conda, you will need a `requirements.txt` file to pip install in your Dockerfile.
Future Works
- Creation of alerts and triggers for retraining in orchestration
- Logging of models with orchestration pipeline
- Store and load the data from S3
- Incorporation of the utils function into the deployment Python modules. However, this were left in this implementation to show different methods of loading the model and vectorizer artifacts (i.e. directly from S3 like in deployment scripts, and locally (already downloaded from S3) as in the `utils/model_loader.py`)
- Setting up alerts from Grafana for automatic retraining.
- Poetry for managing dependencies
- Making utils to load data from S3 instead of having to download it locally from S3 first before loading.
- CI/CD
- Interconnection of all modules. The methodology of going from week 1 module to week 6, caused that there were some modules that were sort of disconnect (e.g orchestration)
- Optimizing code to facilitate lower cloud costs.

To Do,
Fix path issues for model monitoring
