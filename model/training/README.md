First install pipenv
```bash
pip install pipenv
```
To install packages
```bash
pipenv install kaggle textblob xgboost wordcloud --python==3.11
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
scp ~/Downloads/kaggle.json ubuntu@51.20.254.178:~/mental_health_mlops_project
```

To setup s3, follow instructions in [x]
then

