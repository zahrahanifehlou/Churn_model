# Telco Customer Churn — End-to-End MLOps Pipeline

> **First project in the End-to-End MLOps series.**  
> The goal is to go beyond notebooks and build a production-grade ML pipeline covering data quality, training, serving, containerisation, CI/CD, deployment, and monitoring.

---

## Table of Contents

- [Overview](#overview)
- [Dataset](#dataset)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
- [Pipeline Stages](#pipeline-stages)
  - [1. Data Quality](#1-data-quality)
  - [2. Training & Experiment Tracking](#2-training--experiment-tracking)
  - [3. Serving Layer](#3-serving-layer)
  - [4. Containerisation](#4-containerisation)
  - [5. CI/CD](#5-cicd)
  - [6. Cloud Deployment](#6-cloud-deployment)
- [API Reference](#api-reference)
- [Running Tests](#running-tests)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

This project predicts whether a telecom customer will churn (cancel their subscription) using structured customer data. The emphasis is on the **full MLOps lifecycle**, not just model accuracy:

- Automated data validation before every training run
- Tracked experiments so every model version is reproducible
- A REST API ready for production traffic
- A Docker image that runs identically on any machine or cloud node
- GitHub Actions pipelines that test, build, and deploy on every push
- AWS ECS (Fargate) hosting behind an Application Load Balancer for scalable, serverless inference

---

## Dataset

| Property | Value |
|---|---|
| Source | [IBM Watson — Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) |
| File | `data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv` |
| Rows | 7 043 |
| Columns | 21 |
| Target | `Churn` (Yes / No) |

**Key features:** `tenure`, `Contract`, `MonthlyCharges`, `TotalCharges`, `InternetService`, `PaymentMethod`, and 15 additional service / demographic columns.

---

## Project Structure

```
Churn_model/
├── .github/
│   └── workflows/          # GitHub Actions CI/CD pipelines
├── data/
│   ├── raw/                # Original, immutable data
│   └── processed/          # Cleaned & feature-engineered data
├── notebooks/
│   └── check_data.ipynb    # Exploratory data analysis
├── src/
│   ├── data/               # Data loading & preprocessing
│   ├── features/           # Feature engineering
│   ├── models/             # Training & evaluation scripts
│   ├── api/                # FastAPI application
│   └── expectations/       # Great Expectations suites
├── tests/                  # Unit & integration tests
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Tech Stack

| Layer | Tool | Purpose |
|---|---|---|
| Data Quality | [Great Expectations](https://greatexpectations.io/) | Validate data before training |
| Experiment Tracking | [MLFlow](https://mlflow.org/) | Log params, metrics, and artefacts |
| Serving | [FastAPI](https://fastapi.tiangolo.com/) | REST API for real-time predictions |
| Containerisation | [Docker](https://www.docker.com/) | Reproducible runtime environment |
| CI/CD | [GitHub Actions](https://github.com/features/actions) | Automated test → build → deploy |
| Cloud Compute | [AWS ECS Fargate](https://aws.amazon.com/fargate/) | Serverless container hosting |
| Load Balancing | [AWS ALB](https://aws.amazon.com/elasticloadbalancing/) | Route and distribute inference traffic |

---

## Getting Started

### Prerequisites

- Python 3.9+
- Docker & Docker Compose
- AWS CLI configured (`aws configure`)
- An MLFlow tracking server (local or remote)

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/<your-org>/Churn_model.git
cd Churn_model

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file at the project root (never commit this file):

```env
MLFLOW_TRACKING_URI=http://localhost:5000
AWS_REGION=us-east-1
ECR_REPOSITORY=churn-model
ECS_CLUSTER=churn-cluster
ECS_SERVICE=churn-service
```

---

## Pipeline Stages

### 1. Data Quality

[Great Expectations](https://greatexpectations.io/) suites live in `src/expectations/`. Run validations with:

```bash
python src/expectations/validate.py
```

Checks include: no missing values in critical columns, value ranges for `tenure` and `MonthlyCharges`, and valid category sets for `Contract` and `InternetService`.

### 2. Training & Experiment Tracking

All training runs are logged to MLFlow (parameters, metrics, and the serialised model artefact):

```bash
python src/models/train.py
```

Launch the MLFlow UI to compare runs:

```bash
mlflow ui
# open http://localhost:5000
```

### 3. Serving Layer

The FastAPI app exposes a `/predict` endpoint that loads the registered MLFlow model at startup:

```bash
uvicorn src.api.main:app --reload
# open http://localhost:8000/docs for the interactive Swagger UI
```

### 4. Containerisation

```bash
# Build
docker build -t churn-model:latest .

# Run locally
docker compose up
```

### 5. CI/CD

GitHub Actions workflows (`.github/workflows/`) automatically:

1. **Test** — run `pytest` on every pull request
2. **Build** — build and push the Docker image to AWS ECR on merge to `main`
3. **Deploy** — update the ECS service with the new image revision

### 6. Cloud Deployment

The container runs on **AWS ECS (Fargate)** — no EC2 instances to manage. An **Application Load Balancer (ALB)** sits in front of the ECS service and handles HTTPS termination, routing, and health checks.

```
Internet → ALB (HTTPS :443) → ECS Fargate Task (FastAPI :8000)
```

---

## API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `POST` | `/predict` | Return churn probability for a customer |

**Example request:**

```json
POST /predict
{
  "tenure": 12,
  "MonthlyCharges": 65.5,
  "TotalCharges": 786.0,
  "Contract": "Month-to-month",
  "InternetService": "Fiber optic",
  "PaymentMethod": "Electronic check"
}
```

**Example response:**

```json
{
  "churn_probability": 0.73,
  "churn_prediction": "Yes"
}
```

---

## Running Tests

```bash
pytest tests/ -v
```

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "feat: your feature"`
4. Push and open a Pull Request

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
