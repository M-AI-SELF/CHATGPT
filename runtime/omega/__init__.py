"""M-AI-SELF Ω Runtime public interface."""

from .capabilities import CapabilityAdapter, CapabilityDescriptor, CapabilityRegistry, CapabilityRequirement
from .kernel import OmegaKernel, WorldState

__all__ = [
    "CapabilityAdapter",
    "CapabilityDescriptor",
    "CapabilityRegistry",
    "CapabilityRequirement",
    "OmegaKernel",
    "WorldState",
]
