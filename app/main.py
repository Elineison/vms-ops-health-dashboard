from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

from app.probes import WORKERS


app = FastAPI(
    title="Security Ops Monitoring Demo",
    version="1.0.0",
    description="Public-safe monitoring demo for distributed video analytics systems.",
)


@app.get("/api/workers")
def workers() -> list[dict]:
    return [
        {
            **worker.__dict__,
            "issues": worker.issues(),
        }
        for worker in WORKERS
    ]


@app.get("/api/health")
def health() -> dict:
    worker_payloads = workers()
    issues = [
        {"worker": worker["name"], **issue}
        for worker in worker_payloads
        for issue in worker["issues"]
    ]
    critical = any(issue["severity"] == "critical" for issue in issues)
    return {
        "service": "security-ops-monitoring-demo",
        "state": "CRITICAL" if critical else ("DEGRADED" if issues else "HEALTHY"),
        "workers_total": len(worker_payloads),
        "cameras_running": sum(worker["cameras_running"] for worker in worker_payloads),
        "cameras_expected": sum(worker["cameras_expected"] for worker in worker_payloads),
        "active_alerts": sum(worker["active_alerts"] for worker in worker_payloads),
        "issues": issues,
    }


@app.get("/metrics", response_class=PlainTextResponse)
def metrics() -> str:
    lines = [
        "# HELP vms_worker_online Worker online state.",
        "# TYPE vms_worker_online gauge",
    ]
    for worker in WORKERS:
        online = 1 if worker.state == "online" else 0
        labels = f'worker="{worker.name}",role="{worker.role}"'
        lines.append(f"vms_worker_online{{{labels}}} {online}")
        lines.append(f"vms_cameras_running{{{labels}}} {worker.cameras_running}")
        lines.append(f"vms_cameras_expected{{{labels}}} {worker.cameras_expected}")
        lines.append(f"vms_frame_age_p95_seconds{{{labels}}} {worker.frame_age_p95_s}")
        lines.append(f"vms_inference_p95_ms{{{labels}}} {worker.inference_p95_ms}")
        lines.append(f"vms_gpu_memory_used_percent{{{labels}}} {worker.gpu_memory_used_pct}")
        lines.append(f"vms_active_alerts{{{labels}}} {worker.active_alerts}")
    return "\n".join(lines) + "\n"

