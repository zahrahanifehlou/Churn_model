# MLOp Approaches

# 1. What is MLOps?

MLOps = **Machine Learning Operations**.

It combines:

-   Machine Learning
-   Software Engineering
-   Data Engineering
-   DevOps
-   Cloud infrastructure
-   Automation
-   Monitoring

The goal is to make ML systems:

-   reproducible
-   deployable
-   monitorable
-   maintainable
-   scalable
-   continuously improvable

A model that works in a notebook is not necessarily a production ML
system.

MLOps helps move from:

``` text
"I trained a model"
```

to:

``` text
"I have a reliable ML system running in production,
and I can monitor, update, and retrain it."
```

------------------------------------------------------------------------

# 2.  ways to implement MLOps

There are several major approaches.

| Approach                       | Typical tools                                       | Where it runs         |
| ------------------------------ | --------------------------------------------------- | --------------------- |
| **Google Cloud**               | Vertex AI, BigQuery, Cloud Build, Artifact Registry | GCP                   |
| **AWS**                        | SageMaker, S3, ECR, CodePipeline, CloudWatch        | AWS                   |
| **Azure**                      | Azure Machine Learning, Azure DevOps, Blob Storage  | Azure                 |
| **Databricks**                 | MLflow, Unity Catalog, Databricks Workflows         | Databricks / cloud    |
| **Open-source / self-managed** | MLflow, Kubeflow, DVC, Airflow, Kubernetes          | Your infrastructure   |
| **Git-based MLOps**            | GitHub/GitLab + CI/CD + MLflow + Docker             | Cloud or on-premise   |
| **Hybrid**                     | MLflow + Kubernetes + cloud services                | Multiple environments |


------------------------------------------------------------------------

# 3. AWS MLOps example

AWS has its own ecosystem.

A simplified AWS MLOps architecture could be:

``` text
S3
 ↓
SageMaker Processing
 ↓
SageMaker Training
 ↓
SageMaker Model Registry
 ↓
SageMaker Endpoint
 ↓
CloudWatch
 ↓
SageMaker Pipelines
 ↓
Retraining
```

Here:

-   **S3** → stores data and artifacts
-   **SageMaker Processing** → data processing
-   **SageMaker Training** → model training
-   **SageMaker Model Registry** → model versioning and management
-   **SageMaker Endpoint** → model serving
-   **CloudWatch** → monitoring
-   **SageMaker Pipelines** → workflow automation

The concepts are very similar to Vertex AI.

------------------------------------------------------------------------

# 4. Open-source MLOps example

You can also build an MLOps platform using open-source tools.

For example:

``` text
Data
 ↓
DVC
 ↓
Python / PyTorch
 ↓
MLflow
 ↓
Docker
 ↓
Kubernetes
 ↓
Prometheus / Grafana
 ↓
Airflow / Kubeflow
 ↓
Retraining
```

Possible responsibilities:

-   **DVC** → dataset/version management
-   **Python / PyTorch** → model development
-   **MLflow** → experiment tracking and model registry
-   **Docker** → containerization
-   **Kubernetes** → deployment/orchestration
-   **Prometheus / Grafana** → monitoring
-   **Airflow / Kubeflow** → workflow orchestration

This approach gives you much more control, but you are responsible for
managing more infrastructure.

------------------------------------------------------------------------

# 5. The most important concept: learn MLOps concepts, not only tools

Do not think:

> "I need to learn Vertex AI, then I need to learn another MLOps tool."

Instead, learn the **MLOps concepts first**.

The tools are implementations of those concepts.

For example:

``` text
MLOps Concept
      ↓
Different implementations
      ↓
Vertex AI
AWS SageMaker
Azure ML
MLflow
Kubeflow
Databricks
etc.
```

Once you understand the concept, learning another platform becomes much
easier.

------------------------------------------------------------------------

# 6. MLOps concepts and their implementations

 | MLOps concept          | Vertex AI                  | Other implementations               |
