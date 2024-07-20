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