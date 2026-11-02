# M-AI-SELF :: Ω Runtime — Project Overview

> **Artifact:** ARTIFACT_0000  
> **Title:** THE SEED  
> **Document type:** Canonical project overview  
> **Status:** Draft v1.0  
> **Project state:** Active bootstrap  
> **Runtime target:** Python 3.11+  
> **Source of truth:** Git repository

## 1. Executive vision

M-AI-SELF is a modular Cognitive Operating Environment in which a person and AI systems collaboratively create and evolve a persistent cognitive World. The World is intended to outlive individual conversations, applications, models, and runtime providers.

A World is not merely a chat history or a folder of notes. It is a structured, versioned environment containing identity, intent, knowledge, artifacts, decisions, events, chapters, chronicles, capabilities, and checkpoints.

The World belongs to its creator. Ω Runtime is replaceable. Artifacts endure.

## 2. The three layers: M / AI / SELF

### M — the human layer
Intent, identity, values, experience, goals, preferences, and long-term direction. The human remains the source of purpose and authority.

### AI — the computational layer
Reasoning, planning, knowledge processing, execution, automation, and tool orchestration. Different providers and local models may contribute different capabilities.

### SELF — the emergent layer
The persistent cognitive environment formed through ongoing human–AI collaboration: continuity, context, shared working models, and adaptive workflows. SELF is not a claim that software is conscious; it names the designed continuity layer.

## 3. World-centric architecture

The project is World-centric rather than conversation-centric.

A World contains:
- World identity and ownership metadata.
- Goals, values, and active intent.
- Artifacts and their semantic relationships.
- Event history and checkpoints.
- Chapters and Chronicles.
- Knowledge and memory structures.
- Runtime and capability declarations.
- Plugins, agents, and Spellbooks.
- Optional connections to other Worlds.

A compatible runtime reads the World package, inspects its capabilities, identifies unsupported features, and reconstructs the richest faithful state it can. It must report limitations rather than silently inventing missing functionality.

## 4. Artifact model

An Artifact is the durable unit of meaningful work: code, specifications, decisions, research, images, diagrams, conversations, workflows, media, or other structured knowledge.

Artifacts should have stable identifiers, type, title, authorship, timestamps, version, semantic summary, tags, relationships, content references, and validation metadata. Changes create new versions or events rather than erasing lineage.

## 5. Chapters and Chronicles

Artifacts are grouped into Chapters representing meaningful milestones, not arbitrary calendar intervals.

Chronicles narrate how a World evolves. They can be rendered as technical histories, timelines, manga-style narratives, release notes, interactive stories, or presentations. A Chronicle is derived from recorded events and linked artifacts; it must not replace the underlying evidence.

## 6. Checkpoints, snapshots, and DNA Capsules

A Checkpoint identifies a validated continuity point: the World version, event position, active chapter, key artifacts, runtime compatibility, and next objective.

A Snapshot captures a selected World state. A DNA Capsule packages the information and references required to restore or migrate that state. Capsules may be exported from one device and restored on another, subject to permissions, available data, dependencies, and runtime capabilities.

A QR code or recovery key may identify or authorize access to a capsule, but should not expose private World contents or act as an unprotected secret.

## 7. Ω Runtime

Ω Runtime is the execution kernel. Its intended responsibilities include:
- Loading and validating World manifests.
- Restoring checkpoints and replaying events.
- Resolving artifacts and semantic relationships.
- Building context for human and agent tasks.
- Planning and executing bounded workflows.
- Managing capabilities, plugins, and agents.
- Generating Chronicles.
- Dispatching renderers.
- Exporting and importing Capsules.
- Preserving lineage and rollback capability.

The current repository contains an initial executable nucleus with World and Artifact creation, event emission, checkpoint operations, append-only event persistence, and reconstruction through event replay. The broader services remain staged work.

## 8. Embryo: local perception

Embryo is a proposed local perception organ for devices such as computers and phones. With explicit permissions, it may transform selected signals—voice-derived notes, application context, calendar events, location zones, or optional wearable summaries—into semantic cognitive events.

The design goal is not continuous surveillance. Raw audio, location traces, biometric streams, and other sensitive signals should remain local by default. Collection must be visible, configurable, revocable, and minimized. Derived observations should include provenance and confidence and remain editable by the user.

## 9. Forest Protocol and Living Atlas

The Forest is a network of sovereign Worlds. Connections are voluntary and permissioned. Worlds may exchange selected artifacts, public Chronicles, plugins, Spellbooks, knowledge packages, and collaboration invitations without surrendering ownership of private state.

The Living Atlas is a proposed discovery and presence interface. A World may publish a minimal public heartbeat—such as availability or a declared activity—without exposing private memory, precise location, or internal events. The Tavern is a proposed shared social space for visits, collaboration, and community activities.

## 10. Spellbooks

A Spellbook is a portable, declarative collection of workflows. A Spell can restore a context, prepare a workspace, execute a validated sequence, or request a state transition.

Examples:
- Continue Yesterday.
- Deep Focus.
- Research Mode.
- Publish Chapter.
- Build Runtime.
- Export Capsule.

Spells must declare required capabilities, inputs, permissions, expected effects, validation steps, and failure behavior. Descriptive names do not grant permission to perform external actions.

## 11. Renderer pipeline

Canonical Artifacts may be rendered into README files, documentation, websites, PDFs, presentations, graphics, videos, social posts, and interactive interfaces. Renderers are derived views, not canonical sources. Generated outputs should record their source artifact IDs and versions.

## 12. Multi-agent collaboration

Agents with different models and tools may specialize in architecture, research, engineering, review, design, writing, publishing, or observation. They collaborate through shared, inspectable artifacts and events, not opaque claims of shared memory.

Every agent must declare capabilities, permissions, provenance, and execution outcomes. Unsupported operations are reported explicitly.

## 13. Governance and invariants

- No mutation without validation.
- No evolution without a recoverable checkpoint.
- Rollback must remain possible.
- Protect identity, lineage, event history, and ownership.
- Share only what the World owner authorizes.
- Do not confuse conceptual designs with implemented systems.
- Prefer survivability and continuity over unconstrained autonomy.

## 14. Implementation maturity

This overview describes both an implemented foundation and a larger target architecture. The repository is authoritative for what currently runs. A concept becomes implemented only when source code, tests, and operational evidence support that status.

## 15. Guiding statement

> The World belongs to the user.  
> The Runtime is replaceable.  
> The Artifacts endure.
