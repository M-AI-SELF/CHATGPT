# World Event Store

The Ω Runtime bootstrap event store uses append-only JSON Lines records.

Events are immutable. World state is reconstructed by replaying events in stored order.

The event log is an implementation detail; the semantic Event Specification remains canonical.
