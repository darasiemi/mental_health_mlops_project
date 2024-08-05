First install pipenv
```bash
pip install pipenv
```
To install packages
```bash
pipenv install kaggle xgboost mlflow boto3 --python==3.11
```
To launch pipenv shell
```bash
pipenv shell
```
To run jupyter notebook in pipenv
```bash
pipenv run jupyter notebook
```
Generate API key from Kaggle and copy to remote machine
```bash
scp ~/Downloads/kaggle.json ubuntu@16.16.187.168:~/mental_health_mlops_project
```

 ls /home/ubuntu/anaconda3/bin/python3.11
