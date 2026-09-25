# DVC — Data Version Control

## 1. What is DVC?

**DVC (Data Version Control)** is a tool used to version and reproduce datasets, ML models, and other large files that should not be stored directly in Git.

Git is excellent for versioning:

* Python code
* Configuration files
* Tests
* Documentation
* Small metadata files

But Git is not designed for large datasets such as:

* CSV files with millions of rows
* Images
* Audio
* Video
* Large model files
* Processed datasets

DVC works together with Git.

The basic idea is:

```text
Git  → versions the code and DVC metadata
DVC  → versions the actual data
Storage → stores the actual dataset files
```

---

# 2. Why do we need data versioning?

Imagine an ML project:

```text
data/raw/
    train.csv
```

You train a model today.

Later, you modify the preprocessing:

```text
remove missing values
normalize numerical features
encode categorical features
```

Now you have a different dataset.

If you simply overwrite:

```text
data/train.csv
```

you lose the previous version.

You may no longer know:

* Which data was used to train model v1?
* Which preprocessing created the data?
* What changed between datasets?
* Can I reproduce an old experiment?
* Which model was trained with which dataset?

This is the problem that **data versioning** solves.

---

# 3. What does DVC actually store?

A common misunderstanding is:

> "DVC puts my dataset into Git."

It does not.

Suppose you have:

```text
data/
    raw/
        churn.csv
```

You run:

```bash
dvc add data/raw/churn.csv
```

DVC creates:

```text
data/raw/churn.csv.dvc
```

The `.dvc` file is a small metadata file.

Conceptually:

```text
data/raw/churn.csv.dvc
        |
        | contains metadata
        | about the dataset
        ▼
DVC storage
        |
        ▼
actual churn.csv
```

Git tracks:

```text
data/raw/churn.csv.dvc
```

DVC manages:

```text
data/raw/churn.csv
```

---

# 4. Installing DVC

Install DVC with:

```bash
pip install dvc
```

Check:

```bash
dvc --version
```

---

# 5. Initialize DVC

Start with an existing Git repository:

```bash
git init
```

Then:

```bash
dvc init
```

Now the project contains DVC configuration.

Typical structure:

```text
project/
│
├── .git/
├── .dvc/
├── data/
├── src/
├── notebooks/
└── README.md
```

Commit the DVC configuration:

```bash
git add .dvc
git commit -m "Initialize DVC"
```

---

# 6. Add raw data to DVC

Suppose:

```text
data/
└── raw/
    └── churn.csv
```

Run:

```bash
dvc add data/raw/churn.csv
```

DVC creates:

```text
data/
└── raw/
    ├── churn.csv
    └── churn.csv.dvc
```

The dataset itself is now managed by DVC.

The `.dvc` file should be committed to Git:

```bash
git add data/raw/churn.csv.dvc
git commit -m "Version raw churn dataset"
```

---

# 7. The important idea: Git commit + DVC data version

A dataset version is reproducible because two things work together:

```text
Git commit
     +
DVC-tracked data
```

For example:

```text
Git commit A
    |
    └── churn.csv.dvc
             |
             └── dataset version 1
```

Later:

```text
Git commit B
    |
    └── churn.csv.dvc
             |
             └── dataset version 2
```

Therefore:

```text
Git commit A → DVC dataset version 1
Git commit B → DVC dataset version 2
```

---

# 8. What happens when the dataset changes?

Suppose the original dataset is:

```text
churn.csv
```

You receive new customer records.

You update:

```text
churn.csv
```

Now run:

```bash
dvc add data/raw/churn.csv
```

DVC detects that the file changed and updates:

```text
churn.csv.dvc
```

Then commit the metadata:

```bash
git add data/raw/churn.csv.dvc
git commit -m "Update churn dataset"
```

Now you have a new dataset version.

---

# 9. Checkout an old dataset version

Suppose your Git history contains:

```text
commit A → dataset v1
commit B → dataset v2
commit C → dataset v3
```

To retrieve the dataset associated with commit A:

```bash
git checkout A
dvc checkout
```

DVC restores the data corresponding to that Git revision.

This is extremely important for ML reproducibility.

---

# 10. DVC remote storage

DVC can use remote storage.

Examples:

```text
Amazon S3
Google Cloud Storage
Azure Blob Storage
SSH
Google Drive
local filesystem
```

For example:

