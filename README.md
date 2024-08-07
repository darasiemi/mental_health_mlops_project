# Mental Health Project: Stress Prediction Using Multimodal Input
Introduction


## Table of Contents
- [Problem Statement](#problem-statement)
- [Data](#data)
- [Experiment Tracking](#experiment-tracking)
- [Orchestration](#orchestration)
- [Data](#data)
- [Deployment](#deployment)
- [Monitoring](#monitoring)
- [infrastructure](#Infrastructure)
- [Best Practices](#best-practices)
- [General Guidelines](#best-practices)
- [Future Works](#future-works)
- [Setup](#setup)

### Problem Statement

### Data

### Experiment tracking

### Orchestration

### Deployment

### Monitoring

### Infrastructure

### Best Practices

### General Guidelines
- After spinning up a docker container, you can run `docker ps` to check information about running containers
- You can work with conda environment for development, but it's easier to use `pip environment` for containerization. If you want to maintain the environment using conda, you will need a `requirements.txt` file to pip install in your Dockerfile.

### Future Works
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

### Setup
