# Ω-0010 :: Runtime Capability Registry Specification

## Principle

**The World declares what it needs. The Runtime declares what it can do.**

A capability is a provider-independent declaration of a runtime function. The registry resolves an eligible provider without making the World dependent on that provider.

## Descriptor

A descriptor contains:
- `capability_id` and `version`
- human-readable description
- provider identifier
- declared permissions
- trust level: `untrusted`, `restricted`, or `trusted`
- enabled state
- optional input/output schema and metadata

## Requirement

A requirement identifies a capability and may constrain:
- required permission set
- minimum trust level
- exact provider

## Resolution

1. Ignore disabled providers.
2. Match capability ID and optional provider.
3. Require all requested permissions.
4. Require the minimum trust level.
5. Prefer the highest eligible trust level.
6. Break ties deterministically by provider and version.

No eligible provider produces a `LookupError`. Registration collisions for the same capability/provider pair are rejected unless replacement is explicit.

## Ownership and persistence

The registry belongs to the Runtime and is intentionally in-memory in this milestone. Provider availability is not canonical World state and is not included in DNA Capsules. Worlds may declare capability requirements; a Runtime discovers its own available providers at boot.

## Adapter boundary

`CapabilityAdapter` defines a minimal `execute(input_data)` protocol. This milestone does not invoke arbitrary adapter code, grant permissions, or claim provider execution. Execution, policy enforcement and auditable capability events are later work.

## Security invariants

- Capability declarations do not grant permissions.
- Resolution is not authorization to execute.
- Disabled providers cannot be resolved.
- Trust metadata is a declared property, not cryptographic attestation.
- No capability may mutate the World outside validated Runtime workflows.
