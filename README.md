# Security Ops Monitoring Demo

Public portfolio demo for operational monitoring of video analytics systems.

This project models how a production support team can observe distributed VMS services: worker health, frame freshness, inference latency, GPU pressure, active alerts, and service state.

## What This Demonstrates

- FastAPI health API
- Prometheus-style metrics output
- issue classification for video analytics systems
- synthetic worker probes
- operational thinking from security electronics support
- public-safe monitoring design

## Run Locally

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open:

- `http://127.0.0.1:8000/api/health`
- `http://127.0.0.1:8000/metrics`
- `http://127.0.0.1:8000/api/workers`

## Example

```bash
curl http://127.0.0.1:8000/api/health
curl http://127.0.0.1:8000/metrics
```

## Portfolio Note

All metrics are synthetic. This repository does not expose production monitoring configuration, hostnames, private IPs, customer identifiers, logs, or alert destinations.

