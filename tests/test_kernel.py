from pathlib import Path

import pytest

from runtime.omega import OmegaKernel, WorldState


def test_world_lifecycle() -> None:
    kernel = OmegaKernel()
    artifact = kernel.create_artifact("A-0001", "Test", "hello")
    checkpoint = kernel.checkpoint()
    kernel.restore(checkpoint)
    assert artifact["id"] == "A-0001"
    assert checkpoint["world_id"] == "omega-world"
    assert "A-0001" in checkpoint["artifact_ids"]


def test_event_persistence_and_deterministic_replay(tmp_path: Path) -> None:
    event_log = tmp_path / "events.jsonl"
    writer = OmegaKernel(event_log=event_log)
    writer.create_artifact("A-0001", "Seed", "hello")
    reader = OmegaKernel(event_log=event_log)
    rebuilt = reader.restore_from_event_log()
    assert rebuilt.artifacts == writer.state.artifacts
    assert reader.fingerprint() == writer.fingerprint()


def test_replay_is_independent_of_runtime_instance(tmp_path: Path) -> None:
    event_log = tmp_path / "events.jsonl"
    original = OmegaKernel(event_log=event_log)
    original.create_artifact("A-0001", "Seed", "hello")
    expected = original.fingerprint()
    restored = OmegaKernel(event_log=event_log)
    restored.restore_from_event_log()
    assert restored.fingerprint() == expected


def test_event_validation() -> None:
    kernel = OmegaKernel()
    with pytest.raises(ValueError):
        kernel.emit("", {})
    with pytest.raises(ValueError):
        kernel.emit("Invalid", [])  # type: ignore[arg-type]


def test_checkpoint_restore_verifies_fingerprint(tmp_path: Path) -> None:
    event_log = tmp_path / "events.jsonl"
    source = OmegaKernel(event_log=event_log)
    source.create_artifact("A-0001", "Seed", "hello")
    checkpoint = source.checkpoint()
    restored = OmegaKernel(event_log=event_log)
    restored.restore_checkpoint(checkpoint)
    assert restored.fingerprint() == checkpoint["fingerprint"]


def test_checkpoint_restore_rejects_mismatch(tmp_path: Path) -> None:
    event_log = tmp_path / "events.jsonl"
    source = OmegaKernel(event_log=event_log)
    source.create_artifact("A-0001", "Seed", "hello")
    checkpoint = source.checkpoint()
    checkpoint["fingerprint"] = "tampered"
    restored = OmegaKernel(event_log=event_log)
    with pytest.raises(ValueError, match="fingerprint"):
        restored.restore_checkpoint(checkpoint)


def test_cognitive_diff() -> None:
    kernel = OmegaKernel()
    before = WorldState(world_id="omega-world", artifacts={"A": {"id": "A", "content": "old"}})
    after = WorldState(world_id="omega-world", artifacts={"A": {"id": "A", "content": "new"}, "B": {"id": "B", "content": "added"}})
    diff = kernel.cognitive_diff(before, after)["cognitive_diff"]
    assert diff["added"] == ["B"]
    assert diff["changed"] == ["A"]
    assert diff["removed"] == []

def test_chronicle_generation() -> None:
    kernel = OmegaKernel()
    kernel.create_artifact("A-0001", "Seed", "hello")
    chronicle = kernel.generate_chronicle("Genesis Chronicle")
    assert chronicle["type"] == "chronicle"
    assert chronicle["title"] == "Genesis Chronicle"
    assert chronicle["event_count"] == 1
    assert chronicle["timeline"][0]["type"] == "ArtifactCreated"
    assert chronicle["world_fingerprint"] == kernel.fingerprint()
