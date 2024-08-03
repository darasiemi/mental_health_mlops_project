# mental_health_mlops_project

Note that you should create a folder `data` and download the train and test data to this directory in the parent directory (i.e `mental_health_mlops_project/data`). This is done in the `stress_prediction_notebook` under the `model/training` folder

To set Python path for the folder as a variable
```bash
export PYTHONPATH=$PYTHONPATH:~/mental_health_mlops_project
```


To run linting using pylint, first launch pipenv
```
pipenv shell
```
Then run
```bash
pylint --recursive=y .
```
You can also run for particular folders
```bash
pylint --recursive=y  monitoring
```
```bash
pylint --recursive=y  deployment
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
black --diff monitoring
```

```bash
black --diff deployment
```

Likewise, to reformat
```bash
black monitoring
```

```bash
black deployment
```

To fix the import order,
```bash
isort [folder]
```


 


General Guidelines
- After spinning up a docker container, you can run `docker ps` to check information about running containers
- You can work with conda environment for development, but it's easier to use `pip environment` for containerization. If you want to maintain the environment using conda, you will need a `requirements.txt` file to pip install in your Dockerfile.
Future Works
- Creation of alerts and triggers for retraining in orchestration
- Logging of models with orchestration pipeline
- Interconnection of all modules. The methodology of going from week 1 module to week 6, caused that there were some modules that were sort of disconnect (e.g orchestration) 
- Loading data from S3
- Setting up alerts from Grafana for automatic retraining.
- Poetry for managing dependencies