```text
GitHub
   |
   | code + .dvc metadata
   |
   ▼
Git repository


DVC
   |
   | actual datasets
   |
   ▼
S3 / Azure / GCS
```


---

# 11. Configure a local DVC remote

For learning, you can use a local directory.

Example:

```bash
mkdir -p ../dvc-storage
```

Configure it:

```bash
dvc remote add -d localstorage ../dvc-storage
```

Check:

```bash
dvc remote list
```

You might see:

```text
localstorage    ../dvc-storage    default
```

---

# 12. Push data to the remote

After adding data:

```bash
dvc add data/raw/churn.csv
```

Push it:

```bash
dvc push
```

Now the actual data is stored in the DVC remote.

Git still stores only the metadata.

---

# 13. Pull data

On another machine:

```bash
git clone <repository>
```

Then:

```bash
dvc pull
```

DVC downloads the required data from the remote.

This gives you:

```text
Git repository
+
DVC remote
=
reproducible project
```

---

# 14. DVC's content-addressed storage

DVC identifies data using hashes.

Conceptually:

```text
churn.csv
    ↓
hash
    ↓
abc123...
```

If the contents change:

```text
churn.csv
    ↓
new hash
    ↓
xyz789...
```

Therefore DVC can determine whether the data changed.

This also helps DVC avoid unnecessarily duplicating identical data.

---



# 15. What if I change preprocessing?

This is a very important MLOps question.

Suppose version 1 uses:

```text
missing values → median
```

Then you change the preprocessing to:

```text
missing values → mean
```

This creates a different processed dataset.

You should not lose the previous result.

Instead:

```text
Raw Dataset v1
       |
       ▼
Preprocessing v1
       |
       ▼
Processed Dataset v1
```

Then:

```text
Raw Dataset v1
       |
       ▼
Preprocessing v2
       |
       ▼
Processed Dataset v2
```

Both are reproducible.

---

# 16. What should be versioned?

In an MLOps project, version at least:

### Data

```text
raw data
processed data
training data
validation data
test data
```

### Code

```text
preprocessing code
training code
evaluation code
inference code
```

### Configuration

```text
preprocessing parameters
training parameters
model parameters
```

### Models

```text
trained model artifacts
```

### Metadata

```text
dataset version
model version
experiment information
metrics
```

---


# 17. Dependencies and outputs

Every DVC stage can have:

```text
deps
outs
```

### Dependencies

Things required to run the stage:

```yaml
deps:
  - data/raw/churn.csv
  - src/preprocess.py
```

### Outputs

Things produced by the stage:

```yaml
outs:
  - data/processed/churn.csv
```

Therefore:

```text
dependency → command → output
```

---

# 18. Why dependency tracking matters

Suppose:

```text
raw data
    ↓
preprocess
    ↓
processed data
    ↓
train
```

You modify:

```text
preprocess.py
```

DVC knows that the preprocessing stage changed.

Therefore the processed dataset must be regenerated.

And because the processed dataset changed, training may also need to run again.

This is the foundation of reproducible ML pipelines.

---

# 19. dvc repro

After defining the pipeline:

```bash
dvc repro
```

DVC determines which stages need to run.

For example:

```text
preprocess.py changed
        ↓
preprocess must run
        ↓
processed data changed
        ↓
train must run
        ↓
model changed
        ↓
evaluation must run
```

DVC avoids unnecessarily running stages whose dependencies have not changed.

---

# 20. dvc status

Check whether the pipeline/data has changed:

```bash
dvc status
```

It can tell you that something is different from the last saved state.

For example:

```text
Data and pipelines are up to date.
```

or:

```text
modified:
    data/raw/churn.csv
```

---

# 21. dvc diff

You can compare DVC versions:

```bash
dvc diff
```

This helps identify changes between dataset versions.

Conceptually:

```text
Dataset v1
    ↓
Dataset v2

added records
deleted records
changed files
```

---

# 22. DVC experiments

DVC can also help manage ML experiments.

For example:

```text
Experiment A
learning_rate = 0.001

Experiment B
learning_rate = 0.01

Experiment C
learning_rate = 0.1
```

You can use:

```bash
dvc exp run
```

DVC can track changes in parameters and outputs.

---

# 23. Parameters

Parameters can be stored in:

```text
params.yaml
```

Example:

```yaml
train:
  learning_rate: 0.001
  epochs: 20
  batch_size: 32
```

Then your training code reads these parameters.

DVC can track parameter changes.

---

# 24. Metrics

Your training pipeline can produce:

