"""OpenEvolve optimization runner."""

import os
import sys

from openevolve import Config, OpenEvolve


async def main():
    src_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(src_dir)
    takehome_dir = os.path.join(project_root, "original_performance_takehome-main-5452f74")
    initial_program_path = os.path.join(takehome_dir, "perf_takehome.py")
    evaluator_path = os.path.join(src_dir, "evaluator.py")
    config_path = os.path.join(project_root, "config", "config.yaml")
    output_dir = os.path.join(project_root, "openevolve_output")

    if not os.environ.get("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY environment variable is not set.")
        print("Please set it in your .env file or environment.")
        sys.exit(1)

    config = Config.from_yaml(config_path)

    oe = OpenEvolve(
        initial_program_path=initial_program_path,
        evaluation_file=evaluator_path,
        config=config,
        output_dir=output_dir,
    )

    print("Starting OpenEvolve optimization...")
    print(f"Initial program: {initial_program_path}")
    print(f"Evaluator: {evaluator_path}")
    print(f"Config: {config_path}")
    print(f"Output directory: {output_dir}")
    print()

    best = await oe.run(iterations=config.max_iterations)

    print()
    print("=" * 60)
    print("Evolution complete!")
    print("=" * 60)
    print(f"Best score: {best.score if hasattr(best, 'score') else best}")
    print(f"Results saved to: {output_dir}")

    return best
