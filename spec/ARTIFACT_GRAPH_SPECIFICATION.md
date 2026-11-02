# ARTIFACT GRAPH & LINEAGE SPECIFICATION v1

## Relationship edge

```yaml
source: ARTIFACT_ID
type: derived_from
target: ARTIFACT_ID
```

## Supported relationship types

- `references`
- `depends_on`
- `extends`
- `implements`
- `belongs_to`
- `derived_from`
- `generated_by`
- `duplicates`
- `contradicts`
- `supports`
- `explains`

## Validation rules

1. Both endpoints must reference existing Artifacts.
2. Relationship types must belong to the supported vocabulary.
3. Duplicate edges are idempotent.
4. `derived_from`, `depends_on` and `extends` form the acyclic lineage subset; cycles are rejected.
5. The canonical graph fingerprint includes Artifact records and sorted relationship edges.
6. Relationship creation is recorded as `ArtifactRelationshipCreated` and reconstructed by event replay.

## Lineage query

`artifact_lineage(artifact_id)` returns the selected Artifact, its transitive ancestors through the acyclic lineage subset, and its directly connected relationships.

## Capsule integration

DNA Capsule v1 snapshots include `world.relationships`. Import verifies that this graph snapshot exactly matches the graph reconstructed from the event stream before committing the candidate World.

## Cognitive Diff

Relationship additions and removals are included under `cognitive_diff.relationships`.