```text
metrics.json
```

Example:

```json
{
  "accuracy": 0.91,
  "precision": 0.89,
  "recall": 0.87,
  "f1": 0.88
}
```

DVC can track metrics.

You can inspect them with:

```bash
dvc metrics show
```

And compare them:

```bash
dvc metrics diff
```

---

# 25. Complete experiment relationship

A reproducible experiment should connect:

```text
Dataset
   +
Code
   +
Parameters
   +
Model
   +
Metrics
```

For example:

```text
Dataset v3
    +
preprocessing code v2
    +
learning_rate = 0.001
    +
Random seed = 42
    ↓
Model v5
    ↓
F1 = 0.88
```

Now you know exactly what produced the model.


---

# 26. Important commands

### Initialize

```bash
dvc init
```

### Track data

```bash
dvc add data/raw/churn.csv
```

### Push data

```bash
dvc push
```

### Download data

```bash
dvc pull
```

### Check status

```bash
dvc status
```

### Reproduce pipeline

```bash
dvc repro
```

### Show pipeline

```bash
dvc dag
```

### Compare metrics

```bash
dvc metrics diff
```

### Show metrics

```bash
dvc metrics show
```

### Compare data

```bash
dvc diff
```

### Run experiment

```bash
dvc exp run
```

---

# 27. DVC vs Git LFS

Both can manage large files, but they solve somewhat different problems.

| Feature                   | Git     | Git LFS    | DVC             |
| ------------------------- | ------- | ---------- | --------------- |
| Code versioning           | Yes     | No         | No              |
| Large files               | Limited | Yes        | Yes             |
| Dataset versioning        | Basic   | File-based | Designed for ML |
| ML pipelines              | No      | No         | Yes             |
| Experiments               | No      | No         | Yes             |
| Metrics                   | No      | No         | Yes             |
| Parameters                | No      | No         | Yes             |
| Data lineage              | Limited | Limited    | Strong          |
| Reproducible ML pipelines | No      | No         | Yes             |

DVC is specifically designed around **ML data and reproducibility**.

---

# 28. DVC vs MLflow

DVC and MLflow are complementary.

### DVC

Focuses heavily on:

```text
data
pipelines
experiments
reproducibility
```

### MLflow

Focuses heavily on:

```text
experiment tracking
metrics
parameters
models
model registry
```

A production MLOps architecture may use both:

```text
              Git
               |
       ┌───────┴───────┐
       │               │
      DVC            MLflow
       │               │
    datasets        experiments
    pipelines       metrics
    data versions   models
       │               │
       └───────┬───────┘
               │
          ML workflow
```

---

# 29. Recommended project structure

A simple DVC-based ML project can look like:

```text
churn-ml/
│
├── data/
│   ├── raw/
│   │   └── churn.csv
│   │
│   └── processed/
│       └── churn_processed.csv
│
├── src/
│   ├── preprocess.py
│   ├── train.py
│   └── evaluate.py
│
├── configs/
│   └── config.yaml
│
├── models/
│
├── metrics/
│
├── notebooks/
│
├── dvc.yaml
├── params.yaml
├── .dvcignore
├── .gitignore
└── README.md
```

---

# 30. A complete example

Suppose we start with:

```text
data/raw/churn.csv
```

### Step 1 — Initialize

```bash
git init
dvc init
```

### Step 2 — Track raw data

```bash
dvc add data/raw/churn.csv
```

### Step 3 — Commit metadata

```bash
git add .
git commit -m "Add raw churn dataset"
```

### Step 4 — Create preprocessing

```text
src/preprocess.py
```

The script creates:

```text
data/processed/churn.csv
```

### Step 5 — Track processed data

```bash
dvc add data/processed/churn.csv
```

### Step 6 — Commit

```bash
git add .
git commit -m "Add processed churn dataset"
```

### Step 7 — Create training pipeline

```text
raw data
   ↓
preprocessing
   ↓
processed data
   ↓
training
   ↓
model
   ↓
evaluation
```

### Step 8 — Create DVC pipeline

```bash
dvc stage add ...
```

### Step 9 — Reproduce

```bash
dvc repro
```

### Step 10 — Push data

```bash
dvc push
```

### Step 11 — Push Git

```bash
git push
```

Now the project can be reproduced by another developer.

---

# 31. What happens when preprocessing changes?

This is the key MLOps workflow.

Initial version:

