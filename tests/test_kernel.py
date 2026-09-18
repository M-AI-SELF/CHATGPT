from pathlib import Path

import pytest

from runtime.omega import OmegaKernel


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
        kernel.emit("Invalid", [])
