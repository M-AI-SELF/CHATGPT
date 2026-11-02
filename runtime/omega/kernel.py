"""Executable Ω Kernel with persistence, deterministic reconstruction and checkpoints."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass
class WorldState:
    world_id: str
    status: str = "active"
    mode: str = "build"
    artifacts: dict[str, dict[str, Any]] = field(default_factory=dict)
    chapters: dict[str, dict[str, Any]] = field(default_factory=dict)
    events: list[dict[str, Any]] = field(default_factory=list)


class OmegaKernel:
    def __init__(self, world_id: str = "omega-world", event_log: str | Path | None = None) -> None:
        self.event_log = Path(event_log) if event_log is not None else None
        self.state = WorldState(world_id=world_id)

    def emit(self, event_type: str, payload: dict[str, Any]) -> dict[str, Any]:
        # Freeze payload at emission time so later in-memory mutations cannot rewrite history.
        frozen_payload = json.loads(json.dumps(payload, ensure_ascii=False, sort_keys=True))
        event = {"type": event_type, "timestamp": datetime.now(timezone.utc).isoformat(), "payload": frozen_payload}
        self._validate_event(event)
        self.state.events.append(event)
        self._persist_event(event)
        return event

    @staticmethod
    def _validate_event(event: dict[str, Any]) -> None:
        if not event.get("type"):
            raise ValueError("Event type is required.")
        if not isinstance(event.get("payload"), dict):
            raise ValueError("Event payload must be an object.")

    def _persist_event(self, event: dict[str, Any]) -> None:
        if self.event_log is None:
            return
        self.event_log.parent.mkdir(parents=True, exist_ok=True)
        with self.event_log.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")

    def create_artifact(self, artifact_id: str, title: str, content: str, artifact_type: str = "text") -> dict[str, Any]:
        if artifact_id in self.state.artifacts:
            raise ValueError(f"Artifact already exists: {artifact_id}")
        artifact = {"id": artifact_id, "type": artifact_type, "title": title, "version": "1.0.0", "content": content}
        self.state.artifacts[artifact_id] = artifact
        self.emit("ArtifactCreated", {"artifact": artifact})
        return artifact

    def checkpoint(self) -> dict[str, Any]:
        return {
            "world_id": self.state.world_id,
            "status": self.state.status,
            "mode": self.state.mode,
            "artifact_ids": sorted(self.state.artifacts),
            "event_count": len(self.state.events),
            "fingerprint": self.fingerprint(),
        }

    def fingerprint(self, state: WorldState | None = None) -> str:
        target = state or self.state
        canonical = {
            "world_id": target.world_id,
            "status": target.status,
            "mode": target.mode,
            "artifacts": target.artifacts,
            "chapters": target.chapters,
        }
        payload = json.dumps(canonical, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def restore(self, checkpoint: dict[str, Any]) -> None:
        if checkpoint["world_id"] != self.state.world_id:
            raise ValueError("Checkpoint belongs to a different World.")
        self.state.status = checkpoint["status"]
        self.state.mode = checkpoint["mode"]
        if checkpoint.get("fingerprint") and checkpoint["fingerprint"] != self.fingerprint():
            raise ValueError("Checkpoint fingerprint does not match current World.")

    def replay(self, events: list[dict[str, Any]]) -> WorldState:
        rebuilt = WorldState(world_id=self.state.world_id)
        for event in events:
            self._validate_event(event)
            self._apply_event(rebuilt, event)
        rebuilt.events = list(events)
        self.state = rebuilt
        return rebuilt

    def load_events(self) -> list[dict[str, Any]]:
        if self.event_log is None or not self.event_log.exists():
            return []
        with self.event_log.open("r", encoding="utf-8") as handle:
            return [json.loads(line) for line in handle if line.strip()]

    def restore_from_event_log(self) -> WorldState:
        return self.replay(self.load_events())

    def restore_checkpoint(self, checkpoint: dict[str, Any], events: list[dict[str, Any]] | None = None) -> WorldState:
        if checkpoint["world_id"] != self.state.world_id:
            raise ValueError("Checkpoint belongs to a different World.")
        source_events = self.load_events() if events is None else events
        restored = self.replay(source_events)
        if checkpoint.get("fingerprint") != self.fingerprint():
            raise ValueError("Restored World fingerprint does not match checkpoint.")
        self.state.status = checkpoint["status"]
        self.state.mode = checkpoint["mode"]
        return restored

    def cognitive_diff(self, before: WorldState, after: WorldState) -> dict[str, Any]:
        before_ids, after_ids = set(before.artifacts), set(after.artifacts)
        added = sorted(after_ids - before_ids)
        removed = sorted(before_ids - after_ids)
        changed = sorted(
            artifact_id for artifact_id in before_ids & after_ids
            if before.artifacts[artifact_id] != after.artifacts[artifact_id]
        )
        return {
            "cognitive_diff": {
                "added": added,
                "changed": changed,
                "removed": removed,
                "artifacts": {"added": added, "changed": changed, "removed": removed},
                "decisions": [],
                "goals": [],
                "relationships": [],
                "semantic_summary": f"{len(added)} added, {len(changed)} changed, {len(removed)} removed",
                "next_objective": "inspect changed artifacts" if changed else "continue",
            }
        }

    @staticmethod
    def _apply_event(state: WorldState, event: dict[str, Any]) -> None:
        event_type = event["type"]
        payload = event["payload"]
        if event_type == "ArtifactCreated":
            artifact = payload["artifact"]
            state.artifacts[artifact["id"]] = artifact
        elif event_type == "ArtifactArchived":
            state.artifacts.pop(payload["artifact_id"], None)
        elif event_type == "WorldStatusChanged":
            state.status = payload["status"]
        elif event_type == "WorldModeChanged":
            state.mode = payload["mode"]
        elif event_type == "ChapterCreated":
            chapter = payload["chapter"]
            state.chapters[chapter["id"]] = chapter
        elif event_type == "ChapterArtifactAttached":
            state.chapters[payload["chapter_id"]]["artifacts"].append(payload["artifact_id"])
        elif event_type == "ChapterChronicleAttached":
            state.chapters[payload["chapter_id"]]["chronicle"] = payload["chronicle"]
        elif event_type == "ChapterCheckpointAttached":
            state.chapters[payload["chapter_id"]]["checkpoints"].append(payload["checkpoint"])
        elif event_type == "ChapterPublished":
            state.chapters[payload["chapter_id"]]["status"] = "published"
            state.chapters[payload["chapter_id"]]["release_notes"] = payload["release_notes"]
        else:
            raise ValueError(f"Unsupported replay event: {event_type}")

    def create_chapter(self, chapter_id: str, title: str, goals: list[str] | None = None) -> dict[str, Any]:
        if chapter_id in self.state.chapters:
            raise ValueError(f"Chapter already exists: {chapter_id}")
        chapter = {"id": chapter_id, "title": title, "goals": list(goals or []), "artifacts": [], "chronicle": None, "checkpoints": [], "release_notes": [], "status": "open"}
        self.state.chapters[chapter_id] = chapter
        self.emit("ChapterCreated", {"chapter": chapter})
        return chapter

    def attach_artifact_to_chapter(self, chapter_id: str, artifact_id: str) -> None:
        if chapter_id not in self.state.chapters or artifact_id not in self.state.artifacts:
            raise KeyError("Chapter or Artifact does not exist.")
        chapter = self.state.chapters[chapter_id]
        if chapter["status"] != "open":
            raise ValueError("Artifacts can only be attached to open Chapters.")
        if artifact_id not in chapter["artifacts"]:
            chapter["artifacts"].append(artifact_id)
            self.emit("ChapterArtifactAttached", {"chapter_id": chapter_id, "artifact_id": artifact_id})

    def publish_chapter(self, chapter_id: str, release_notes: list[str] | None = None) -> dict[str, Any]:
        if chapter_id not in self.state.chapters:
            raise KeyError(f"Unknown Chapter: {chapter_id}")
        chapter = self.state.chapters[chapter_id]
        if chapter["status"] != "open":
            raise ValueError("Only open Chapters can be published.")
        chronicle = self.generate_chronicle(f"{chapter['title']} Chronicle")
        chronicle["related_chapters"] = [chapter_id]
        chapter["chronicle"] = chronicle
        self.emit("ChapterChronicleAttached", {"chapter_id": chapter_id, "chronicle": chronicle})
        snapshot = self.checkpoint()
        chapter["checkpoints"].append(snapshot)
        self.emit("ChapterCheckpointAttached", {"chapter_id": chapter_id, "checkpoint": snapshot})
        notes = list(release_notes or [])
        self.emit("ChapterPublished", {"chapter_id": chapter_id, "release_notes": notes})
        chapter["status"] = "published"
        chapter["release_notes"] = notes
        return chapter
    def generate_chronicle(self, title: str = "World Evolution") -> dict[str, Any]:
        """Generate a durable chronicle artifact from the current event stream."""
        events = list(self.state.events)
        diff_summary = self._event_diff_summary(events)
        chronicle = {
            "id": f"CHR-{len(events):04d}",
            "type": "chronicle",
            "title": title,
            "world_id": self.state.world_id,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "summary": diff_summary["semantic_summary"],
            "timeline": [
                {"index": index, "type": event["type"], "timestamp": event["timestamp"]}
                for index, event in enumerate(events, start=1)
            ],
            "major_decisions": [],
            "contributors": ["runtime"],
            "related_chapters": [],
            "event_count": len(events),
            "world_fingerprint": self.fingerprint(),
        }
        return chronicle

    @staticmethod
    def _event_diff_summary(events: list[dict[str, Any]]) -> dict[str, Any]:
        counts: dict[str, int] = {}
        for event in events:
            event_type = event["type"]
            counts[event_type] = counts.get(event_type, 0) + 1
        summary = ", ".join(f"{count} {kind}" for kind, count in sorted(counts.items()))
        return {"semantic_summary": summary or "No recorded events."}
