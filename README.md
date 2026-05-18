# VMS Operations Health Dashboard

Public case study for operational health checks across video analytics modules in a Dahua/Intelbras operational platform family.

This repository models the support view I care about in real security operations: are the modules online, are cameras delivering fresh frames, is inference latency acceptable, is the alert channel healthy, and does a period without alerts mean quiet operation or a system issue?

## Operational Problem

A monitoring team cannot rely only on alerts. A system may be healthy and simply have no incidents, or it may be silent because a camera stalled, a worker stopped, or an alert channel failed. This dashboard separates business events from technical health.

## What This Demonstrates

- Health model for elevator dwell analytics, carona access monitoring, and sidewalk monitoring, treating Dahua/Intelbras as one platform family.
- Camera freshness, inference latency, restart count, open event count, and alert-channel state.
- Alert-silence check for cases like "no alert since Friday".
- Prometheus-style `/metrics` endpoint for monitoring integrations.
- Clean public-safe API payloads for support workflows.

## Architecture

```text
module probes -> operations snapshot -> health decision
             -> alert-silence review -> metrics endpoint
```

## Run Locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8014
```

Open:

- `http://127.0.0.1:8014/`
- `http://127.0.0.1:8014/api/operations/snapshot`
- `http://127.0.0.1:8014/api/alerts/silence-check`
- `http://127.0.0.1:8014/metrics`

## Public-Safe Scope

All modules, counters, latencies, camera counts, and alert history values are synthetic. No customer data, private IPs, real logs, credentials, dashboards, platform SDK files, alert destinations, or incident records are included.

## Skills Represented

Python, FastAPI, observability, health checks, alerting logic, Prometheus-style metrics, VMS support workflows, and operational debugging.
