# mlops-batch-signal-pipeline
# MLOps Batch Signal Pipeline

## Overview

This project implements a minimal MLOps-style batch processing pipeline in Python.

The pipeline:

- Loads configuration from YAML
- Reads OHLCV market data from CSV
- Computes a rolling mean on the close price
- Generates trading signals
- Produces structured metrics in JSON format
- Generates detailed execution logs
- Runs locally and inside Docker

---

## Project Structure

```text
mlops-batch-signal-pipeline/
│
├── run.py
├── config.yaml
├── data.csv
├── requirements.txt
├── Dockerfile
├── README.md
├── metrics.json
└── run.log
```

---

## Configuration

config.yaml

```yaml
seed: 42
window: 5
version: "v1"
```

---

## Installation

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Local Execution

Run the application:

```bash
python run.py --input data.csv --config config.yaml --output metrics.json --log-file run.log
```

---

## Processing Steps

1. Load and validate configuration
2. Load and validate dataset
3. Compute rolling mean on close price
4. Generate binary signals

Signal Logic:

```text
signal = 1 if close > rolling_mean
signal = 0 otherwise
```

5. Compute metrics:
   - rows_processed
   - signal_rate
   - latency_ms

6. Save results to metrics.json
7. Write execution logs to run.log

---

## Docker

### Build Image

```bash
docker build -t mlops-task .
```

### Run Container

```bash
docker run --rm mlops-task
```

---

## Example metrics.json

```json
{
    "version": "v1",
    "rows_processed": 10000,
    "metric": "signal_rate",
    "value": 0.4990,
    "latency_ms": 127,
    "seed": 42,
    "status": "success"
}
```

---

## Example run.log

```text
2026-06-03 10:00:01,112 - INFO - Job started
2026-06-03 10:00:01,118 - INFO - Config loaded: seed=42, window=5, version=v1
2026-06-03 10:00:01,145 - INFO - Rows loaded: 10000
2026-06-03 10:00:01,151 - INFO - Rolling mean computed
2026-06-03 10:00:01,156 - INFO - Signals generated
2026-06-03 10:00:01,239 - INFO - Metrics generated successfully
2026-06-03 10:00:01,240 - INFO - Job completed successfully
```

---

## Features

- Deterministic execution using configurable seed
- Structured JSON metrics output
- Comprehensive logging
- Error handling and validation
- Dockerized deployment
- Reproducible batch processing workflow

---

## Author

Submitted for ML/MLOps Engineering Internship Technical Assessment.
