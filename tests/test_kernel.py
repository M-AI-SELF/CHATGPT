import json
import hashlib
from pathlib import Path

import pytest

from runtime.omega import OmegaKernel
from runtime.omega.kernel import WorldState


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


def test_chapter_lifecycle_and_replay(tmp_path: Path) -> None:
    event_log = tmp_path / "events.jsonl"
    kernel = OmegaKernel(event_log=event_log)
    kernel.create_artifact("A-CH", "Chapter Artifact", "content")
    kernel.create_chapter("CH-0001", "Genesis", ["Establish continuity"])
    kernel.attach_artifact_to_chapter("CH-0001", "A-CH")
    chapter = kernel.publish_chapter("CH-0001", ["Initial chapter published"])
    assert chapter["status"] == "published"
    assert chapter["artifacts"] == ["A-CH"]
    assert chapter["chronicle"]["related_chapters"] == ["CH-0001"]
    assert len(chapter["checkpoints"]) == 1
    restored = OmegaKernel(event_log=event_log)
    restored.restore_from_event_log()
    assert restored.state.chapters["CH-0001"] == chapter
    assert restored.fingerprint() == kernel.fingerprint()


def test_published_chapter_is_immutable() -> None:
    kernel = OmegaKernel()
    kernel.create_artifact("A-1", "Artifact", "content")
    kernel.create_chapter("CH-1", "Chapter")
    kernel.publish_chapter("CH-1")
    with pytest.raises(ValueError):
        kernel.attach_artifact_to_chapter("CH-1", "A-1")


def test_capsule_round_trip_preserves_world(tmp_path: Path) -> None:
    source = OmegaKernel(identity={"owner": "creator", "sovereignty": True})
    source.create_artifact("A-CAP", "Capsule Artifact", "portable content")
    source.create_chapter("CH-CAP", "Capsule Chapter", ["Preserve continuity"])
    source.attach_artifact_to_chapter("CH-CAP", "A-CAP")
    source.publish_chapter("CH-CAP", ["Capsule release"])
    expected_fingerprint = source.fingerprint()
    capsule_path = tmp_path / "world.dna.json"
    capsule = source.export_capsule(capsule_path)
    target = OmegaKernel(world_id="temporary-world")
    target.import_capsule(capsule_path)
    assert target.state.world_id == "omega-world"
    assert target.fingerprint() == expected_fingerprint
    assert target.identity == {"owner": "creator", "sovereignty": True}
    assert target.state.chapters["CH-CAP"]["status"] == "published"


def test_capsule_rejects_tampering() -> None:
    source = OmegaKernel()
    source.create_artifact("A-TAMPER", "Original", "safe")
    capsule = source.export_capsule()
    capsule["world"]["artifacts"]["A-TAMPER"]["content"] = "tampered"
    target = OmegaKernel()
    with pytest.raises(ValueError, match="integrity"):
        target.import_capsule(capsule)


