# Ω-0007 :: CHAPTER ENGINE

## Purpose

A Chapter groups goals, Artifacts, a Chronicle, Checkpoints and release notes into one explicit evolutionary unit.

## Chapter lifecycle

```text
OPEN → ASSEMBLE → VALIDATE → CHRONICLE → CHECKPOINT → PUBLISH
  │         │          │           │           │          │
  │         │          │           │           │          └─ immutable boundary
  │         │          │           │           └─ recovery marker
  │         │          │           └─ narrative history
  │         │          └─ required goals / references
  │         └─ attach Artifacts
  └─ create Chapter with goals
```

## Swimlane

```text
AUTHOR          Ω KERNEL          WORLD STORE          CHRONICLE
  |                 |                  |                   |
  | create chapter |                  |                   |
  |---------------->| ChapterCreated   |                   |
  |                 |----------------->|                   |
  | attach artifact |                  |                   |
  |---------------->| ArtifactAttached|                   |
  |                 |----------------->|                   |
  | publish         |                  |                   |
  |---------------->| generate         |------------------>| Chronicle
  |                 | attach chronicle |                   |
  |                 |----------------->|                   |
  |                 | checkpoint       |                   |
  |                 |----------------->|                   |
  |                 | publish event    |                   |
  |<----------------|                  |                   |
  | Chapter published                |                   |
```

## Chapter schema (bootstrap)

- `id`, `title`, `goals`
- `artifacts`
- `chronicle`
- `checkpoints`
- `release_notes`
- `status`: `open` or `published`

## Runtime behavior

- Chapter creation and changes are event-sourced.
- Artifacts can be attached only while a Chapter is open.
- Publishing generates a Chronicle, records a checkpoint snapshot, and emits a publication event.
- Published Chapters reject further Artifact attachment.
- A fresh Runtime reconstructs Chapter state by replaying the event log.

## Scope note

This is the executable bootstrap lifecycle. Goal completion semantics, chapter reopening, signed releases and standalone checkpoint files remain future work.

## Next milestone

Ω-0008 :: Capsule Serialization — package a sovereign World into a portable, verifiable export.
