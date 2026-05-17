from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WorkerProbe:
    name: str
    role: str
    state: str
    cameras_running: int
    cameras_expected: int
    frame_age_p95_s: float
    inference_p95_ms: float
    gpu_memory_used_pct: float
    active_alerts: int

    def issues(self) -> list[dict]:
        issues: list[dict] = []
        if self.state != "online":
            issues.append({"severity": "critical", "reason": "worker_offline"})
        if self.cameras_running < self.cameras_expected:
            issues.append({"severity": "warning", "reason": "camera_runtime_missing"})
        if self.frame_age_p95_s > 5:
            issues.append({"severity": "warning", "reason": "stale_frames"})
        if self.inference_p95_ms > 1200:
            issues.append({"severity": "warning", "reason": "slow_inference"})
        if self.gpu_memory_used_pct > 92:
            issues.append({"severity": "warning", "reason": "gpu_memory_pressure"})
        return issues


WORKERS = [
    WorkerProbe(
        name="analytics-worker-a",
        role="elevator-analytics",
        state="online",
        cameras_running=18,
        cameras_expected=18,
        frame_age_p95_s=0.28,
        inference_p95_ms=940,
        gpu_memory_used_pct=86.0,
        active_alerts=0,
    ),
    WorkerProbe(
        name="analytics-worker-b",
        role="elevator-analytics",
        state="online",
        cameras_running=19,
        cameras_expected=19,
        frame_age_p95_s=0.35,
        inference_p95_ms=1035,
        gpu_memory_used_pct=89.5,
        active_alerts=1,
    ),
    WorkerProbe(
        name="live-gateway",
        role="live-streaming",
        state="online",
        cameras_running=42,
        cameras_expected=42,
        frame_age_p95_s=0.19,
        inference_p95_ms=0,
        gpu_memory_used_pct=0.0,
        active_alerts=0,
    ),
]

