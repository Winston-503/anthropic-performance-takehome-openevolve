import os

from openevolve import Config, OpenEvolve
from openevolve.database import Program

from .utils import CONFIG_DIR, EVALUATOR_PATH, INITIAL_PROGRAM_PATH, OUTPUT_DIR


async def main(config_filename: str) -> Program | None:
    config_path = os.path.join(CONFIG_DIR, config_filename)
    config = Config.from_yaml(config_path)

    openevolve_controller = OpenEvolve(
        initial_program_path=INITIAL_PROGRAM_PATH,
        evaluation_file=EVALUATOR_PATH,
        config=config,
        output_dir=OUTPUT_DIR,
    )

    print("Starting OpenEvolve optimization...")
    print(f"Initial program: {INITIAL_PROGRAM_PATH}")
    print(f"Evaluator: {EVALUATOR_PATH}")
    print(f"Config: {config_path}")
    print(f"Output directory: {OUTPUT_DIR}")
    print()

    best = await openevolve_controller.run(iterations=config.max_iterations)

    print()
    print("=" * 60)
    print("Evolution complete!")
    print("=" * 60)
    print(f"Results saved to: {OUTPUT_DIR}")
    if best is not None:
        print(f"Best metrics: {best.metrics}")

    return best
