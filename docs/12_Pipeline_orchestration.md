ML Pipelines

Now automate the entire workflow.

Instead of:

prepare data
↓
train
↓
evaluate
↓
register
↓
deploy

manually, create a pipeline:

        DATA
          ↓
     VALIDATION
          ↓
     PREPROCESSING
          ↓
       TRAINING
          ↓
      EVALUATION
          ↓
   QUALITY GATE
          ↓
    MODEL REGISTRY
          ↓
       DEPLOY
          ↓
      MONITOR

Tools to learn:

First

MLflow / simple Python pipelines

Then
Prefect
Airflow
Kubeflow
cloud-native pipelines

You don't need all of them.