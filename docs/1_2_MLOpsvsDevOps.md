# MLOps vs DevOps and ML-Specific Challenges

## 1. What is MLOps?

**MLOps (Machine Learning Operations)** applies software engineering and **DevOps principles** to machine learning systems.

The objective is to manage the complete ML lifecycle efficiently:

* Resources
* Data
* Code
* Models
* Experiments
* Time
* Quality
* Deployment
* Monitoring
* Retraining

A useful mental model:

```text
DevOps
Software Development
        +
        ↓
ML-specific challenges
        ↓
MLOps
```

MLOps is therefore **not simply DevOps applied to ML**. Machine learning introduces additional problems around data, models, experiments, and changing data distributions.

---

# 2. MLOps and DevOps Practices

MLOps adopts many established DevOps practices.

## Source Control

Code should be version controlled using systems such as Git.

```text
Developer
   ↓
Git
   ↓
Repository
   ↓
Versioned Code
```

This allows teams to:

* Track changes
* Revert changes
* Collaborate
* Review code
* Reproduce previous versions

---

## Branching Strategies

Teams can use branches to isolate development work.

Example:

```text
main
 │
 ├── feature/data-pipeline
 │
 ├── feature/model-training
 │
 └── feature/api
```

Changes can later be reviewed and merged into the main branch.

---

## Continuous Integration — CI

**Continuous Integration (CI)** automatically checks changes when developers push code.

A simplified workflow:

```text
Git Push
   ↓
CI Pipeline
   ↓
Tests
   ↓
Linting / Validation
   ↓
Build
   ↓
Result
```

The goal is to detect problems early and reduce integration conflicts.

---

# 3. Continuous Delivery vs Continuous Deployment

These concepts are related but not identical.

### Continuous Delivery (CD)

Code is automatically:

```text
Built
  ↓
Tested
  ↓
Validated
  ↓
Prepared for Release
```

The production release may still require a manual approval.

### Continuous Deployment

Production deployment is also automated:

```text
Code Change
    ↓
CI
    ↓
Tests
    ↓
Validation
    ↓
Automatic Production Deployment
```

### Key Difference

```text
Continuous Delivery
→ Automatically prepare a release

Continuous Deployment
→ Automatically deploy the release
```

---

# 4. What Makes MLOps Different?

Traditional software generally depends on deterministic code:

```text
Input + Code → Output
```

Machine learning introduces additional dependencies:

```text
Data
  +
Code
  +
Features
  +
Model
  +
Hyperparameters
  +
Training Process
        ↓
      Model
        ↓
    Prediction
```

The model's behavior depends heavily on the data used to train it.

Therefore, ML systems require additional operational processes.

---

# 5. Continuous Training — CT

One of the major differences between DevOps and MLOps is **Continuous Training (CT)**.

Traditional software:

```text
Code changes
    ↓
Build
    ↓
Test
    ↓
Deploy
```

ML systems may require:

```text
New Data
   ↓
Data Validation
   ↓
Training
   ↓
Model Evaluation
   ↓
Model Validation
   ↓
Deployment
```

Why?

Because the real-world data distribution can change over time.

A model that performs well today may perform worse later because the relationship between inputs and targets has changed.

---

# 6. Validation in MLOps

In traditional software development, we mainly validate the code.

In MLOps, we need to validate **multiple components**.

```text
Code
Data
Schema
Features
Model
Configuration
Environment
```

For example:

### Data validation

Check:

* Missing values
* Data types
* Value ranges
* Unexpected categories
* Data distribution

### Schema validation

Check whether incoming data still follows the expected structure.

### Model validation

Check:

* Performance metrics
* Model quality
* Required thresholds
* Comparison with the current production model

---

# 7. Monitoring

Deployment is not the end of the ML lifecycle.

After deployment:

```text
Deploy Model
     ↓
   Monitor
     ↓
Detect Problems
     ↓
Retrain / Update
     ↓
Deploy New Model
```

Important things to monitor include:

* Prediction performance
* Data quality
* Data distribution
* Model behavior
* Latency
* Errors
* Resource usage

---

# 8. Concept Drift and Model Decay

### Concept Drift

**Concept drift** occurs when the relationship between input data and the target variable changes over time.

For example:

```text
Past:
Customer behavior → Default risk

Later:
Customer behavior → Different default risk relationship
```

The model may therefore become less accurate even though the software itself has not changed.

### Model Decay

Model performance can decrease over time because the data or real-world environment changes.

```text
Model Performance

High
 │───────
 │       \
 │        \
 │         \
 │          \____
 └──────────────────→ Time
```

This creates a need for:

```text
Monitoring
    ↓
Drift Detection
    ↓
Retraining
    ↓
Evaluation
    ↓
Deployment
```

---

# 9. Team and Operational Challenges