def test_capsule_rejects_unsupported_schema() -> None:
    source = OmegaKernel()
    capsule = source.export_capsule()
    capsule["schema_version"] = 99
    unsigned = {key: value for key, value in capsule.items() if key != "integrity"}
    capsule["integrity"]["digest"] = __import__("hashlib").sha256(
        json.dumps(unsigned, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    target = OmegaKernel()
    with pytest.raises(ValueError, match="schema version"):
        target.import_capsule(capsule)


def test_capsule_export_is_detached_from_live_world() -> None:
    source = OmegaKernel()
    source.create_artifact("A-DETACH", "Original", "source")
    capsule = source.export_capsule()
    capsule["world"]["artifacts"]["A-DETACH"]["content"] = "external mutation"
    assert source.state.artifacts["A-DETACH"]["content"] == "source"


def test_failed_capsule_import_does_not_mutate_target() -> None:
    source = OmegaKernel()
    source.create_artifact("A-SOURCE", "Source", "data")
    capsule = source.export_capsule()
    capsule["integrity"]["digest"] = "invalid"
    target = OmegaKernel(world_id="target-world")
    target.create_artifact("A-LOCAL", "Local", "keep")
    before = target.fingerprint()
    with pytest.raises(ValueError, match="integrity"):
        target.import_capsule(capsule)
    assert target.state.world_id == "target-world"
    assert target.fingerprint() == before


def test_artifact_graph_relationships_and_lineage(tmp_path: Path) -> None:
    event_log = tmp_path / "events.jsonl"
    kernel = OmegaKernel(event_log=event_log)
    kernel.create_artifact("A-ROOT", "Root", "root")
    kernel.create_artifact("A-MID", "Middle", "middle")
    kernel.create_artifact("A-LEAF", "Leaf", "leaf")
    kernel.add_artifact_relationship("A-MID", "derived_from", "A-ROOT")
    kernel.add_artifact_relationship("A-LEAF", "derived_from", "A-MID")
    graph = kernel.validate_artifact_graph()
    assert graph["valid"] is True
    assert graph["relationship_count"] == 2
    lineage = kernel.artifact_lineage("A-LEAF")
    assert lineage["ancestors"] == ["A-MID", "A-ROOT"]
    restored = OmegaKernel(event_log=event_log)
    restored.restore_from_event_log()
    assert restored.state.relationships == kernel.state.relationships
    assert restored.fingerprint() == kernel.fingerprint()


def test_artifact_graph_rejects_dangling_relationship() -> None:
    kernel = OmegaKernel()
    kernel.create_artifact("A-1", "One", "one")
    with pytest.raises(KeyError):
        kernel.add_artifact_relationship("A-1", "depends_on", "MISSING")


def test_artifact_graph_rejects_lineage_cycle() -> None:
    kernel = OmegaKernel()
    kernel.create_artifact("A-1", "One", "one")
    kernel.create_artifact("A-2", "Two", "two")
    kernel.add_artifact_relationship("A-1", "derived_from", "A-2")
    with pytest.raises(ValueError, match="cycle"):
        kernel.add_artifact_relationship("A-2", "derived_from", "A-1")


def test_capsule_round_trip_preserves_artifact_graph() -> None:
    source = OmegaKernel()
    source.create_artifact("A-ROOT", "Root", "root")
    source.create_artifact("A-CHILD", "Child", "child")
    source.add_artifact_relationship("A-CHILD", "derived_from", "A-ROOT")
    capsule = source.export_capsule()
    target = OmegaKernel()
    target.import_capsule(capsule)
    assert target.state.relationships == source.state.relationships
    assert target.fingerprint() == source.fingerprint()


def test_cognitive_diff_includes_relationship_changes() -> None:
    kernel = OmegaKernel()
    before = WorldState(world_id="omega-world", artifacts={"A": {"id": "A"}, "B": {"id": "B"}})
    after = WorldState(
        world_id="omega-world",
        artifacts={"A": {"id": "A"}, "B": {"id": "B"}},
        relationships=[{"source": "B", "type": "derived_from", "target": "A"}],
    )
    diff = kernel.cognitive_diff(before, after)["cognitive_diff"]
    assert diff["relationships"]["added"] == [{"source": "B", "type": "derived_from", "target": "A"}]


def test_cognitive_diff_includes_relationship_changes() -> None:
    kernel = OmegaKernel()
    before = WorldState(world_id="omega-world", artifacts={"A": {"id": "A"}, "B": {"id": "B"}})
    after = WorldState(
        world_id="omega-world",
        artifacts={"A": {"id": "A"}, "B": {"id": "B"}},
        relationships=[{"source": "B", "type": "derived_from", "target": "A"}],
    )
    diff = kernel.cognitive_diff(before, after)["cognitive_diff"]
    assert diff["relationships"]["added"] == [{"source": "B", "type": "derived_from", "target": "A"}]


def test_capsule_v1_remains_importable() -> None:
    source = OmegaKernel()
    source.create_artifact("A-V1", "Legacy", "compatible")
    capsule = source.export_capsule()
    legacy_state = {
        "world_id": source.state.world_id,
        "status": source.state.status,
        "mode": source.state.mode,
        "artifacts": source.state.artifacts,
        "chapters": source.state.chapters,
    }
    legacy_fingerprint = hashlib.sha256(json.dumps(legacy_state, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
    capsule["schema_version"] = 1
    capsule["manifest"]["fingerprint"] = legacy_fingerprint
    capsule["checkpoint"]["fingerprint"] = legacy_fingerprint
    capsule["world"].pop("relationships", None)
    unsigned = {key: value for key, value in capsule.items() if key != "integrity"}
    capsule["integrity"]["digest"] = hashlib.sha256(json.dumps(unsigned, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
    target = OmegaKernel()
    target.import_capsule(capsule)
    assert target.state.artifacts == source.state.artifacts