| ---------------------- | -------------------------- | ----------------------------------- |
| Experiment tracking    | Vertex AI Experiments      | MLflow                              |
| Dataset management     | Vertex AI datasets / GCS   | DVC, S3, Azure Blob                 |
| Model registry         | Vertex AI Model Registry   | MLflow Registry, SageMaker Registry |
| Training               | Vertex AI Training         | SageMaker, Azure ML, Kubernetes     |
| Pipeline orchestration | Vertex AI Pipelines        | Kubeflow, Airflow, Dagster          |
| Deployment             | Vertex AI Endpoint         | Kubernetes, SageMaker Endpoint      |
| Monitoring             | Vertex AI Model Monitoring | Evidently, Prometheus, CloudWatch   |
| CI/CD                  | Cloud Build                | GitHub Actions, GitLab CI, Jenkins  |
| Containers             | Artifact Registry          | Docker + ECR/ACR/GCR                |
| Feature management     | Vertex AI Feature Store    | Feast, Databricks                   |

  -----------------------------------------------------------------------

The important point is:

**Same MLOps problem → different technology solutions.**

------------------------------------------------------------------------

# 7. Example: Model Registry

Suppose you train three versions of a model:

``` text
Model v1
Model v2
Model v3
```

You need to know:

-   Which dataset was used?
-   Which code version was used?
-   Which hyperparameters were used?
-   Which metrics did the model achieve?
-   Which model is currently in production?
-   Can we roll back to an older model?

This is the **model registry / model lifecycle management** problem.

Possible solutions:

``` text
Google Cloud → Vertex AI Model Registry

AWS → SageMaker Model Registry

Open source → MLflow Model Registry
```

The concept remains the same.

------------------------------------------------------------------------

# 8. Example: Experiment tracking

Imagine you run:

``` text
Experiment 1
learning_rate = 0.001
batch_size = 32
F1 = 0.81

Experiment 2
learning_rate = 0.0005
batch_size = 32
F1 = 0.84

Experiment 3
learning_rate = 0.0001
batch_size = 64
F1 = 0.86
```

You need a systematic way to record these experiments.

Possible tools:

``` text
Vertex AI Experiments
        OR
MLflow
        OR
Databricks MLflow
```

Again, the **MLOps concept is the same**.

------------------------------------------------------------------------

# 9. Example: Pipeline orchestration

A production ML workflow might contain:

``` text
Load data
   ↓
Validate data
   ↓
Transform data
   ↓
Train model
   ↓
Evaluate model
   ↓
Register model
   ↓
Deploy model
   ↓
Monitor model
```

You don't want a human manually executing every step.

You want an automated pipeline.

Possible technologies:

``` text
Vertex AI Pipelines
        OR
Kubeflow
        OR
Airflow
        OR
Dagster
```

------------------------------------------------------------------------

# 10. Example: Model monitoring

A model can perform well when you deploy it and become worse later.

For example:

``` text
Training data
      ↓
Model
      ↓
Production
      ↓
New real-world data
      ↓
Data distribution changes
      ↓
Model performance decreases
```

This is why production models need monitoring.

You may monitor:

-   prediction quality
-   data drift
-   feature distributions
-   missing values
-   latency
-   errors
-   resource usage
-   model behavior

Possible tools include:

``` text
Vertex AI Model Monitoring
CloudWatch
Evidently
Prometheus
Grafana
Datadog
```

------------------------------------------------------------------------

# 11. The MLOps lifecycle

A useful mental model is:

``` text
                  ┌──────────────┐
                  │     Data     │
                  └──────┬───────┘
                         ↓
                  ┌──────────────┐
                  │  Validation  │
                  └──────┬───────┘
                         ↓
                  ┌──────────────┐
                  │   Training   │
                  └──────┬───────┘
                         ↓
                  ┌──────────────┐
                  │  Evaluation  │
                  └──────┬───────┘
                         ↓
                  ┌──────────────┐
                  │Model Registry│
                  └──────┬───────┘
                         ↓
                  ┌──────────────┐
                  │  Deployment  │
                  └──────┬───────┘
                         ↓
                  ┌──────────────┐
                  │  Monitoring  │
                  └──────┬───────┘
                         ↓
                  ┌──────────────┐
                  │ New / Drift  │
                  │     Data     │
                  └──────┬───────┘
                         │
                         └──────────────→ Retraining
```

