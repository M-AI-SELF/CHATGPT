# Ω-0008 :: DNA CAPSULE ENGINE

## Purpose

Make a sovereign World portable across Runtime instances without losing its identity, artifacts, chapters or event history.

## Export / Import Swimlane

```text
WORLD OWNER       RUNTIME A        CAPSULE BUILDER       TRANSFER       RUNTIME B
    |                  |                  |                  |               |
    | request export   |                  |                  |               |
    |----------------->|                  |                  |               |
    |                  | snapshot World   |                  |               |
    |                  |----------------->|                  |               |
    |                  |                  | canonical JSON   |               |
    |                  |                  | SHA-256 digest   |               |
    |                  |                  |----------------->|               |
    |                  |                  |                  | deliver       |
    |                  |                  |                  |-------------->|
    |                  |                  |                  |               | parse
    |                  |                  |                  |               | verify hash
    |                  |                  |                  |               | replay events
    |                  |                  |                  |               | compare snapshot
    |                  |                  |                  |               | verify checkpoint
    |                  |                  |                  |               | commit state
    |<-----------------------------------------------------------------------|
    |                         WORLD RESTORED                                |
```

## Implemented

- UTF-8 JSON capsule format, schema version 1
- World manifest and identity metadata
- Artifact and Chapter snapshots
- ordered event history and checkpoint
- canonical SHA-256 integrity digest
- file export and object/file import
- replay-based fingerprint verification
- atomic import: failed validation leaves target World untouched
- detached export payload: modifying returned capsule cannot mutate source World

## Security boundary

SHA-256 provides integrity checking, not cryptographic publisher authentication. Signed capsules and key management are future work.

## Acceptance

A new Runtime imports the capsule, replays its event history, and reproduces the exported World fingerprint. Tampering, unsupported schema versions and inconsistent snapshots are rejected.

## Next

Ω-0009 :: Artifact Graph + Lineage — make relationships between Artifacts first-class, validated and portable.
