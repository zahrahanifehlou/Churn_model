# MLOps — Introduction & Role of ML Practitioners

## 1. Overview

MLOps is the set of practices used to **develop, deploy, monitor, and maintain machine learning systems in production**.

Machine learning in production is more than training a model. It requires managing:

* Data
* Code
* Models
* Experiments
* Parameters
* Metrics
* Infrastructure
* Deployment
* Monitoring
* Collaboration

The goal of MLOps is to make ML systems **reproducible, reliable, scalable, and maintainable**.

---

## 2. Who Are ML Practitioners?

**ML practitioners** are the people involved in different stages of the machine learning lifecycle.

Typical roles include:

| Role              | Main contribution                                             |
| ----------------- | ------------------------------------------------------------- |
| Product Manager   | Defines the business problem and requirements                 |
| Data Scientist    | Explores data, develops features, trains and evaluates models |
| ML Engineer       | Builds production ML systems and deployment pipelines         |
| Data Engineer     | Builds and maintains data pipelines                           |
| Software Engineer | Develops reliable software around ML systems                  |
| MLOps Engineer    | Automates, deploys, monitors, and maintains ML workflows      |

These roles often work together rather than operating independently.

### ML Lifecycle

A simplified ML lifecycle is:

```text
Business Problem
      ↓
Data Collection
      ↓
Data Preparation
      ↓
Experimentation
      ↓
Model Training
      ↓
Model Validation
      ↓
Deployment
      ↓
Monitoring
      ↓
Retraining / Updating
      ↺
```

---

# 3. Challenges of Operationalizing ML Models

Training a model in a notebook is relatively easy compared with maintaining it in production.

An ML system contains many moving parts:

```text
Data
  +
Code
  +
Features
  +
Model Architecture
  +
Hyperparameters
  +
Training Environment
  +
Model Version
  +
Evaluation Metrics
```

All of these can change over time.

## Common Challenges

### 3.1 Data Management

Questions that need to be answered:

* Which dataset was used?
* Which version of the dataset?
* How was the data cleaned?
* Which features were used?
* Did the data change after deployment?

---

### 3.2 Experiment Tracking

During experimentation, practitioners may change:

* Model architecture
* Learning rate
* Batch size
* Number of epochs
* Optimizer
* Features
* Dataset version
* Random seed

Without tracking these changes, it becomes difficult to determine **why one experiment performed better than another**.

---

### 3.3 Model Versioning

A production system should know exactly which model is deployed.

For example:

```text
Model v1
Model v2
Model v3
```

We should be able to answer:

> Which model generated this prediction?

---

### 3.4 Collaboration

ML projects involve multiple people and teams.

Without proper versioning and tracking, teams can have problems such as:

* Different datasets
* Different model versions
* Different environments
* Untracked experiments
* Reproducing someone else's results

---

# 4. Reproducibility

## What is reproducibility?

**Reproducibility means being able to recreate an ML experiment or result using the same inputs, code, configuration, and environment.**

For example:

```text
Dataset v1
+
Code commit abc123
+
Config v5
+
Random seed 42
+
Model architecture
+
Training parameters
        ↓
Same experiment
        ↓
Comparable result
```

A reproducible ML system should track important information such as:

* Dataset version
* Source code version
* Model version
* Hyperparameters
* Configuration
* Random seed
* Training environment
* Evaluation metrics

## Why is reproducibility important?

Reproducibility helps with:

* Debugging
* Experiment comparison
* Collaboration
* Model deployment
* Auditing
* Compliance
* Retraining
* Investigating production problems

A model that cannot be reproduced is difficult to trust and maintain.

---

# 5. Automation

Manual ML workflows become difficult to maintain as projects grow.

For example, manually performing:

```text
Download data
    ↓
Clean data
    ↓
Train model
    ↓
Evaluate model
    ↓
Save model
    ↓
Deploy model
```

can lead to:

* Human errors
* Inconsistent environments
* Repeated manual work
* Difficult-to-reproduce results
* Slow model updates

MLOps aims to automate these processes.

---

## 6. ML Pipelines

A typical automated ML pipeline might look like:

```text
Data Ingestion
      ↓
Data Validation
      ↓
Data Preprocessing
      ↓
Feature Engineering
      ↓
Model Training
      ↓
Model Evaluation
      ↓
Model Validation
      ↓
Model Deployment
      ↓
Monitoring
```

Automation allows the pipeline to be executed consistently.

It can also support **regular model updates when new data becomes available**.

---

# 7. Reproducibility + Automation

These two concepts are fundamental to MLOps.

### Reproducibility

Answers:

> **Can I recreate what happened?**

### Automation

Answers:

> **Can the process happen consistently without manually repeating every step?**

Together:

```text
Reproducibility
      +
Automation
      ↓
Reliable ML Operations
      ↓
Production ML Systems
```

---

# 8. Key Takeaways

### ML practitioners

ML involves multiple roles, including:

* Product managers
* Data scientists
* ML engineers
* Data engineers
* Software engineers
* MLOps engineers

### Operationalizing ML

Production ML requires managing much more than the model itself:

* Data
* Code
* Experiments
* Parameters
* Models
* Infrastructure
* Deployment
* Monitoring

### Reproducibility

We should be able to determine:

> **What was trained, with which data, using which code and parameters, and how did it perform?**

### Automation

Automated pipelines help:

* Reduce manual errors
* Improve consistency
* Accelerate deployment
* Support continuous retraining
* Make ML systems easier to maintain

---

# 9. Mental Model

The main idea to remember:

```text
        DEVELOPMENT
             ↓
     Experimentation
             ↓
       Reproducibility
             ↓
        Automation
             ↓
        DEPLOYMENT
             ↓
        Monitoring
             ↓
      Continuous Update
             ↺
```

**MLOps bridges the gap between building an ML model and operating an ML system reliably in production.**