This lifecycle is much more important to understand than memorizing the
name of one platform.

------------------------------------------------------------------------

# 12. Three Important layers 

A strong learning strategy is to understand MLOps at three levels.

## Layer 1 --- MLOps concepts

Understand:

-   data versioning
-   experiment tracking
-   reproducibility
-   model versioning
-   model registry
-   model evaluation
-   CI/CD
-   model deployment
-   monitoring
-   drift detection
-   retraining
-   pipeline orchestration
-   governance

This knowledge is platform-independent.

------------------------------------------------------------------------

## Layer 2 --- One cloud implementation

Learn one cloud platform deeply enough to build real systems.

For example:

**Google Cloud + Vertex AI**

You can learn:

``` text
GCS
 ↓
Vertex AI
 ↓
Vertex AI Pipelines
 ↓
Vertex AI Experiments
 ↓
Vertex AI Model Registry
 ↓
Vertex AI Endpoint
 ↓
Vertex AI Monitoring
```

This gives you practical cloud MLOps experience.

------------------------------------------------------------------------

## Layer 3 --- Portable/open-source tools

Then learn tools that are not tied to one cloud provider.

A useful combination is:

``` text
MLflow
Docker
GitHub Actions
Kubernetes
DVC
```

This gives you more portability.

For example:

``` text
                    MLOps
                      │
          ┌───────────┼───────────┐
          ↓           ↓           ↓
       Cloud       Open Source   CI/CD
          │           │           │
     Vertex AI      MLflow     GitHub Actions
     SageMaker     Kubeflow    GitLab CI
     Azure ML      DVC         Jenkins
```

------------------------------------------------------------------------

# 13. Why this matters for an AI Engineer

If you only know:

``` text
Vertex AI
```

you know one platform.

If you understand:

``` text
MLOps concepts
        +
Vertex AI
        +
MLflow
        +
Docker
        +
CI/CD
```

you understand how production ML systems are actually built.

Then when you encounter:

``` text
SageMaker
Azure ML
Databricks
Kubeflow
```

you can map the new tools to concepts you already understand.



------------------------------------------------------------------------

# 14. Recommended learning direction

For an AI Engineer, a practical progression is:

``` text

                    MLOps
                      │
        ┌─────────────┴─────────────┐
        │                           │
   ML Foundations              Software/DevOps
        │                           │
        └─────────────┬─────────────┘
                      ↓
              1. ML Project Structure
                      ↓
              2. Data Management
                      ↓
              3. Experiment Tracking
                      ↓
              4. Model Versioning
                      ↓
              5. Reproducibility
                      ↓
              6. Model Evaluation
                      ↓
              7. CI/CD for ML
                      ↓
              8. Model Deployment
                      ↓
              9. Model Monitoring
                      ↓
             10. Model/Data Drift
                      ↓
             11. Model Registry
                      ↓
             12. Pipelines
                      ↓
             13. Cloud MLOps
                      ↓
             14. Kubernetes
                      ↓
             15. Production MLOps

```

The objective is not to memorize every tool.

The objective is to understand **how a machine learning model becomes a
reliable production system**.


| Project                    | What you learn             |
| -------------------------- | -------------------------- |
| **1. ML project**          | ML + Python + Git          |
| **2. Reproducible ML**     | Config + logging + testing |
| **3. Dataset versioning**  | DVC                        |
| **4. Experiment tracking** | MLflow                     |
| **5. Model registry**      | MLflow Registry            |
| **6. ML API**              | FastAPI                    |
| **7. Containerized ML**    | Docker                     |
| **8. CI/CD ML**            | GitHub Actions             |
| **9. Production ML**       | Monitoring + drift         |
| **10. Cloud MLOps**        | Vertex AI / AWS / Azure    |
