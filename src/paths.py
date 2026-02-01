import os
from typing import Final

SRC_DIR: Final[str] = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT: Final[str] = os.path.dirname(SRC_DIR)
TAKEHOME_DIR: Final[str] = os.path.join(PROJECT_ROOT, "original_performance_takehome-main-5452f74")

INITIAL_PROGRAM_PATH: Final[str] = os.path.join(TAKEHOME_DIR, "perf_takehome.py")
EVALUATOR_PATH: Final[str] = os.path.join(SRC_DIR, "evaluator.py")
CONFIG_DIR: Final[str] = os.path.join(PROJECT_ROOT, "config")
RESULTS_DIR: Final[str] = os.path.join(PROJECT_ROOT, "results")
