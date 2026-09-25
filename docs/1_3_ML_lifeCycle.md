

# MLOps — ML Lifecycle

The machine learning lifecycle can be divided into three main phases:

```text
Discovery
   ↓
Development
   ↓
Deployment
   ↓
Monitoring & Maintenance
   ↺
```

MLOps practices support all three phases, not only deployment.

---

# 1. Discovery Phase

## Goal

Determine **what problem should be solved, whether ML is appropriate, and what is required to build the solution**.

The discovery phase connects the **business problem** to a potential ML solution.

---

## Main Activities

### 1.1 Define the Business Use Case

First, understand:

* What problem are we solving?
* Who are the users?
* What decision will the model support?
* What is the expected business impact?
* How will success be measured?

Example:

```text
Business Problem
      ↓
Customer support is too slow
      ↓
Potential ML solution
      ↓
Automatically classify support requests
```

The important point is:

> Start with the problem, not with the model.

---

### 1.2 Understand the Users and Context

The model must operate within a real-world workflow.

Questions include:

* Who will use the predictions?
* How will predictions be consumed?
* What happens when the model is uncertain?
* What are the consequences of an incorrect prediction?
* What latency is acceptable?

A technically accurate model may still be unsuitable if it does not fit the user's workflow.

---

### 1.3 Assess ML Feasibility

Before building the system, determine whether machine learning is actually appropriate.

Consider:

* Is sufficient data available?
* Is the target variable measurable?
* Is the problem predictable?
* Are labels available?
* Is the expected performance useful?
* Are there regulatory or operational constraints?

```text
Business Problem
      ↓
Is ML appropriate?
      ↓
 ┌────┴────┐
 No        Yes
 ↓          ↓
Other     Continue
solution  discovery
```

---

### 1.4 Data Accessibility

Determine:

* Where is the data?
* Who owns it?
* Can it legally be used?
* How much data is available?
* Is the data representative?
* How frequently is it updated?
* What is its quality?

Data availability is often a major constraint on ML projects.

---

### 1.5 Dataset Selection

Potential datasets need to be evaluated based on:

* Relevance
* Quality
* Coverage
* Size
* Labels
* Bias
* Freshness
* Accessibility

The selected dataset becomes one of the foundations of the ML system.

---

### 1.6 Model Architecture and Algorithm Selection

At this stage, identify an appropriate technical approach.

For example:

```text
Problem
   ↓
Classification?
Regression?
Ranking?
Generation?
Detection?
   ↓
Candidate algorithms
   ↓
Architecture selection
```

The choice depends on:

* Problem type
* Dataset
* Performance requirements
* Computational resources
* Latency requirements
* Interpretability requirements

---

# 2. Development Phase

## Goal

Build, train, evaluate, and iteratively improve the ML system.

The development phase usually includes:

```text
Data
 ↓
Data Pipeline
 ↓
Feature Engineering
 ↓
Model Training
 ↓
Evaluation
 ↓
Iteration
 ↺
```

---

# 3. Data Pipeline

The first major engineering task is preparing reliable data pipelines.

A typical pipeline:

```text
Raw Data
   ↓
Ingestion
   ↓
Validation
   ↓
Cleaning
   ↓
Transformation
   ↓
Features
   ↓
Training Dataset
```

The pipeline should ideally be:

* Reproducible
* Automated
* Testable
* Versioned
* Monitorable

---

# 4. Feature Engineering

Feature engineering transforms raw data into useful model inputs.

Example:

```text
Raw customer data
       ↓
Age
Transaction history
Account activity
       ↓
Engineered features
       ↓
ML model
```

Feature engineering can have a significant effect on model performance.

For modern deep learning systems, feature engineering may be reduced or replaced by learned representations, but data preparation and representation choices remain important.

---

# 5. Model Development

Models are developed iteratively.

A simplified workflow:

```text
Train Model
    ↓
Evaluate
    ↓
Analyze Results
    ↓
Change
 ┌──┴───────────────┐
 │                  │
Data            Algorithm
 │                  │
Features        Architecture
 │                  │
 └────────┬─────────┘
          ↓
      Train Again
```

The team may revisit:

* The original use case
* Dataset selection
* Features
* Algorithms
* Model architecture
* Hyperparameters

This iteration is a normal part of ML development.

---

# 6. Development Is Not Always Linear

A common misconception is:

```text
Data → Model → Deployment
```

In reality, ML development is iterative:

```text
        ┌───────────────┐
        ↓               │
      Data → Model → Evaluation
        ↑               │
        └───────────────┘
```

