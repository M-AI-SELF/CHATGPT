"""Read-only HTTP dashboard for the M-AI-SELF Ω Runtime.

Run from the repository root:
    python -m runtime.omega.dashboard
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from .kernel import OmegaKernel

ROOT = Path(__file__).resolve().parents[2]
DASHBOARD_FILE = ROOT / "apps" / "dashboard" / "index.html"
DEFAULT_EVENT_LOG = ROOT / "world" / "events" / "events.jsonl"


def build_overview(event_log: str | Path = DEFAULT_EVENT_LOG, world_id: str = "omega-world") -> dict[str, Any]:
    """Reconstruct a read-only dashboard view from the canonical event log."""
    log_path = Path(event_log)
    kernel = OmegaKernel(world_id=world_id, event_log=log_path)
    events: list[dict[str, Any]] = []
    replay_ok = True
    error: str | None = None
    if log_path.exists():
        try:
            events = kernel.load_events()
            kernel.replay(events)
        except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
            replay_ok = False
            error = str(exc)
    graph = {"valid": True, "artifact_count": 0, "relationship_count": 0}
    if replay_ok:
        try:
            graph = kernel.validate_artifact_graph()
        except (ValueError, KeyError) as exc:
            replay_ok = False
            error = str(exc)
    state = kernel.state
    recent_events = []
    for event in events[-12:]:
        payload = event.get("payload", {})
        summary = (
            payload.get("artifact", {}).get("title")
            or payload.get("chapter", {}).get("title")
            or payload.get("relationship", {}).get("type")
            or payload.get("status")
            or payload.get("mode")
            or "World state transition"
        )
        recent_events.append({
            "type": event.get("type", "UnknownEvent"),
            "timestamp": event.get("timestamp", ""),
            "summary": str(summary),
        })
    checkpoint_files = list((ROOT / "world" / "checkpoints").glob("*.yaml"))
    return {
        "source": "live",
        "world": {"id": state.world_id, "name": "M-AI-SELF :: Ω Runtime", "status": state.status, "mode": state.mode},
        "identity": {"owner": kernel.identity.get("owner", "user"), "sovereignty": bool(kernel.identity.get("sovereignty", True))},
        "metrics": {
            "artifacts": len(state.artifacts),
            "relationships": len(state.relationships),
            "chapters": len(state.chapters),
            "events": len(events),
        },
        "health": {
            "event_replay": "HEALTHY" if replay_ok else "DEGRADED",
            "graph_integrity": "VALID" if graph.get("valid") else "INVALID",
            "checkpoint": "AVAILABLE" if checkpoint_files else "NOT FOUND",
            "runtime": "READ-ONLY",
        },
        "artifacts": [{"id": item["id"], "title": item.get("title", item["id"])} for item in state.artifacts.values()],
        "relationships": list(state.relationships),
        "chapters": [{"id": item["id"], "title": item.get("title", item["id"]), "status": item.get("status", "open")} for item in state.chapters.values()],
        "events": recent_events,
        "capabilities": [],
        "checkpoint": {"available": bool(checkpoint_files)},
        "error": error,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


class DashboardHandler(BaseHTTPRequestHandler):
    event_log = DEFAULT_EVENT_LOG
    world_id = "omega-world"

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path == "/api/overview":
            body = json.dumps(build_overview(self.event_log, self.world_id), ensure_ascii=False).encode("utf-8")
            self._send(200, body, "application/json; charset=utf-8")
            return
        if path in ("/", "/index.html"):
            try:
                body = DASHBOARD_FILE.read_bytes()
            except OSError:
                self._send(404, b"Dashboard asset not found.", "text/plain; charset=utf-8")
                return
            self._send(200, body, "text/html; charset=utf-8")
            return
        if path == "/health":
            self._send(200, b'{"status":"ok","mode":"read-only"}', "application/json")
            return
        self._send(404, b"Not found.", "text/plain; charset=utf-8")

    def _send(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt: str, *args: Any) -> None:
        return


def main() -> None:
    parser = argparse.ArgumentParser(description="Serve the read-only Ω Command Center.")
    parser.add_argument("--host", default="127.0.0.1", help="Bind address (default: localhost only).")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--event-log", type=Path, default=DEFAULT_EVENT_LOG)
    parser.add_argument("--world-id", default="omega-world")
    args = parser.parse_args()
    handler = type("ConfiguredDashboardHandler", (DashboardHandler,), {"event_log": args.event_log, "world_id": args.world_id})
    server = ThreadingHTTPServer((args.host, args.port), handler)
    print(f"Ω Command Center: http://{args.host}:{args.port}")
    print(f"World event log: {args.event_log}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down Ω Command Center.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
