"""Minimal executable Ω Kernel."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class WorldState:
    world_id: str
    status: str = "active"
    mode: str = "build"
    artifacts: dict[str, dict[str, Any]] = field(default_factory=dict)
    events: list[dict[str, Any]] = field(default_factory=list)


class OmegaKernel:
    """Minimal kernel proving the core lifecycle."""

    def __init__(self, world_id: str = "omega-world") -> None:
        self.state = WorldState(world_id=world_id)

    def emit(self, event_type: str, payload: dict[str, Any]) -> dict[str, Any]:
        event = {
            "type": event_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "payload": payload,
        }
        self.state.events.append(event)
        return event

    def create_artifact(
        self, artifact_id: str, title: str, content: str, artifact_type: str = "text"
    ) -> dict[str, Any]:
        artifact = {
            "id": artifact_id,
            "type": artifact_type,
            "title": title,
            "version": "1.0.0",
            "content": content,
        }
        self.state.artifacts[artifact_id] = artifact
        self.emit("ArtifactCreated", {"artifact_id": artifact_id})
        return artifact

    def checkpoint(self) -> dict[str, Any]:
        return {
            "world_id": self.state.world_id,
            "status": self.state.status,
            "mode": self.state.mode,
            "artifact_ids": list(self.state.artifacts),
            "event_count": len(self.state.events),
        }

    def restore(self, checkpoint: dict[str, Any]) -> None:
        if checkpoint["world_id"] != self.state.world_id:
            raise ValueError("Checkpoint belongs to a different World.")
        self.state.status = checkpoint["status"]
        self.state.mode = checkpoint["mode"]