```text
RAW v1
  |
  ▼
preprocess.py v1
  |
  ▼
PROCESSED v1
  |
  ▼
MODEL v1
```

You change preprocessing:

```text
preprocess.py v2
```

Now:

```text
RAW v1
  |
  ▼
preprocess.py v2
  |
  ▼
PROCESSED v2
  |
  ▼
MODEL v2
```

The raw data did not change.

The preprocessing code changed.

Therefore the processed data changes.

DVC can detect this dependency through the pipeline.

---

# 32. What if the raw data changes?

Then:

```text
RAW v2
  |
  ▼
preprocess.py v2
  |
  ▼
PROCESSED v3
  |
  ▼
MODEL v3
```

The entire downstream pipeline may need to be reproduced.

This is why dependency tracking is important.

---

# 33. What should NOT be done?

Avoid manually overwriting everything without recording the relationship.

Bad:

```text
data.csv
data_final.csv
data_final2.csv
data_final_new.csv
data_final_really_new.csv
```

This makes lineage unclear.

Instead:

```text
raw data
    ↓
versioned preprocessing
    ↓
versioned processed data
    ↓
versioned training
    ↓
versioned model
```

---

# 34. Data lineage

DVC helps establish **data lineage**.

Data lineage answers:

> Where did this model come from?

For example:

```text
Model v4
   ↑
Training v3
   ↑
Processed Dataset v7
   ↑
Preprocessing v3
   ↑
Raw Dataset v2
```

This is extremely important in production ML.

---

# 35. Reproducibility

The ultimate goal is:

> Given the same code, data, parameters, and environment, I should be able to reproduce the experiment.

Conceptually:

```text
Git commit
+
DVC dataset version
+
parameters
+
pipeline
+
environment
+
random seed
        ↓
same experiment
        ↓
same result
```

Perfect bit-for-bit reproducibility is not always guaranteed across different hardware/software environments, but the workflow should make the experiment traceable and repeatable.

---

# 36. DVC in the MLOps lifecycle

A simplified MLOps workflow is:

```text
             DATA
               |
               ▼
        Data Versioning
             DVC
               |
               ▼
       Data Validation
               |
               ▼
        Preprocessing
               |
               ▼
       Feature Engineering
               |
               ▼
          Training
               |
               ▼
        Experiment Tracking
               |
               ▼
          Evaluation
               |
               ▼
       Model Versioning
               |
               ▼
          Deployment
               |
               ▼
         Monitoring
               |
               ▼
          New Data
               |
               └──────────► repeat
```

DVC is especially useful around:

```text
data
preprocessing
pipelines
experiments
reproducibility
```

---


# 37. DVC checklist

When starting an ML project:

* [ ] Initialize Git
* [ ] Initialize DVC
* [ ] Define raw-data structure
* [ ] Add raw data to DVC
* [ ] Commit `.dvc` metadata to Git
* [ ] Configure DVC remote
* [ ] Push data to remote
* [ ] Write preprocessing code
* [ ] Track preprocessing outputs
* [ ] Define DVC pipeline
* [ ] Version parameters
* [ ] Version models
* [ ] Track metrics
* [ ] Use `dvc repro`
* [ ] Use `dvc status`
* [ ] Use `dvc diff`
* [ ] Test reproduction from a clean environment

---

# 38. The core commands to remember

```bash
# Initialize
dvc init

# Track data
dvc add data/raw/churn.csv

# Configure remote
dvc remote add -d storage <remote>

# Upload data
dvc push

# Download data
dvc pull

# Check changes
dvc status

# Reproduce pipeline
dvc repro

# Show pipeline
dvc dag

# Show metrics
dvc metrics show

# Compare metrics
dvc metrics diff

# Compare data
dvc diff

# Run experiment
dvc exp run
```


---

# Example: Preprocessing Version 1

Suppose we start with:

```yaml
preprocess:
  missing_strategy: median
  scaler_type: standard
  remove_outliers: false
```

Run:

```bash
dvc repro
```

The pipeline produces:

```text
data/processed/churn_processed.csv
```

DVC calculates a hash of the resulting file and stores the file in its cache.

Then commit the pipeline state:

```bash
git add params.yaml dvc.yaml dvc.lock
git commit -m "Preprocessing: median + standard scaler"
```

If the processed dataset is a DVC output, the important metadata is recorded in `dvc.lock`.

---

# Example: Preprocessing Version 2

Now we want to try a different strategy.

Change:

