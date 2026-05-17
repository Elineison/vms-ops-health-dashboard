from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, PlainTextResponse

from app.probes import PROBES, generated_at


app = FastAPI(
    title='VMS Operations Health Dashboard',
    version='2.0.0',
    description='Public case study for operational health checks across elevator, carona and sidewalk analytics modules.',
)


@app.get('/', response_class=HTMLResponse)
def index() -> str:
    return '''
    <main style="font-family:system-ui;max-width:920px;margin:40px auto;line-height:1.5">
      <p style="text-transform:uppercase;font-size:12px;letter-spacing:.08em;color:#476582">public case study</p>
      <h1>VMS Operations Health Dashboard</h1>
      <p>
        Sanitized observability service for video analytics operations: module health,
        camera freshness, inference latency, alert-channel state and alert-silence checks.
      </p>
      <ul>
        <li><a href="/api/operations/snapshot">Operations snapshot</a></li>
        <li><a href="/api/alerts/silence-check">Alert silence check</a></li>
        <li><a href="/metrics">Prometheus-style metrics</a></li>
      </ul>
    </main>
    '''


@app.get('/api/modules')
def modules() -> list[dict]:
    return [probe.payload() for probe in PROBES]


@app.get('/api/operations/snapshot')
def operations_snapshot() -> dict:
    module_payloads = modules()
    issues = [
        {'module': module['name'], 'domain': module['domain'], **issue}
        for module in module_payloads
        for issue in module['issues']
    ]
    critical = any(issue['severity'] == 'critical' for issue in issues)
    return {
        'service': 'vms-ops-health-dashboard',
        'generated_at': generated_at(),
        'state': 'CRITICAL' if critical else ('DEGRADED' if issues else 'HEALTHY'),
        'modules_total': len(module_payloads),
        'cameras_expected': sum(module['cameras_expected'] for module in module_payloads),
        'cameras_running': sum(module['cameras_running'] for module in module_payloads),
        'open_events': sum(module['open_events'] for module in module_payloads),
        'issues': issues,
        'modules': module_payloads,
    }


@app.get('/api/alerts/silence-check')
def alert_silence_check() -> dict:
    checks = [probe.alert_silence() for probe in PROBES]
    return {
        'service': 'vms-ops-health-dashboard',
        'generated_at': generated_at(),
        'checks': checks,
        'operator_note': 'No alert since Friday is not treated as failure by itself; frame freshness, worker state and alert-channel state decide whether to probe further.',
    }


@app.get('/api/health')
def health() -> dict:
    snapshot = operations_snapshot()
    return {
        'service': snapshot['service'],
        'state': snapshot['state'],
        'issues': snapshot['issues'],
    }


@app.get('/metrics', response_class=PlainTextResponse)
def metrics() -> str:
    lines = [
        '# HELP vms_module_online Module online state.',
        '# TYPE vms_module_online gauge',
    ]
    for probe in PROBES:
        labels = f'module="{probe.name}",domain="{probe.domain}"'
        online = 1 if probe.state == 'online' else 0
        lines.append(f'vms_module_online{{{labels}}} {online}')
        lines.append(f'vms_cameras_running{{{labels}}} {probe.cameras_running}')
        lines.append(f'vms_cameras_expected{{{labels}}} {probe.cameras_expected}')
        lines.append(f'vms_frame_age_p95_seconds{{{labels}}} {probe.last_frame_age_p95_s}')
        lines.append(f'vms_inference_p95_ms{{{labels}}} {probe.inference_p95_ms}')
        lines.append(f'vms_module_restarts_24h{{{labels}}} {probe.restart_total_24h}')
        lines.append(f'vms_open_events{{{labels}}} {probe.open_events}')
    return '\n'.join(lines) + '\n'
