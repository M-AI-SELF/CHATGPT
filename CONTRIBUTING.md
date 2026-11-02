# Contributing

Thank you for helping evolve M-AI-SELF :: Ω Runtime.

## Before contributing

1. Read [README.md](README.md) and [docs/PROJECT_OVERVIEW.md](docs/PROJECT_OVERVIEW.md).
2. Inspect the relevant specification and current implementation.
3. Check existing issues and avoid duplicating work.
4. Keep changes aligned with World sovereignty, artifact lineage, and runtime independence.

## Engineering rules

- Do not describe planned functionality as implemented.
- Prefer small, reviewable changes.
- Preserve backward compatibility or document migrations.
- Validate inputs and state transitions.
- Add or update tests for behavior changes.
- Preserve append-only event history and checkpoint recoverability.
- Never commit credentials, private user data, raw recordings, or unredacted secrets.

## Artifacts and commits

Meaningful work should reference its Artifact and Chapter where applicable. Use concise commit messages, for example:

`docs(artifact-0000): establish canonical project overview`

## Pull requests

A pull request should explain:
- What changed and why.
- Which specification or Artifact it affects.
- Validation performed and results.
- Compatibility or migration impact.
- Known limitations and follow-up work.

## Security

Do not publish vulnerabilities or secrets in public issues. Follow the repository's security reporting guidance when one is established.
