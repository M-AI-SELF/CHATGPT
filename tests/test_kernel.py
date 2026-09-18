from runtime.omega import OmegaKernel


def test_world_lifecycle() -> None:
    kernel = OmegaKernel()
    artifact = kernel.create_artifact("A-0001", "Test", "hello")

    assert artifact["id"] == "A-0001"
    assert len(kernel.state.events) == 1

    checkpoint = kernel.checkpoint()
    kernel.restore(checkpoint)

    assert checkpoint["world_id"] == "omega-world"
    assert "A-0001" in checkpoint["artifact_ids"]
