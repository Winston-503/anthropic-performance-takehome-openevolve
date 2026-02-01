"""OpenEvolve optimization runner."""

import os
import sys

from openevolve import Config, OpenEvolve
from src.utils import DEFAULT_CONFIG_PATH, EVALUATOR_PATH, INITIAL_PROGRAM_PATH, OUTPUT_DIR


async def main(config_path: str | None = None):
    if config_path is None:
        config_path = DEFAULT_CONFIG_PATH

    if not os.environ.get("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY environment variable is not set.")
        print("Please set it in your .env file or environment.")
        sys.exit(1)

    config = Config.from_yaml(config_path)

    oe = OpenEvolve(
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

    best = await oe.run(iterations=config.max_iterations)

    print()
    print("=" * 60)
    print("Evolution complete!")
    print("=" * 60)
    print(f"Best score: {best.score if hasattr(best, 'score') else best}")
    print(f"Results saved to: {OUTPUT_DIR}")

    return best