```yaml
preprocess:
  missing_strategy: mean
  scaler_type: minmax
  remove_outliers: true
```

Then run:

```bash
dvc repro
```

DVC detects that the preprocessing parameters changed.

It runs the preprocessing stage again and generates a new:

```text
data/processed/churn_processed.csv
```

The previous version is not simply lost.

DVC has the previous version in its cache, and the Git history records which parameters and DVC pipeline state produced it.

Commit the new version:

```bash
git add params.yaml dvc.lock
git commit -m "Preprocessing: mean + minmax + outlier removal"
```

---

# What Is Actually Being Versioned?

There are several things involved:

```text
Git
│
├── preprocess.py
├── params.yaml
├── dvc.yaml
└── dvc.lock
       │
       ▼
DVC
│
├── Processed dataset version 1
├── Processed dataset version 2
└── ...
```

### Git versions:

* preprocessing code
* parameters
* pipeline definition
* DVC lock file

### DVC versions:

* datasets
* processed datasets
* other large ML artifacts

This gives us a connection between:

```text
Code + Parameters + Data
```

---

# Going Back to an Older Version

Suppose we have:

```text
Commit A
    ↓
median + standard scaler
    ↓
processed dataset V1

Commit B
    ↓
mean + minmax scaler
    ↓
processed dataset V2
```

We are currently on Commit B.

To go back to Commit A:

```bash
git checkout <old-commit>
```

Then restore the corresponding DVC data:

```bash
dvc checkout
```

Now the working directory contains the processed dataset corresponding to that older Git/DVC state.

This is one of the important benefits of combining Git and DVC.

---

# Why Not Create Many CSV Files?

It is possible to do this:

```text
data/processed/
├── churn_median_standard.csv
├── churn_mean_minmax.csv
├── churn_median_no_outliers.csv
└── churn_mean_standard.csv
```

But this can become difficult to manage.

You now have to manually keep track of:

```text
Which file?
Which parameters?
Which preprocessing code?
Which model?
Which experiment?
```

For a normal ML pipeline, it is cleaner to use:

```text
data/processed/churn_processed.csv
```

and let Git + DVC track the history.

---

# When Multiple Files Make Sense

Multiple processed datasets can make sense when you intentionally want to keep several datasets available **at the same time**.

For example:

```text
data/processed/
├── churn_standard.csv
├── churn_minmax.csv
└── churn_robust.csv
```

This can be useful for a specific comparison experiment.

But this is different from normal pipeline versioning.

For normal development:

```text
Raw Data
   ↓
Preprocessing
   ↓
ONE processed output
```

is simpler.

---

# Important MLOps Principle

The important idea is **not**:

> "Save every preprocessing result as a different filename."

The important idea is:

> **Make the preprocessing process reproducible and version the inputs, code, parameters, and outputs.**

For example:

```text
Dataset V1
+
preprocess.py V1
+
params.yaml V1
        ↓
Processed Dataset V1
```

Then:

```text
Dataset V1
+
preprocess.py V1
+
params.yaml V2
        ↓
Processed Dataset V2
```

The preprocessing configuration is therefore part of the reproducibility record.

---

# The Complete MLOps Flow

A simple DVC-based ML workflow looks like:

```text
                    Git
                     │
          ┌──────────┼──────────┐
          │          │          │
     preprocess.py params.yaml dvc.yaml
          │          │
          └─────┬────┘
                │
                ▼
          DVC pipeline
                │
                ▼
        data/raw/churn.csv
                │
                ▼
          preprocessing
                │
                ▼
   data/processed/churn_processed.csv
                │
                ▼
             training
                │
                ▼
          trained model
```

DVC records the relationship between these stages.

---

# Key Commands

Track the raw dataset:

```bash
dvc add data/raw/churn.csv
```

Run the pipeline:

```bash
dvc repro
```

Check the pipeline status:

```bash
dvc status
```

Commit the pipeline metadata:

```bash
git add params.yaml dvc.yaml dvc.lock
git commit -m "Update preprocessing"
```

Restore the data corresponding to the current Git version:

```bash
dvc checkout
```

---

# One-Sentence Summary

> **Change the preprocessing parameters → run `dvc repro` → DVC generates the new processed dataset → Git records the code/configuration/pipeline state → DVC keeps the corresponding data versions.**

The key MLOps principle is:

```text
Git = code + configuration + pipeline definition

DVC = datasets + large ML artifacts

Together = reproducible ML experiments
```
