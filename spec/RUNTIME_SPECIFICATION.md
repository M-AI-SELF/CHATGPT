# M-AI-SELF :: Ω Runtime
## Runtime Specification v0.1

The Runtime interprets a World; it does not own the World.

### Required operations

- LoadWorld
- RestoreCheckpoint
- ExecuteSpell
- ExecuteGoal
- GenerateChronicle
- Render
- ExportCapsule
- ImportCapsule
- QueryArtifacts
- QueryKnowledge
- SaveCheckpoint

### Kernel services

- ContextBuilder
- IdentityResolver
- ArtifactIndex
- EventBus
- StateManager
- Planner
- Scheduler
- CapabilityRegistry
- PluginManager
- SpellbookEngine
- CheckpointManager
- ChronicleEngine
- RendererDispatcher

### Runtime contract

A compatible runtime MUST preserve semantic continuity and MUST NOT require a specific model provider.

> The World belongs to the user. The Runtime is replaceable.
