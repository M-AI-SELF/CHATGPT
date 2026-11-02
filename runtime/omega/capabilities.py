"""Provider-independent runtime capability declarations and resolution.

The registry describes what this Runtime can provide. It does not execute adapters
or make capability availability part of the portable World state.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol


TRUST_LEVELS = {"untrusted": 0, "restricted": 1, "trusted": 2}


class CapabilityAdapter(Protocol):
    """Minimal adapter contract; implementations are supplied by Runtime providers."""

    def execute(self, input_data: dict[str, Any]) -> dict[str, Any]: ...


@dataclass(frozen=True)
class CapabilityDescriptor:
    capability_id: str
    version: str = "1.0.0"
    description: str = ""
    provider: str = "local"
    permissions: tuple[str, ...] = ()
    trust_level: str = "restricted"
    enabled: bool = True
    input_schema: dict[str, Any] | None = None
    output_schema: dict[str, Any] | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.capability_id.strip():
            raise ValueError("Capability ID is required.")
        if not self.version.strip():
            raise ValueError("Capability version is required.")
        if not self.provider.strip():
            raise ValueError("Capability provider is required.")
        if self.trust_level not in TRUST_LEVELS:
            raise ValueError(f"Unsupported trust level: {self.trust_level}")
        if any(not permission.strip() for permission in self.permissions):
            raise ValueError("Capability permissions must be non-empty strings.")

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.capability_id,
            "version": self.version,
            "description": self.description,
            "provider": self.provider,
            "permissions": list(self.permissions),
            "trust_level": self.trust_level,
            "enabled": self.enabled,
            "input_schema": self.input_schema,
            "output_schema": self.output_schema,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True)
class CapabilityRequirement:
    capability_id: str
    permissions: tuple[str, ...] = ()
    minimum_trust: str = "untrusted"
    provider: str | None = None

    def __post_init__(self) -> None:
        if not self.capability_id.strip():
            raise ValueError("Required capability ID is required.")
        if self.minimum_trust not in TRUST_LEVELS:
            raise ValueError(f"Unsupported minimum trust level: {self.minimum_trust}")


class CapabilityRegistry:
    """In-memory registry for Runtime-provided capabilities.

    Registry contents are intentionally Runtime-scoped and disposable. A World
    may declare requirements, but it must not serialize provider availability.
    """

    def __init__(self) -> None:
        self._entries: dict[tuple[str, str], CapabilityDescriptor] = {}

    def register(self, descriptor: CapabilityDescriptor, *, replace: bool = False) -> CapabilityDescriptor:
        key = (descriptor.capability_id, descriptor.provider)
        if key in self._entries and not replace:
            raise ValueError(f"Capability already registered: {descriptor.capability_id} from {descriptor.provider}")
        self._entries[key] = descriptor
        return descriptor

    def unregister(self, capability_id: str, provider: str) -> bool:
        return self._entries.pop((capability_id, provider), None) is not None

    def get(self, capability_id: str, provider: str | None = None) -> CapabilityDescriptor:
        matches = self.discover(capability_id=capability_id, provider=provider, include_disabled=True)
        if not matches:
            raise KeyError(f"Unknown capability: {capability_id}")
        return matches[0]

    def discover(
        self,
        *,
        capability_id: str | None = None,
        provider: str | None = None,
        include_disabled: bool = False,
    ) -> list[CapabilityDescriptor]:
        matches = [
            item for item in self._entries.values()
            if (capability_id is None or item.capability_id == capability_id)
            and (provider is None or item.provider == provider)
            and (include_disabled or item.enabled)
        ]
        return sorted(matches, key=lambda item: (item.capability_id, item.provider, item.version))

    def resolve(self, requirement: CapabilityRequirement) -> CapabilityDescriptor:
        required_permissions = set(requirement.permissions)
        minimum_trust = TRUST_LEVELS[requirement.minimum_trust]
        candidates = [
            item for item in self.discover(capability_id=requirement.capability_id)
            if (requirement.provider is None or item.provider == requirement.provider)
            and required_permissions.issubset(set(item.permissions))
            and TRUST_LEVELS[item.trust_level] >= minimum_trust
        ]
        if not candidates:
            raise LookupError(f"No capability provider satisfies requirement: {requirement.capability_id}")
        # Prefer the most trusted eligible provider; tie-break deterministically.
        candidates.sort(key=lambda item: (-TRUST_LEVELS[item.trust_level], item.provider, item.version))
        return candidates[0]

    def describe(self) -> list[dict[str, Any]]:
        return [item.to_dict() for item in self.discover(include_disabled=True)]

    def __len__(self) -> int:
        return len(self._entries)
