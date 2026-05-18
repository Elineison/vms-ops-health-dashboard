# VMS Operations Health Dashboard

Módulo FastAPI que representa a camada de saúde operacional para servidores VMS, workers de stream e módulos de detecção.

## O Que Significa VMS Aqui

VMS significa Sistema de Gerenciamento de Vídeo: a camada que centraliza câmeras, DVRs/NVRs, streams ao vivo, gravações, eventos, alertas e integrações. Neste repositório, o foco é acompanhar se essa base operacional e os módulos conectados continuam entregando vídeo, eventos, métricas e alertas corretamente.

## O Que o Sistema Faz

- Consolida status de módulos de elevador, acesso carona e calçadas.
- Mostra câmeras esperadas, câmeras rodando, idade de frames, latência de inferência e restarts.
- Identifica problemas como worker offline, câmera sem frame recente, inferência lenta e canal de alerta com falha.
- Inclui checagem de silêncio de alerta para diferenciar ausência real de eventos de falha operacional.
- Expõe métricas no formato Prometheus.

## Contexto Representado

- Servidores VMS com Hikvision e família Dahua/Intelbras.
- Workers de streaming em tempo real.
- Módulos de detecção integrados à operação.
- APIs de saúde para suporte e diagnóstico.

## Endpoints

- `GET /` - página simples com links do módulo.
- `GET /api/modules` - status individual dos módulos.
- `GET /api/operations/snapshot` - visão consolidada da operação.
- `GET /api/alerts/silence-check` - análise de silêncio de alerta.
- `GET /api/health` - saúde geral.
- `GET /metrics` - métricas estilo Prometheus.

## Rodar Localmente

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8014
```

## Testar

```bash
curl http://127.0.0.1:8014/api/modules
curl http://127.0.0.1:8014/api/operations/snapshot
curl http://127.0.0.1:8014/api/alerts/silence-check
curl http://127.0.0.1:8014/metrics
```

## Escopo Público

Todos os módulos, contadores, latências e históricos são sintéticos. Não há logs reais, IPs privados, credenciais, dashboards internos, SDKs proprietários, destinos de alerta ou dados de clientes.
