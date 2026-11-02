# Ω Command Center :: Dashboard Specification v0.1

## Purpose

The Command Center is a read-only renderer of the canonical World. It is not a second database, an alternate state manager, or a privileged mutation surface.

## Data flow

```text
World Event Log → Ω Kernel Replay → Dashboard Overview API → Browser Renderer
                         │                    │
                         └─ graph validation  └─ polling /api/overview
```

## First release

- World identity and operating mode.
- Artifact, relationship, Chapter and event counts.
- Artifact constellation rendered from actual graph nodes and edges.
- Event Chronicle stream.
- Event replay, graph integrity and checkpoint availability indicators.
- Runtime Capability Registry descriptors and provider trust/permission metadata.
- Automatic refresh every 15 seconds and manual refresh.
- Preview mode when opened without the local API.

## Runtime contract

- `GET /` serves the dashboard.
- `GET /api/overview` returns a JSON read model reconstructed from the event log.
- `GET /health` returns process health.
- The server binds to `127.0.0.1` by default.
- The dashboard does not expose mutation endpoints.
- A failed replay is shown as degraded; it is never silently reported as healthy.

## Run

```bash
python -m runtime.omega.dashboard
```

Open `http://127.0.0.1:8765`.

The server uses Python's standard library and the existing Kernel. No frontend build chain or external dependency is required.