ML systems usually require **multi-functional teams**.

For example:

```text
Product
   +
Data Engineering
   +
Data Science
   +
ML Engineering
   +
Software Engineering
   +
MLOps
```

Different teams may work on different parts of the system.

This creates challenges around:

* Experiment tracking
* Reproducibility
* Versioning
* Collaboration
* Testing
* Deployment
* Infrastructure
* Monitoring

---

# 10. Testing ML Systems

ML testing is more complex than traditional software testing.

A production ML system may require testing of:

```text
Code
 ↓
Data
 ↓
Features
 ↓
Training Pipeline
 ↓
Model
 ↓
API
 ↓
Deployment
```

For example, a model can have correct code but still produce poor predictions because:

* Training data changed
* Features changed
* Data contains unexpected values
* The model was trained with the wrong configuration

Therefore:

> **A successful software test does not necessarily mean the ML system is correct.**

---

# 11. Complex Deployment Pipelines

Deploying an ML model is often a multi-step process.

Example:

```text
Data
 ↓
Validation
 ↓
Preprocessing
 ↓
Feature Engineering
 ↓
Training
 ↓
Evaluation
 ↓
Model Validation
 ↓
Model Registry
 ↓
Deployment
 ↓
Serving
 ↓
Monitoring
```

Each stage can introduce failures.

MLOps aims to automate and control this pipeline.

---

# 12. Technical Debt in MLOps

**Technical debt** is the future cost created by taking shortcuts or accumulating complexity in a system.

ML systems can accumulate technical debt particularly quickly.

Why?

Because ML projects often involve:

* Rapid experimentation
* Temporary code
* Multiple datasets
* Many experiments
* Changing models
* Complex dependencies
* Manual processes
* Data pipelines
* Production infrastructure

A prototype can therefore become difficult to maintain.

---

## Technical Debt Example

Early project:

```text
Notebook
 ↓
Train Model
 ↓
Save model.pkl
```

Production system:

```text
Data Pipeline
     ↓
Data Validation
     ↓
Feature Pipeline
     ↓
Training Pipeline
     ↓
Experiment Tracking
     ↓
Model Registry
     ↓
Deployment
     ↓
API
     ↓
Monitoring
     ↓
Retraining
```

If the system grows without proper engineering practices, maintenance becomes increasingly expensive.

---

# 13. Speed vs Quality

MLOps involves a continuous trade-off between **fast delivery and long-term maintainability**.

A shortcut may make development faster today:

```text
Quick implementation
       ↓
Fast delivery
```

But if the shortcut creates technical debt:

```text
Technical debt
       ↓
More maintenance
       ↓
More complexity
       ↓
Slower future development
```

The objective is not to eliminate all technical debt.

The objective is to **manage it deliberately** and prevent high-cost debt from accumulating.

---

# 14. DevOps → MLOps

A useful comparison:

| DevOps                 | MLOps                           |
| ---------------------- | ------------------------------- |
| Source control         | Source control                  |
| Branching              | Branching                       |
| CI                     | CI                              |
| Continuous delivery    | Continuous delivery             |
| Continuous deployment  | Continuous deployment           |
| Software testing       | Software + data + model testing |
| Application monitoring | Application + model monitoring  |
| Deployment             | Model deployment                |
| —                      | Continuous training             |
| —                      | Data validation                 |
| —                      | Model validation                |
| —                      | Drift detection                 |
| —                      | Retraining                      |

The important point is:

> **MLOps inherits DevOps practices but adds processes required to operate data- and model-dependent systems.**

---

# 15. Key Takeaways

### MLOps

MLOps applies operational and software engineering practices to the ML lifecycle.

### DevOps practices reused by MLOps

* Git and source control
* Branching
* CI
* Continuous delivery
* Continuous deployment
* Automated testing

### ML-specific additions

* Data validation
* Schema validation
* Model validation
* Continuous training
* Experiment tracking
* Model monitoring
* Drift detection
* Retraining

### Technical debt

ML systems can accumulate technical debt quickly because of their experimental and data-dependent nature.

The core goal is:

```text
Reliable Code
     +
Reliable Data
     +
Reliable Models
     +
Automation
     +
Monitoring
     ↓
Sustainable ML System
```

---

# 16. Mental Model

Remember the difference like this:

```text
             DEVOPS
                │
       Code + Software
                │
                ▼
             MLOps
                │
     ┌──────────┼──────────┐
     ▼          ▼          ▼
   Data       Model       Code
     │          │          │
     └──────────┼──────────┘
                ▼
        Training Pipeline
                ▼
            Deployment
                ▼
           Monitoring
                ▼
         Drift Detection
                ▼
           Retraining
                ↺
```

**MLOps = DevOps principles + ML-specific lifecycle management.**
