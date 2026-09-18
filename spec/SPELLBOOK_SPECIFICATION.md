# Spellbook Specification v0.1

Spellbooks are declarative semantic workflows.

~~~yaml
spell:
  id: publish-chapter
  intent:
    publish: current_chapter
  requires:
    - artifact
    - checkpoint
  steps:
    - validate
    - generate_chronicle
    - render
    - create_capsule
    - publish
    - checkpoint
~~~

A Runtime interprets a Spell according to its registered capabilities.
