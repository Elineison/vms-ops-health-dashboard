from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List


@dataclass
class ModuleProbe:
    name: str
    domain: str
    state: str
    cameras_expected: int
    cameras_running: int
    last_frame_age_p95_s: float
    inference_p95_ms: float
    restart_total_24h: int
    open_events: int
    last_event_hours_ago: float | None
    alert_channel_state: str

    def issues(self) -> list[dict]:
        issues = []
        if self.state != 'online':
            issues.append({'severity': 'critical', 'reason': 'worker_offline'})
        if self.cameras_running < self.cameras_expected:
            issues.append({'severity': 'warning', 'reason': 'camera_not_running'})
        if self.last_frame_age_p95_s > 20:
            issues.append({'severity': 'warning', 'reason': 'stale_frames'})
        if self.inference_p95_ms > 950:
            issues.append({'severity': 'warning', 'reason': 'slow_inference'})
        if self.alert_channel_state != 'ok':
            issues.append({'severity': 'critical', 'reason': 'alert_channel_failed'})
        return issues

    def alert_silence(self) -> dict:
        if self.last_event_hours_ago is None:
            status = 'no_history'
            note = 'No synthetic event history is available for this module.'
        elif self.last_event_hours_ago > 72 and self.state == 'online' and self.cameras_running == self.cameras_expected:
            status = 'quiet_but_healthy'
            note = 'No recent event, but worker, cameras and alert channel are healthy.'
        elif self.last_event_hours_ago > 72:
            status = 'needs_probe'
            note = 'No recent event and at least one runtime check needs attention.'
        else:
            status = 'recent_events'
            note = 'Events were observed inside the expected review window.'
        return {
            'module': self.name,
            'domain': self.domain,
            'last_event_hours_ago': self.last_event_hours_ago,
            'status': status,
            'note': note,
        }

    def payload(self) -> dict:
        return {
            'name': self.name,
            'domain': self.domain,
            'state': self.state,
            'cameras_expected': self.cameras_expected,
            'cameras_running': self.cameras_running,
            'last_frame_age_p95_s': self.last_frame_age_p95_s,
            'inference_p95_ms': self.inference_p95_ms,
            'restart_total_24h': self.restart_total_24h,
            'open_events': self.open_events,
            'last_event_hours_ago': self.last_event_hours_ago,
            'alert_channel_state': self.alert_channel_state,
            'issues': self.issues(),
        }


PROBES: List[ModuleProbe] = [
    ModuleProbe(
        name='elevator-analytics-a',
        domain='elevator_dwell',
        state='online',
        cameras_expected=18,
        cameras_running=18,
        last_frame_age_p95_s=1.8,
        inference_p95_ms=142.0,
        restart_total_24h=0,
        open_events=0,
        last_event_hours_ago=74.0,
        alert_channel_state='ok',
    ),
    ModuleProbe(
        name='carona-access-a',
        domain='access_carona',
        state='online',
        cameras_expected=6,
        cameras_running=6,
        last_frame_age_p95_s=2.1,
        inference_p95_ms=168.0,
        restart_total_24h=1,
        open_events=1,
        last_event_hours_ago=5.5,
        alert_channel_state='ok',
    ),
    ModuleProbe(
        name='sidewalk-monitoring-a',
        domain='sidewalk_dwell',
        state='online',
        cameras_expected=8,
        cameras_running=7,
        last_frame_age_p95_s=28.0,
        inference_p95_ms=214.0,
        restart_total_24h=3,
        open_events=0,
        last_event_hours_ago=91.0,
        alert_channel_state='ok',
    ),
]


def generated_at() -> str:
    return datetime.now(timezone.utc).isoformat()
