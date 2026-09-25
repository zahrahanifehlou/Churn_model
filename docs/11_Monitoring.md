Monitoring

This is where MLOps becomes significantly different from normal software deployment.

A normal application asks:

Is the application working?

ML asks:

Is the application working and is the model still behaving correctly?

Monitor:

System metrics
CPU
GPU
RAM
latency
throughput
errors
Model metrics
accuracy
precision
recall
F1
Data metrics
missing values
distribution
schema
feature statistics
Drift
Training data
      ↓
Distribution A


Production data
      ↓
Distribution B

If A and B become significantly different:

Data drift