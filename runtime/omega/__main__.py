from .kernel import OmegaKernel


def main() -> None:
    kernel = OmegaKernel()
    kernel.create_artifact("Ω-SEED-0001", "The Seed", "M-AI-SELF :: Ω Runtime")
    print(kernel.checkpoint())


if __name__ == "__main__":
    main()
