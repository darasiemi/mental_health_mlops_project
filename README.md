# Mental Health Project: Stress Prediction Using Social Media Posts
Introduction
This is a final project for the Data Talks Club MLOps [Zoomcamp ](https://github.com/DataTalksClub/mlops-zoomcamp). In this project, I have implemented the end-to-end machine learning life cycle, including infrastructure provisioning using Terraform, modeling and experiment tracking using MLflow, orchestration with Mage, deployment using Flask, Lambda and Kinesis, monitoring with Evidently and Grafana, and best practices such as integration tests with localstark, unit testing, formatting, Makefile, pre-commit hooks etc.


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
- [Acknowledgement](#acknowledgement)
- [References](#references)

### Problem Statement
The World Health Organization defines mental health as a state of well-being that allows individuals to handle life’s stresses, realise their potential, learn effectively, work productively, and contribute to their community. This definition highlights stress as a potential trigger that must be managed. In contrast, the National Alliance on Mental Illness defines mental illness as conditions that impact a person's emotions, behaviour, thoughts, and mood, leading to a negative effect on their daily functioning[1]. Mental illnesses affect more than 1 billion people globally, with significant economic consequences [2]. Stress is recognized as one of the contributing factors to mental illness, underscoring the need for technological tools for longitudinal monitoring and care for managing stress and mental illnesses.

This project aims to predict stress using social media posts (text) combined with numerical tabular data. The project utilises data available on Kaggle. Traditional machine learning models and handcrafted features using a feature vectorizer have been explored. Due to the challenge of high dimensionality from numerous tabular features, mutual information (MI) was used to select the top 5 features based on MI. The choice of five features is arbitrary and intended for experimental purposes.

### Data
The dataset is publicly available online on [Kaggle](https://www.kaggle.com/datasets/ruchi798/stress-analysis-in-social-media). The training dataset information, as analysed on Mage is as thus:

![Dataset summary](images/mage_summary_overview.jpeg)

The final selected features which were used to train the model and make inference are:
|      Text         | lex_liwc_Tone  |   lex_liwc_i   |lex_liwc_negemo | lex_liwc_Clout | Sentiment|
|-------------------|----------------|----------------|----------------|----------------|----------|
| Social media posts|    float       |     float      |      float     |     float      |  float   |

### Experiment tracking
I explored using an EC2 instance as a tracking server for MLflow. This is to model a situation whereby there are different machine learning professionals in a company, who can easily view experiements run on Mlflow through the tracking server's public IP address. The model artificacts were also stored and can be retrieved from S3.

The notebooks used for experiment tracking can be found in `model-experiments/experiment_tracking`. There are two notebooks namely `stress_prediction_mlflow.ipynb` and `stress_prediction_hyperparameter.ipynb`. The former was used to explore different models and the Random Forest(RF) was shown to have the best performance. I also explored the use of stacked features (text and numerical data), and only text data, and I discovered that my model performed better using the stacked features. The stacked features and RF were then used for hyperparameter tuning, to get the best parameters. The model and vectorizer artifacts were then logged for the best performing model. Note that hyperopt was used for the hyperparameter tuning. Since this minimizes a loss, and the accuracy is intended to maximise, a negative accuracy was returned as the objective to be minimized.

Please not that for the experiment tracking, this was done outside orchestration. However, using Mage, I was able to load my model performance from MLflow. The plot of the model performances can be found as follows

![Model performance](images/mage_model_performance_plot.jpeg)

### Orchestration

### Deployment

### Monitoring

### Infrastructure

### Best Practices

### General Guidelines
- After spinning up a docker container, you can run `docker ps` to check information about running containers
- You can work with conda environment for development, but it's easier to use `pip environment` for containerization. If you want to maintain the environment using conda, you will need a `requirements.txt` file to pip install in your Dockerfile.
- Please note that the tracking server changes from time to time based on the current running public IP address of the EC2 instance.

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
To run the model experiments, follow the instructions for model training [here](model-experiments/training/README.md)
Intructions on how to set up environment for experiment tracking can be found [here](model-experiments/experiment_tracking/README.md)

### Acknowledgement

### References

[1]	E. H. Rosado-Solomon, J. Koopmann, W. Lee, and M. A. Cronin, “Mental Health and Mental Illness in Organizations: A Review, Comparison, and Extension,” Acad. Manag. Ann., vol. 17, no. 2, pp. 751–797, Jul. 2023, doi: 10.5465/annals.2021.0211.

[2]	J. Blair, J. Brozena, M. Matthews, T. Richardson, and S. Abdullah, “Financial technologies (FinTech) for mental health: The potential of objective financial data to better understand the relationships between financial behavior and mental health,” Front. Psychiatry, vol. 13, 2022, Accessed: Jan. 08, 2024. [Online]. Available: https://www.frontiersin.org/articles/10.3389/fpsyt.2022.810057

[3]	Y.-C. Shin, D. Lee, J. Seol, and S.-W. Lim, “What Kind of Stress Is Associated with Depression, Anxiety and Suicidal Ideation in Korean Employees?,” J. Korean Med. Sci., vol. 32, no. 5, pp. 843–849, May 2017, doi: 10.3346/jkms.2017.32.5.843.
