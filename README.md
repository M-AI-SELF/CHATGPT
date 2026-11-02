# M-AI-SELF :: Ω Runtime

> **The World belongs to the user.**  
> **The Runtime is replaceable.**  
> **The Artifacts endure.**

**A Personal Cognitive Operating Environment**  
*Artifact-driven · Runtime-agnostic · Local-first · Sovereign by design*

---

## What is M-AI-SELF?

M-AI-SELF is an open, modular Cognitive Operating Environment for creating, preserving, reconstructing, and evolving persistent cognitive Worlds.

It is not designed around isolated prompts or conversations. Its primary unit is the **World**: a durable environment containing identity, intent, knowledge, artifacts, decisions, history, capabilities, and runtime state.

The project separates the World from the software used to operate it:

- **World** — the portable, canonical semantic state owned by its creator.
- **Ω Runtime** — an interchangeable implementation that interprets and operates on a World.
- **Artifacts** — durable, versioned objects representing meaningful work and knowledge.
- **Events** — the append-only record of changes from which state can be reconstructed.

The long-term goal is an open World Specification that lets different AI systems reconstruct and continue a World according to their actual capabilities.

## The M / AI / SELF model

| Layer | Meaning |
|---|---|
| **M** | Human intent, identity, values, experience, purpose, and direction. |
| **AI** | Reasoning, planning, knowledge processing, execution, and tool orchestration. |
| **SELF** | The emergent, persistent cognitive environment formed through continuous human–AI collaboration. |

The system should augment human cognition, not replace human agency or ownership.

## Core philosophy

Everything meaningful becomes an **Artifact**.

Artifacts are organized into **Chapters**. Chapters contribute to **Chronicles**. Chronicles describe the evolution of a **World**. Worlds may connect through the **Forest Protocol** while retaining sovereignty.

**One canonical source → many renderers.**

README files, websites, PDFs, graphics, timelines, manga-style chronicles, presentations, and social publications are derived views of canonical project artifacts. They are not competing sources of truth.

## Architecture at a glance

```text
Human (M)
   │ intent, identity, values
   ▼
AI
   │ reasoning, planning, execution
   ▼
SELF
   │ persistent cognitive continuity
   ▼
Ω Runtime
   ├── World / Identity
   ├── Context & Memory
   ├── Artifact Knowledge Graph
   ├── Event Log & State Reconstruction
   ├── Planner & Capability Registry
   ├── Checkpoint Manager
   ├── Chronicle Engine
   ├── Spellbook Executor
   ├── Plugin / Agent Orchestration
   └── Renderer Pipeline
          │
          ▼
     Sovereign World
          │ optional connection
          ▼
     Forest Protocol
```

## Core modules and concepts

- **Ω Runtime** — cognitive kernel and execution environment.
- **World Model** — identity, goals, knowledge, artifacts, events, capabilities, and state.
- **Artifact Model** — immutable, versioned cognitive objects with semantic relationships.
- **Chapter System** — groups artifacts into meaningful evolutionary milestones.
- **Chronicle Engine** — turns event history into an intelligible narrative of the World's evolution.
- **Checkpoint Manager** — records validated recovery and continuity points.
- **World Snapshots / DNA Capsules** — portable, versioned snapshots for restore, migration, and sharing.
- **Spellbooks** — declarative, reusable semantic workflows that restore or transform context and state.
- **Embryo** — optional local perception layer that converts explicitly permitted device signals into semantic events; privacy and user control are foundational.
- **Forest Protocol** — interoperability and voluntary exchange between sovereign Worlds.
- **Tavern / Living Atlas** — proposed social spaces and discovery interfaces for connected Worlds.
- **Renderer Pipeline** — derives documentation, visual, web, PDF, and publication outputs from canonical Artifacts.
- **Multi-Agent Mesh** — agents with different capabilities collaborate through shared, inspectable World artifacts and events.

These names describe the intended architecture. A module is not considered implemented merely because it appears in this overview; see the implementation status below.

## Implemented foundation

The repository already contains an initial executable Ω Runtime nucleus.

The current README history and repository files record these verified milestones:

1. World creation.
2. Artifact creation.
3. Event emission.
4. Checkpoint creation.
5. Checkpoint restoration.
6. Append-only event persistence.
7. Deterministic World reconstruction by replaying persisted events.

**Current verified boundary:** a Runtime instance can be disposable while World state is reconstructed from persisted events.

This is an early executable foundation, not yet the complete Cognitive Operating Environment or a production-ready distributed network.

## Development status

| Area | Status |
|---|---|
| Repository bootstrap | Existing |
| Minimal executable Ω Kernel | Existing |
| Event persistence and replay | Existing milestone |
| World Specification | Draft / evolving |
| Full Artifact Knowledge Graph | Planned |
| Chronicle Engine | Planned |
| DNA Capsule interoperability | Planned |
| Spellbook execution | Planned |
| Embryo local perception | Concept / planned |
| Forest Protocol networking | Concept / planned |
| Living Atlas and Tavern | Concept / planned |
| Multi-agent orchestration | Planned |

