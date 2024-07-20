First is to activate the conda environment
```bash
conda activate your_environment
```

To install dependencies
```bash
pip install -r requirements.txt 
```

To spin-up the container with grafana and others, run
```bash
docker-compose up --build
```

You also need to set your AWS credentials as environment variables
```bash
export AWS_ACCESS_KEY_ID=your_key_id
export AWS_SECRET_ACCESS_KEY=your_secret_access_key
```

Launch jupyter (i.e. `jupyter-notebook`) and run the notebook `monitoring/stress_prediction_monitoring.ipynb`
To launch evidently UI, run 
```bash
evidently ui
```

To log metrics to a database, run
```bash
python evidently_metrics_calculation.py
```
Then go to `localhost:8080` to check the database on Adminer. The System is `PostGresSQL`, username is `postgres`, database is `test` and password is `example`

Therefore, go to `localhost:3000` to access Grafana. Username is `admin` and password is also `admin`. You will be prompted to change your password and you can do so if you wish. Then create dashboard with `PostgreSQL` as datasource.