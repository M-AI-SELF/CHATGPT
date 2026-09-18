# Ω-0003 :: Deterministic World Reconstruction

## Objective

Prove that a fresh Ω Runtime instance can reconstruct the same World from immutable Events.

## Swimlane

```text
HUMAN          RUNTIME A          EVENT STORE          RUNTIME B
  |                |                   |                   |
  | Create World   |                   |                   |
  |--------------->|                   |                   |
  |                | Create Artifact   |                   |
  |                |------------------>| ArtifactCreated   |
  |                |                   |------------------>| Replay
  |                |                   |                   |
  |                | Checkpoint        |                   |
  |                |                   |                   |
  |                X Runtime ends      |                   |
  |                                    |                   |
  |                                    |<------------------|
  |                                    |    load events    |
  |                                    |------------------>| 
  |                                    |                   | Rebuild World
  |                                    |                   |
  |                                    |                   | Fingerprint
  |                                    |<------------------|
  |             VERIFIED: fingerprint A == fingerprint B   |
```

## Contract

State equals Replay of Events.

A reconstruction is successful when event validation passes, artifacts are reconstructed, the World fingerprint matches the original, and the second runtime requires no state from the first runtime.

## Current implementation

- append-only JSONL event persistence
- event validation
- deterministic artifact replay
- canonical World fingerprint using SHA-256
- fresh-runtime reconstruction tests

## Next

Ω-0004 will persist and restore semantic checkpoints.
