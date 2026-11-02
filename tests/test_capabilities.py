import pytest

from runtime.omega.capabilities import (
    CapabilityDescriptor,
    CapabilityRegistry,
    CapabilityRequirement,
)


def test_register_and_discover_capabilities_deterministically():
    registry = CapabilityRegistry()
    registry.register(CapabilityDescriptor("memory.read", provider="zeta", trust_level="trusted"))
    registry.register(CapabilityDescriptor("memory.read", provider="alpha", trust_level="trusted"))
    assert [item.provider for item in registry.discover()] == ["alpha", "zeta"]


def test_duplicate_provider_registration_requires_explicit_replace():
    registry = CapabilityRegistry()
    registry.register(CapabilityDescriptor("vision.analyze", provider="local"))
    with pytest.raises(ValueError):
        registry.register(CapabilityDescriptor("vision.analyze", provider="local", version="2.0.0"))
    registry.register(CapabilityDescriptor("vision.analyze", provider="local", version="2.0.0"), replace=True)
    assert registry.get("vision.analyze").version == "2.0.0"


def test_resolve_matches_permissions_trust_and_provider():
    registry = CapabilityRegistry()
    registry.register(CapabilityDescriptor("filesystem.read", provider="remote", permissions=("fs.read",), trust_level="restricted"))
    registry.register(CapabilityDescriptor("filesystem.read", provider="local", permissions=("fs.read", "fs.list"), trust_level="trusted"))
    result = registry.resolve(CapabilityRequirement("filesystem.read", permissions=("fs.read",), minimum_trust="trusted"))
    assert result.provider == "local"


def test_resolve_rejects_missing_permission_or_trust():
    registry = CapabilityRegistry()
    registry.register(CapabilityDescriptor("automation.execute", permissions=("automation.run",), trust_level="restricted"))
    with pytest.raises(LookupError):
        registry.resolve(CapabilityRequirement("automation.execute", permissions=("filesystem.write",), minimum_trust="trusted"))


def test_disabled_capability_is_not_resolved_but_remains_inspectable():
    registry = CapabilityRegistry()
    registry.register(CapabilityDescriptor("speech.transcribe", enabled=False))
    assert registry.discover() == []
    assert registry.get("speech.transcribe", "local").enabled is False
    with pytest.raises(LookupError):
        registry.resolve(CapabilityRequirement("speech.transcribe"))


def test_unregister_is_idempotent_and_provider_scoped():
    registry = CapabilityRegistry()
    registry.register(CapabilityDescriptor("reasoning", provider="local"))
    assert registry.unregister("reasoning", "local") is True
    assert registry.unregister("reasoning", "local") is False
    assert len(registry) == 0


def test_descriptor_rejects_invalid_trust_and_permissions():
    with pytest.raises(ValueError):
        CapabilityDescriptor("unsafe", trust_level="root")
    with pytest.raises(ValueError):
        CapabilityDescriptor("unsafe", permissions=("",))
