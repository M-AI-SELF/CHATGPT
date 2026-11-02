# Ω-0010 :: RUNTIME CAPABILITY REGISTRY

## Outcome

The Runtime now has a provider-independent capability descriptor and deterministic in-memory registry. A World can express a capability requirement without binding itself to a vendor or adapter.

## Lifecycle

```text
Runtime boot
    │
    ▼
Provider discovery
    │
    ▼
Register descriptors
    │
    ▼
World / task declares requirement
    │
    ▼
Filter enabled + provider + permissions + trust
    │
    ▼
Deterministic provider resolution
    │
    ▼
Adapter boundary (execution is a later milestone)
```

## Implemented

- Validated descriptor and requirement dataclasses.
- Provider-scoped registration and explicit replacement.
- Discovery and inspection, including disabled entries.
- Permission and minimum-trust matching.
- Deterministic resolution and provider tie-breaking.
- Unregister operation.
- Adapter protocol declaration without unsafe implicit execution.

## Boundary

Registry contents are ephemeral Runtime state. They are not added to World fingerprints or DNA Capsules. The dashboard can display registry descriptors once a live Runtime exposes them through its overview endpoint.

## Next

Ω-0011 should connect resolved capabilities to a permission-checked execution boundary and observable execution outcomes.
