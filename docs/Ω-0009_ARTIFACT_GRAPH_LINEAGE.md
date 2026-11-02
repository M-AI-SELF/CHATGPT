# Ω-0009 :: ARTIFACT GRAPH + LINEAGE ENGINE

## Purpose

Make Artifact relationships first-class World state. The graph is reconstructed from events, included in World fingerprints and carried inside DNA Capsules.

## Relationship vocabulary

`references`, `depends_on`, `extends`, `implements`, `belongs_to`, `derived_from`, `generated_by`, `duplicates`, `contradicts`, `supports`, `explains`.

## Graph lifecycle swimlane

```text
AUTHOR        Ω KERNEL        ARTIFACT INDEX       EVENT LOG       LINEAGE
  |               |                 |                  |              |
  | add edge      |                 |                  |              |
  |-------------->| validate refs   |                  |              |
  |               |---------------->| resolve endpoints|              |
  |               |<----------------|                  |              |
  |               | validate cycles |                  |              |
  |               |----------------------------------->| persist event|
  |               |                  |                 |              |
  | query lineage |                  |                 |              |
  |-------------->| traverse graph  |------------------------------->|
  |<--------------| ancestors + edges                                |
```

## Implemented contracts

- Relationship endpoints must exist.
- Relationship types are validated against a fixed vocabulary.
- Duplicate edges are idempotent.
- `derived_from`, `depends_on` and `extends` are cycle-checked.
- Relationship creation is event-sourced.
- Graph fingerprint is canonical and deterministic.
- Lineage query returns transitive ancestors.
- Cognitive Diff includes added and removed relationship edges.
- DNA Capsule snapshots include graph edges; import checks them against replayed history.

## Next

Ω-0010 :: Runtime Capability Registry — declare, inspect and resolve capabilities without binding the World to one AI provider.