Status labels distinguish **implemented**, **specified**, **prototype**, and **planned** work. No conceptual module should be represented as production-ready without tests and evidence.

## Repository map

```text
.anchor/          Runtime identity and bootstrap manifest
spec/             World, Runtime, Artifact, Event and workflow specifications
world/            Canonical World manifest, artifacts, events and checkpoints
runtime/omega/    Executable Ω Kernel
tests/            Runtime and lifecycle verification
docs/             Project overview and design documentation
assets/           Visual assets and diagrams
```

The repository is the canonical project record. Documentation should evolve alongside implementation.

## Development principles

1. **Sovereignty** — the creator owns the World and controls its data.
2. **Artifact-first** — meaningful work is represented by durable artifacts.
3. **Event sourcing** — changes are recorded; state is reconstructed from history.
4. **Continuity** — checkpoints and capsules support recovery and migration.
5. **Runtime independence** — no single model or provider owns the World.
6. **Local-first privacy** — sensitive signals remain local unless explicitly shared.
7. **Validation before mutation** — validate changes and preserve rollback paths.
8. **Capability honesty** — runtimes declare what they can and cannot reconstruct.
9. **One source of truth** — renderers derive outputs from canonical artifacts.
10. **Evolution with lineage** — every meaningful milestone is traceable.

## Roadmap

The initial foundation sequence is:

1. Repository identity and project overview.
2. World Specification.
3. Ω Runtime Specification.
4. Artifact Specification.
5. Chapter System.
6. Chronicle Engine.
7. Forest Protocol.
8. DNA Capsules and restoration.
9. Spellbooks.
10. Repository and renderer integration.

Implementation proceeds incrementally. Each milestone should have an artifact, tests where applicable, a checkpoint, and a Chronicle entry.

## Getting started

The project targets **Python 3.11+**. The runtime package and its actual commands are defined by the repository's `pyproject.toml` and source tree.

For the current architecture and contracts, begin with:

- [Project overview](docs/PROJECT_OVERVIEW.md)
- [World manifest](world/manifest.yaml)
- [Specifications](spec/)
- [Runtime implementation](runtime/omega/)
- [Tests](tests/)

## Collaboration

Contributions should preserve the World model, document architectural decisions, include validation, and clearly label implementation maturity. See [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## License

Licensing is not yet declared in this repository. A code license and a separate documentation/specification license should be selected before external reuse is invited.

---

**M-AI-SELF :: Ω Runtime**  
*Building Worlds instead of Conversations.*


## Ω-0007 :: CHAPTER ENGINE

The runtime now groups goals, Artifacts, Chronicles, Checkpoint snapshots and release notes into event-sourced Chapters. Chapters move from `open` to `published`; published Chapters reject further Artifact attachment. A fresh Runtime can reconstruct Chapter state by replaying the event log.

See `docs/Ω-0007_CHAPTER_ENGINE.md` for lifecycle and swimlane diagrams.


## Ω-0008 :: DNA CAPSULE ENGINE

Worlds can now be exported as portable JSON DNA Capsules and imported into a fresh Runtime. Capsules include identity metadata, World snapshots, Artifacts, Chapters, ordered Events and a Checkpoint. Import verifies the SHA-256 digest, replays the event history, checks the reconstructed fingerprint and commits state only after all validation gates pass.

See `spec/CAPSULE_SPECIFICATION.md` and `docs/Ω-0008_DNA_CAPSULE_ENGINE.md` for the format contract and export/import swimlane. SHA-256 provides integrity checking, not digital-signature authentication.


## Ω-0009 :: ARTIFACT GRAPH + LINEAGE

Artifacts now support typed, event-sourced relationships. The Runtime validates endpoints and lineage cycles, computes a canonical graph fingerprint, traverses ancestry, and includes relationship changes in Cognitive Diff. DNA Capsule schema v2 carries graph edges while retaining v1 import compatibility.

See `spec/ARTIFACT_GRAPH_SPECIFICATION.md` and `docs/Ω-0009_ARTIFACT_GRAPH_LINEAGE.md`.


## Ω Command Center :: Dashboard

A local-first, read-only dashboard renders the canonical World from the event log. It includes the World overview, artifact constellation, lineage counts, continuity health, recent Chronicle events and a Capability Registry surface reserved for the Ω-0010 integration.

Run it from the repository root:

```bash
python -m runtime.omega.dashboard
```

Then open [http://127.0.0.1:8765](http://127.0.0.1:8765). The dashboard polls the overview API every 15 seconds. If the API is not running, the page displays a clearly labelled preview. It does not mutate World state.

See `docs/DASHBOARD_SPECIFICATION.md`.
