To create environment
```bash
conda create -n exp-tracking-env
```
To activate environment
```bash
conda activate exp-tracking-env
```
To install packages
```bash
pip install -r requirements.txt
```

To launch tracking server
```bash
mlflow server -h 0.0.0.0 -p 5000 --backend-store-uri postgresql://postgres:9QqTxeByefYq50DlZP8U@mlflow-database.cfka4w20im4d.eu-north-1.rds.amazonaws.com:5432/mlflow_db --default-artifact-root s3://mlflows-artifacts-remote```
