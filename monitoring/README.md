First is to activate the conda environment
```bash
conda activate your_environment
```

To install dependencies
```bash
pip install -r requirements.txt 
```

To spin-up the container with grafana and others, run in the `monitoring` folder
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
Note that in the `evidently_metrics_calculation.py`, we consider a batch backfill, where we parse the test data, 5 rows at a time. We then log the data starting from January 2024 and incrementing daily(hypothetically).

Then go to `localhost:8080` to check the database on Adminer. The System is `PostGresSQL`, username is `postgres`, database is `test` and password is `example`. You will see the data being inputed to our database.

Therefore, go to `localhost:3000` to access Grafana. Username is `admin` and password is also `admin`. You will be prompted to change your password and you can do so if you wish. Then create dashboard with `NewPostgreSQL` as datasource.

The query type should be on `Builder` by default, so you should change the query to `Code`. Then input this query and run it
```sql
SELECT timestamp, prediction_drift FROM metrics_table;
```

This is to plot the timestamp and prediction drift as appropriate. You are free to write your own SQL query as appropriate.

If you are running on a VM, ensure that you forward the ports if not autoforwarded.