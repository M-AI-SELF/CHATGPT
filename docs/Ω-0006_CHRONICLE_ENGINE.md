# Ω-0006 :: CHRONICLE ENGINE

## Purpose

Turn verified World evolution into a durable Chronicle artifact.

## Lifecycle Swimlane

```text
HUMAN        KERNEL          EVENT STORE       DIFF        CHRONICLE       CHAPTER
  |             |                |              |             |              |
  | intent      |                |              |             |              |
  |------------>|                |              |             |              |
  |             | emit event     |              |             |              |
  |             |--------------->| persist      |             |              |
  |             |                |              |             |              |
  |             | replay         |------------->| compare     |              |
  |             |                |              |             |              |
  |             |                |              |-----------> | generate     |
  |             |                |              |             |              |
  |             |                |              |             |----------->   |
  |             |                |              |             |              | publish
  |             |                |              |             |              |
  |             | checkpoint     |              |             |              |
  |<------------|                |              |             |              |
```

## Chronicle Contract

A Chronicle records the durable history of a World evolution boundary. The current bootstrap implementation includes:

- stable Chronicle identity derived from event count
- World identity
- generation timestamp
- semantic event summary
- ordered event timeline
- contributors
- related chapters
- event count
- World fingerprint

The Chronicle is a derived artifact; the event stream remains the temporal source of truth.

## Ω Invariant

```text
EVENTS → REPLAY → DIFF → CHRONICLE
                    ↓
                CHECKPOINT
```

Chronicle generation does not mutate the World event stream.

## Next

Ω-0007 :: Chapter Engine — bind Chronicle + artifacts + checkpoints into explicit evolutionary Chapters.
