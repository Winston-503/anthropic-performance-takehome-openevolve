import os

from openevolve import OpenEvolve
from openevolve.database import Program
from src.paths import CONFIG_DIR, EVALUATOR_PATH, INITIAL_PROGRAM_PATH
from src.utils import create_output_dir, load_config


async def main(config_filename: str, checkpoint: str | None = None) -> Program | None:
    config_path = os.path.join(CONFIG_DIR, config_filename)
    config = load_config(config_filename)

    if checkpoint:
        # When resuming, use the parent of the checkpoints dir as output_dir
        output_path = os.path.dirname(os.path.dirname(os.path.abspath(checkpoint)))
    else:
        output_path = create_output_dir(config_filename)

    openevolve_controller = OpenEvolve(
        initial_program_path=INITIAL_PROGRAM_PATH,
        evaluation_file=EVALUATOR_PATH,
        config=config,
        output_dir=output_path,
    )

    if checkpoint:
        print(f"Resuming from checkpoint: {checkpoint}")
    print("Starting OpenEvolve optimization...")
    print(f"Initial program: {INITIAL_PROGRAM_PATH}")
    print(f"Evaluator: {EVALUATOR_PATH}")
    print(f"Config: {config_path}")
    print(f"Output directory: {output_path}")
    print()

    best = await openevolve_controller.run(
        iterations=config.max_iterations,
        checkpoint_path=checkpoint,
    )

    print()
    print("=" * 60)
    print("Evolution complete!")
    print("=" * 60)
    print(f"Results saved to: {output_path}")
    if best is not None:
        print(f"Best metrics: {best.metrics}")

    return best
