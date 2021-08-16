import mlflow

with mlflow.start_run() as run:
    mlflow.log_param("p", 0)
print(run.info.status)
