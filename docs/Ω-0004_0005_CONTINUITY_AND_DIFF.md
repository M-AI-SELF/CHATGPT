# Ω-0004 → Ω-0005 :: Continuity + Cognitive Diff

## Ω-0004 — World Restore

Checkpoint restoration verifies the World fingerprint after replaying persisted events.

```text
CHECKPOINT → LOAD EVENTS → REPLAY → FINGERPRINT → VERIFY → RESTORE
```

A tampered checkpoint fingerprint is rejected.

## Ω-0005 — Cognitive Diff

The kernel compares two World states and classifies artifact-level changes:
- added
- changed
- removed

The diff also carries reserved fields for decisions, goals and relationships, plus a semantic summary and next objective.

## Lane

```text
WORLD A       DIFF ENGINE        WORLD B
  |               |                |
  |-------------->|                |
  |               |<---------------|
  |               | compare        |
  |               | added          |
  |               | changed        |
  |               | removed        |
  |               | semantic summary|
  |               | next objective |
  |               |--------------->|
```

## Ship rule

Every accepted diff is an auditable development boundary: implementation, tests and checkpoint documentation advance together.

## Next milestone

Ω-0006 :: Chronicle Engine — convert verified World evolution into durable Chronicle artifacts.
