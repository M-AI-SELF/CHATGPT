# DNA CAPSULE SPECIFICATION v1

## Purpose

A DNA Capsule is a portable, integrity-checked package of a sovereign World. It enables export from one Ω Runtime and reconstruction by another compatible Runtime.

## Format

- Container: UTF-8 JSON
- Format identifier: `m-ai-self-dna-capsule`
- Schema version: `1`
- Integrity: SHA-256 over canonical JSON excluding the `integrity` member

## Required members

- `format`: capsule format identifier
- `schema_version`: integer schema version
- `manifest`: World ID, export timestamp, runtime contract, event count and World fingerprint
- `identity`: ownership and sovereignty metadata
- `world`: state snapshot including status, mode, Artifacts and Chapters
- `events`: ordered event history used for reconstruction
- `checkpoint`: checkpoint metadata for the exported state
- `integrity`: algorithm and digest

## Export contract

1. Capture World metadata and event history.
2. Serialize to detached JSON-compatible values.
3. Canonicalize with sorted keys and compact separators.
4. Calculate SHA-256 digest.
5. Optionally write the capsule to a destination path.

## Import contract

1. Parse JSON or accept a capsule object.
2. Validate format and schema version.
3. Verify the SHA-256 digest.
4. Replay events in a temporary candidate Runtime.
5. Compare reconstructed fingerprint, checkpoint, snapshot and event count.
6. Commit candidate state to the target Runtime only after every validation gate passes.

## Safety invariants

- Failed import must not mutate the target World.
- Exported capsule data must not alias mutable in-memory World objects.
- Event history is the reconstruction source of truth.
- Snapshot and checkpoint are verification boundaries, not substitutes for event replay.
- SHA-256 detects accidental or unauthorized content changes when the digest is trusted; it is not a digital signature and does not establish publisher identity.

## Compatibility

Unknown format identifiers and schema versions are rejected. Future versions must define explicit migration behavior.
