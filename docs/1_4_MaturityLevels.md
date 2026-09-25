# MLOps — Maturity Levels and ML Model Delivery

## 1. Overview

MLOps maturity describes how an organization evolves from **manual ML workflows** to **automated, repeatable, and continuously monitored ML systems**.

A simplified progression:

```text
Level 0
Manual ML
   ↓
Level 1
Automated Training
   ↓
Level 2
Full MLOps Automation
```

The main progression is:

> **Manual → Automated Training → Automated CI/CD + Continuous Operations**

---

# 2. ML Model Delivery Process

A typical ML model delivery workflow contains:

```text
Data Extraction
      ↓
Data Analysis
      ↓
Data Preparation
      ↓
Model Training
      ↓
Model Evaluation
      ↓
Model Validation
      ↓
Model Serving
      ↓
Monitoring
```

At low maturity, these steps may be performed manually.

At higher maturity, they are implemented as automated pipelines.

---

# 3. Level 0 — Manual Process

## Characteristics

Level 0 is mostly manual and script-driven.

A typical workflow might look like:

```text
Data
 ↓
Notebook / Scripts
 ↓
Training
 ↓
Evaluation
 ↓
Manual Model Deployment
 ↓
Manual Monitoring
```

There is usually:

* No automated CI
* No automated CD
* Limited pipeline automation
* Interactive development
* Manual model deployment
* Limited production monitoring
* Manual retraining

---

## Example

A data scientist might:

1. Download data
2. Open a notebook
3. Clean the data
4. Train a model
5. Change hyperparameters
6. Train again
7. Save the model
8. Manually deploy it

This can work for experimentation but becomes difficult to manage at production scale.

---

# 4. Level 1 — Automated ML Pipeline

Level 1 introduces **pipeline automation and continuous training**.

The workflow becomes:

```text
New Data
   ↓
Data Validation
   ↓
Data Preparation
   ↓
Training
   ↓
Evaluation
   ↓
Model Validation
   ↓
Model Deployment
```

The important difference is that the ML training process is now automated.

---

## Level 1 Characteristics

### Continuous Training

New data can trigger retraining:

```text
New Data
   ↓
Training Pipeline
   ↓
New Model
   ↓
Evaluation
   ↓
Deployment
```

### Data Validation

The pipeline checks whether the data is suitable for training.

### Model Validation

The newly trained model is checked before deployment.

### Modularized Code

Instead of putting everything in one notebook:

```text
notebook.ipynb
```

the system is divided into reusable components:

```text
data/
training/
evaluation/
validation/
deployment/
```

This makes automation and testing easier.

### Continuous Deployment

A validated model can be automatically deployed to the serving environment.

---

# 5. Level 2 — Full MLOps Automation

Level 2 adds automation around the **entire ML development and delivery lifecycle**.

A simplified architecture:

```text
Source Control
      ↓
Continuous Integration
      ↓
Testing
      ↓
Build
      ↓
Training Pipeline
      ↓
Model Validation
      ↓
Model Registry
      ↓
Continuous Deployment
      ↓
Model Serving
      ↓
Monitoring
```

This is where MLOps becomes a complete operational system rather than just an automated training pipeline.

---

# 6. Level 2 Components

Level 2 typically includes:

### Source Control

Stores and versions:

* Code
* Configuration
* Pipeline definitions

---

### Continuous Integration — CI

Automatically:

```text
Code Change
    ↓
Build
    ↓
Tests
    ↓
Validation
```

The goal is to detect problems before changes enter production workflows.

---

### Continuous Delivery / Deployment

Validated artifacts are automatically delivered or deployed.

```text
Validated Artifact
       ↓
Deployment Pipeline
       ↓
Production
```

---

### Model Registry

A model registry stores and manages model versions.

Example:

```text
Model v1 → Production
Model v2 → Validation
Model v3 → Development
```

This provides a controlled way to manage model lifecycle and deployment.

---

### Metadata Management

ML systems generate metadata about:

* Datasets
* Training runs
* Models
* Parameters
* Metrics
* Pipeline executions
* Artifacts

Metadata allows teams to understand how a model was produced.

---

# 7. Continuous Integration vs Continuous Training vs Continuous Delivery

These concepts should not be confused.

| Concept        | What it automates                        |
| -------------- | ---------------------------------------- |
| **CI**         | Building and testing code                |
| **CT**         | Training models using new data           |
| **CD**         | Delivering/deploying validated artifacts |
| **Monitoring** | Observing production behavior            |

Together:

```text
Code
 ↓
CI
 ↓
Training
 ↓
CT
 ↓
Validation
 ↓
CD
 ↓
Production
 ↓
Monitoring
```

---

# 8. Automated Pipeline Triggering

A mature MLOps system can automatically trigger pipelines.

Possible triggers include:

```text
Code Change
     ↓
CI Pipeline
```

or:

```text
New Data
     ↓
Training Pipeline
```

or:

```text
Model Performance Degradation
     ↓
Retraining / Investigation
```

The exact trigger depends on the system architecture.

---

# 9. Model Delivery

Model delivery means making the trained model available to generate predictions.

```text
Trained Model
      ↓
Model Deployment
      ↓
Model Serving
      ↓
Prediction Request
      ↓
Prediction Response
```

For example:

```text
Application
    ↓
API Request
    ↓
Model Endpoint
    ↓
Prediction
    ↓
Application
```

