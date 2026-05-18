# VMS Operations Health Dashboard

Estudo de caso público para health checks operacionais em módulos de video analytics dentro de uma família operacional Dahua/Intelbras.

Este repositório modela a visão de suporte que considero importante em operações reais de segurança: os módulos estão online, as câmeras estão entregando frames recentes, a latência de inferência está aceitável, o canal de alerta está saudável e um período sem alertas significa operação tranquila ou problema técnico?

## Problema Operacional

Uma equipe de monitoramento não pode depender apenas de alertas. Um sistema pode estar saudável e simplesmente não ter incidentes, ou pode estar silencioso porque uma câmera travou, um worker parou ou um canal de alerta falhou. Este dashboard separa eventos operacionais de saúde técnica.

## O Que Este Projeto Demonstra

- Modelo de saúde para analytics de elevador, monitoramento de acesso carona e monitoramento de calçadas, tratando Dahua/Intelbras como uma única família operacional.
- Frescor de câmera, latência de inferência, contagem de restarts, eventos abertos e estado do canal de alerta.
- Checagem de silêncio de alerta para cenários como "nenhum alerta desde sexta-feira".
- Endpoint `/metrics` no estilo Prometheus para integrações de monitoramento.
- Payloads de API limpos e seguros para fluxos de suporte.

## Arquitetura

```text
probes de módulo -> snapshot operacional -> decisão de saúde
                 -> revisão de silêncio de alerta -> endpoint de métricas
```

## Rodar Localmente

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8014
```

Abra:

- `http://127.0.0.1:8014/`
- `http://127.0.0.1:8014/api/operations/snapshot`
- `http://127.0.0.1:8014/api/alerts/silence-check`
- `http://127.0.0.1:8014/metrics`

## Escopo Público e Seguro

Todos os módulos, contadores, latências, quantidades de câmeras e históricos de alerta são sintéticos. Não há dados de clientes, IPs privados, logs reais, credenciais, dashboards internos, SDKs proprietários, destinos de alerta ou registros de incidentes.

## Competências Representadas

Python, FastAPI, observabilidade, health checks, lógica de alertas, métricas estilo Prometheus, fluxos de suporte VMS e debugging operacional.
