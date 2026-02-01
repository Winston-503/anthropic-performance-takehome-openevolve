import os
from datetime import datetime
from typing import Final

SRC_DIR: Final[str] = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT: Final[str] = os.path.dirname(SRC_DIR)
TAKEHOME_DIR: Final[str] = os.path.join(PROJECT_ROOT, "original_performance_takehome-main-5452f74")

INITIAL_PROGRAM_PATH: Final[str] = os.path.join(TAKEHOME_DIR, "perf_takehome.py")
EVALUATOR_PATH: Final[str] = os.path.join(SRC_DIR, "evaluator.py")
CONFIG_DIR: Final[str] = os.path.join(PROJECT_ROOT, "config")
RESULTS_DIR: Final[str] = os.path.join(PROJECT_ROOT, "results")


def create_output_dir(config_filename: str) -> str:
    """Create and return an output directory path based on config filename and current timestamp."""

    config_name = os.path.splitext(os.path.basename(config_filename))[0]
    timestamp = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
    output_dir = os.path.join(RESULTS_DIR, f"openevolve_output-{config_name}-{timestamp}")
    os.makedirs(output_dir, exist_ok=True)
    return output_dir