---

# 10. Monitoring

Monitoring is essential after deployment.

A production ML system should collect information about:

### System performance

* Latency
* Errors
* Resource usage
* Availability
* Throughput

### ML performance

* Prediction quality
* Data distribution
* Feature behavior
* Data drift
* Model performance

```text
Production Model
      ↓
Monitoring
      ↓
Metrics
      ↓
Detect Issues
      ↓
Retraining / Update
```

---

# 11. MLOps Maturity Comparison

| Capability          | Level 0        | Level 1                    | Level 2            |
| ------------------- | -------------- | -------------------------- | ------------------ |
| Data preparation    | Manual         | Automated                  | Automated          |
| Model training      | Manual         | Automated pipeline         | Automated pipeline |
| Data validation     | Limited/manual | Automated                  | Automated          |
| Model validation    | Manual         | Automated                  | Automated          |
| CI                  | No             | Limited                    | Yes                |
| CD                  | No             | Automated model deployment | Automated          |
| Continuous Training | No             | Yes                        | Yes                |
| Source control      | Basic          | Yes                        | Yes                |
| Model registry      | Usually no     | Possible                   | Yes                |
| Metadata            | Limited        | Some                       | Systematic         |
| Monitoring          | Limited        | Automated                  | Continuous         |
| Pipeline automation | Low            | High                       | End-to-end         |

---

# 12. Google Cloud Tools for MLOps

The course introduces Google Cloud services that can support different parts of the MLOps lifecycle.

> **Important:** These are course-specific Google Cloud tools. The underlying MLOps concepts are vendor-independent.

| MLOps Function     | Google Cloud Tool          |
| ------------------ | -------------------------- |
| Feature management | Vertex AI Feature Store    |
| Development        | Vertex AI Workbench        |
| Source control     | Cloud Source Repositories  |
| CI / Build         | Cloud Build                |
| Artifact storage   | Artifact Registry          |
| ML pipelines       | Vertex AI Pipelines        |
| Model management   | Vertex AI Model Registry   |
| Metadata           | ML Metadata                |
| Model serving      | Vertex AI Prediction       |
| Data / logs        | BigQuery                   |
| Model monitoring   | Vertex AI Model Monitoring |
| Explainability     | Vertex Explainable AI      |

---

# 13. Google Cloud MLOps Architecture

A simplified architecture from development to production:

```text
                    Source Code
                        │
                        ▼
                Cloud Source Repositories
                        │
                        ▼
                    Cloud Build
                        │
                        ▼
                Vertex AI Pipelines
                        │
              ┌─────────┴─────────┐
              ↓                   ↓
          Data / Features      Training
              │                   │
              └─────────┬─────────┘
                        ↓
                   Model Validation
                        ↓
                 Vertex AI Model Registry
                        ↓
                 Vertex AI Prediction
                        ↓
                    Production
                        ↓
             Model Monitoring
                        ↓
                     BigQuery
```

---

# 14. Where the Tools Fit

### Development

```text
Vertex AI Workbench
```

Used as a development environment for ML experimentation.

### Code

```text
Cloud Source Repositories
```

Used for source-code management in the course's Google Cloud workflow.

### Build / CI

```text
Cloud Build
```

Used to automate build and operationalization tasks.

### Pipeline

```text
Vertex AI Pipelines
```

Used to orchestrate ML workflows.

### Artifacts

```text
Artifact Registry
```

Used to store artifacts such as pipeline components and container images.

### Models

```text
Vertex AI Model Registry
```

Used to manage model versions and lifecycle.

### Serving

```text
Vertex AI Prediction
```

Used to serve models for predictions.

### Monitoring

```text
Vertex AI Model Monitoring
```

Used to monitor production ML behavior.

### Explainability

```text
Vertex Explainable AI
```

Provides explainability capabilities for supported ML models.

---

# 15. The Main MLOps Evolution

The most important thing to remember from this lecture is the progression:

```text
LEVEL 0
────────────────────────
Manual
Interactive
Script-driven
No CI/CD
Limited monitoring


          ↓


LEVEL 1
────────────────────────
Automated Training
Data Validation
Model Validation
Modular Pipelines
Continuous Training
Automated Model Deployment


          ↓


LEVEL 2
────────────────────────
Source Control
       +
CI
       +
Automated Testing
       +
Continuous Training
       +
Model Registry
       +
Metadata
       +
CD
       +
Serving
       +
Monitoring
```

---

# 16. Mental Model

Think of MLOps maturity as **increasing automation and control**.

```text
             MATURITY
                ↑
                │
      LEVEL 2   │  Full MLOps
                │  CI + CT + CD
                │  Registry + Metadata
                │  Monitoring
                │
      LEVEL 1   │  Automated ML
                │  Pipelines + CT
                │  Validation
                │
      LEVEL 0   │  Manual ML
                │  Notebooks + Scripts
                │
                └────────────────────→
                       Automation
```

## Core Takeaway

**MLOps maturity is not simply about using more tools.**

It is about progressively making the ML lifecycle:

* **Reproducible**
* **Automated**
* **Testable**
* **Versioned**
* **Deployable**
* **Monitorable**
* **Maintainable**

The ultimate goal is to move from:

> **"A data scientist trained a model."**

to:

> **"An automated system can reliably build, validate, deploy, serve, monitor, and update ML models."**
