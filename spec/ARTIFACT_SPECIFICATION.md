# Artifact Specification v0.1

Artifacts are immutable, versioned units of meaning.

~~~yaml
id:
type:
title:
author:
created:
updated:
version:
parents: []
children: []
tags: []
semantic_summary:
renderer:
content:
metadata: {}
~~~

A modification creates a new Artifact version. Historical Artifacts are never overwritten.

Supported relationships:

- references
- depends_on
- extends
- implements
- belongs_to
- derived_from
- generated_by
- duplicates
- contradicts
- supports
- explains