Poor model performance may indicate that:

* The data is insufficient
* The problem was poorly defined
* Features are inadequate
* The algorithm is inappropriate
* The target is difficult to predict

Therefore, teams may return to the **discovery phase** and reconsider the original assumptions.

---

# 7. Deployment Phase

## Goal

Make the validated ML model available for real-world use and operate it reliably.

Deployment involves more than simply saving a model file.

The system must answer:

* Where will the model run?
* How will users access it?
* How much traffic must it handle?
* How will it scale?
* How will it be monitored?
* How will it be updated?

---

# 8. Deployment Planning

### Hosting

Possible hosting environments include:

* Cloud platforms
* On-premise infrastructure
* Edge devices
* Managed ML platforms
* Containers / Kubernetes

The choice depends on:

* Cost
* Latency
* Security
* Compliance
* Scalability
* Infrastructure requirements

---

## Scaling

The deployment architecture must handle expected workload.

For example:

```text
Users
  ↓
API
  ↓
Load Balancer
  ↓
Model Serving
  ↓
Model
```

As traffic increases, additional serving instances may be required.

---

# 9. Operationalizing the Model

Operationalization means integrating the model into a reliable production system.

A simplified production architecture:

```text
Data
 ↓
Data Pipeline
 ↓
Model
 ↓
Model Serving
 ↓
Application
 ↓
Users
```

But production does not end at deployment.

The system must continuously be observed.

---

# 10. Model Monitoring

After deployment, monitor both the **system** and the **ML behavior**.

### System metrics

Examples:

* Latency
* Throughput
* CPU/GPU usage
* Memory
* Error rate
* Availability

### ML metrics

Examples:

* Prediction distribution
* Accuracy, when labels become available
* Precision / Recall
* Business KPIs
* Data quality
* Data drift
* Model drift

---

# 11. Data Drift

**Data drift** occurs when the distribution of input data changes over time.

Example:

```text
Training Data
     ↓
Age distribution:
20–40 years
```

Later:

```text
Production Data
     ↓
Age distribution:
40–70 years
```

The production data no longer resembles the training data.

This can affect model performance.

---

# 12. Model Maintenance

A production model may need to be updated when:

* Data changes
* Performance decreases
* Business requirements change
* New training data becomes available
* The model becomes outdated
* The underlying environment changes

This creates a continuous lifecycle:

```text
Deploy
  ↓
Monitor
  ↓
Detect Problem / New Data
  ↓
Retrain
  ↓
Evaluate
  ↓
Deploy New Version
  ↺
```

---

# 13. MLOps Across the Three Phases

| Phase           | Main ML Activities                                            | MLOps Concerns                                               |
| --------------- | ------------------------------------------------------------- | ------------------------------------------------------------ |
| **Discovery**   | Define use case, assess feasibility, select data and approach | Data accessibility, requirements, constraints                |
| **Development** | Data pipelines, features, training, evaluation                | Versioning, experiment tracking, reproducibility, automation |
| **Deployment**  | Hosting, serving, scaling                                     | CI/CD, infrastructure, monitoring, model registry            |
| **Maintenance** | Monitoring, retraining, updating                              | Drift detection, continuous training, model lifecycle        |

---

# 14. Key Mental Model

Think of the lifecycle as:

```text
┌──────────────────────────────────────────┐
│              DISCOVERY                   │
│                                          │
│ Business problem                         │
│ Users + context                          │
│ ML feasibility                           │
│ Data availability                        │
│ Dataset + algorithm selection            │
└──────────────────┬───────────────────────┘
                   ↓
┌──────────────────────────────────────────┐
│             DEVELOPMENT                  │
│                                          │
│ Data pipelines                           │
│ Feature engineering                      │
│ Model training                           │
│ Evaluation                               │
│ Experimentation                          │
│ Iteration                                │
└──────────────────┬───────────────────────┘
                   ↓
┌──────────────────────────────────────────┐
│              DEPLOYMENT                  │
│                                          │
│ Hosting                                  │
│ Scaling                                  │
│ Model serving                            │
│ Monitoring                               │
│ Drift detection                          │
│ Maintenance / Retraining                 │
└──────────────────┬───────────────────────┘
                   │
                   └──────────→ Iterate
```

## Core Idea

**MLOps is a lifecycle discipline.**

It begins before model training with **problem and data discovery**, continues through **reproducible model development**, and extends after deployment through **monitoring, maintenance, and retraining**.

The important shift in mindset is:

> **An ML model is not the final product. The production ML system and its lifecycle are the product.**
