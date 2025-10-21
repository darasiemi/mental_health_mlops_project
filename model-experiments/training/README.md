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

 Update 2025: A data leakage issue was observed, and fixed. However, since the experimentation built in 2024 was built using an Ubuntu VM on AWS, which has been since deleted, Docker with an Ubuntu base image was used to correct this. This is why Dockerfile is in the update `model-experiments/training` repository. The `model-experiments/training/stress_prediction_notebook.ipynb` notebook has been corrected to fix this. However, the code still follows for Ubuntu VM with comments. Also, other aspects of the project such as experiment tracking, orchestration are not yet updated. This repo was for educational purpose.

To build the app
```bash
 docker build -t ml-env .
```
 To run the app
 ```bash
 docker run -it --name training -p 8888:8888 -v "$PWD":/app -w /app ml-env \
  python -m notebook \
  --ServerApp.ip=0.0.0.0 \
  --ServerApp.root_dir=/app \
  --ServerApp.open_browser=False \
  --allow-root
 ```
