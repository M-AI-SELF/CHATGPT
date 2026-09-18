# Event Specification v0.1

World state is event-sourced.

~~~text
State = Replay(Events)
~~~

Events are immutable records describing meaningful state transitions.

Initial event vocabulary:

- ArtifactCreated
- ArtifactUpdated
- ArtifactArchived
- DecisionAccepted
- DecisionRejected
- GoalCreated
- GoalCompleted
- PluginInstalled
- PluginRemoved
- SpellExecuted
- RendererExecuted
- CheckpointSaved
- ChapterPublished
- ChronicleGenerated
- WorldImported
- WorldExported
- CapsuleCreated
- CapsuleRestored
