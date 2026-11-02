from __future__ import annotations

import json

from runtime.omega.dashboard import build_overview


def _event(event_type: str, payload: dict) -> dict:
    return {"type": event_type, "timestamp": "2026-11-02T10:00:00+00:00", "payload": payload}


def test_dashboard_reconstructs_world_metrics(tmp_path):
    log = tmp_path / "events.jsonl"
    events = [
        _event("ArtifactCreated", {"artifact": {"id": "a1", "title": "Seed", "type": "text", "version": "1.0.0", "content": "seed"}}),
        _event("ArtifactCreated", {"artifact": {"id": "a2", "title": "Kernel", "type": "text", "version": "1.0.0", "content": "kernel"}}),
        _event("ArtifactRelationshipCreated", {"relationship": {"source": "a2", "type": "derived_from", "target": "a1"}}),
        _event("ChapterCreated", {"chapter": {"id": "c1", "title": "Genesis", "goals": [], "artifacts": [], "chronicle": None, "checkpoints": [], "release_notes": [], "status": "open"}}),
    ]
    log.write_text("\n".join(json.dumps(event) for event in events) + "\n", encoding="utf-8")

    result = build_overview(log)

    assert result["source"] == "live"
    assert result["metrics"] == {"artifacts": 2, "relationships": 1, "chapters": 1, "events": 4}
    assert result["health"]["event_replay"] == "HEALTHY"
    assert result["health"]["graph_integrity"] == "VALID"
    assert result["artifacts"][0]["id"] == "a1"


def test_dashboard_empty_log_is_a_valid_empty_world(tmp_path):
    result = build_overview(tmp_path / "missing.jsonl")
    assert result["metrics"] == {"artifacts": 0, "relationships": 0, "chapters": 0, "events": 0}
    assert result["health"]["event_replay"] == "HEALTHY"


def test_dashboard_reports_corrupt_event_log(tmp_path):
    log = tmp_path / "events.jsonl"
    log.write_text("{not-json}\n", encoding="utf-8")
    result = build_overview(log)
    assert result["health"]["event_replay"] == "DEGRADED"
    assert result["error"]


def test_dashboard_exposes_kernel_capabilities(tmp_path):
    result = build_overview(tmp_path / "missing.jsonl")
    capability_ids = {item["id"] for item in result["capabilities"]}
    assert {"world.replay", "artifact.graph.validate", "checkpoint.create", "capsule.export", "capsule.import"} <= capability_ids
