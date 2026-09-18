# Checkpoint Protocol v0.1

A Checkpoint is a semantic restoration boundary.

~~~yaml
checkpoint:
  id: Ω-0001
  world: personal
  chapter: genesis
  artifact: Ω-SEED-0001

  runtime:
    version: 0.1.0-alpha
    capabilities: []

  state:
    status: active
    mode: build

  layers:
    M: {}
    AI: {}
    SELF: {}

  cognitive_diff:
    added: []
    changed: []
    removed: []

  next: []

  repository:
    commit: null
~~~

A valid checkpoint MUST be sufficient to locate the World state and its next executable context.
