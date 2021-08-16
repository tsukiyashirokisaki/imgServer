from mlflow.tracking import MlflowClient
client = MlflowClient()
run = client.get_run("c1e381dd8daf4496b2246cee574412b9")
# Show newly created run metadata info
print("Run tags: {}".format(run.data.tags))
print("Experiment id: {}".format(run.info.experiment_id))
print("Run id: {}".format(run.info.run_id))
print("lifecycle_stage: {}".format(run.info.lifecycle_stage))
print("status: {}".format(run.info.status))