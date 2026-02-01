import os

from openevolve import Config, OpenEvolve
from openevolve.database import Program

from .paths import CONFIG_DIR, EVALUATOR_PATH, INITIAL_PROGRAM_PATH, create_output_dir


async def main(config_filename: str) -> Program | None:
    config_path = os.path.join(CONFIG_DIR, config_filename)
    config = Config.from_yaml(config_path)

    output_path = create_output_dir(config_filename)

    openevolve_controller = OpenEvolve(
        initial_program_path=INITIAL_PROGRAM_PATH,
        evaluation_file=EVALUATOR_PATH,
        config=config,
        output_dir=output_path,
    )

    print("Starting OpenEvolve optimization...")
    print(f"Initial program: {INITIAL_PROGRAM_PATH}")
    print(f"Evaluator: {EVALUATOR_PATH}")
    print(f"Config: {config_path}")
    print(f"Output directory: {output_path}")
    print()

    best = await openevolve_controller.run(iterations=config.max_iterations)

    print()
    print("=" * 60)
    print("Evolution complete!")
    print("=" * 60)
    print(f"Results saved to: {output_path}")
    if best is not None:
        print(f"Best metrics: {best.metrics}")

    return best
