"""Evaluator for OpenEvolve optimization of the Anthropic Performance Takehome.

Uses the same test logic as tests/submission_tests.py:
- frozen_problem for reference kernel
- Same parameters (forest_height=10, rounds=16, batch_size=256) for performance stages
- BASELINE=147734 cycles for the full problem
"""

from __future__ import annotations

import importlib.util
import random
import sys
import traceback
from types import ModuleType
from typing import Any

from src.paths import INITIAL_PROGRAM_PATH, TAKEHOME_DIR

BASELINE = 147734


def _load_module_from_path(module_name: str, file_path: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load module from {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def _get_frozen_problem_module() -> ModuleType:
    frozen_problem_path = f"{TAKEHOME_DIR}/tests/frozen_problem.py"

    if TAKEHOME_DIR not in sys.path:
        sys.path.insert(0, TAKEHOME_DIR)

    return _load_module_from_path("frozen_problem", frozen_problem_path)


def _run_kernel_test(
    KernelBuilder,
    frozen_problem,
    forest_height: int,
    rounds: int,
    batch_size: int,
) -> tuple[int, bool]:
    """Run a single kernel test — same logic as submission_tests.do_kernel_test.

    Returns (cycles, correct).
    """
    forest = frozen_problem.Tree.generate(forest_height)
    inp = frozen_problem.Input.generate(forest, batch_size, rounds)
    mem = frozen_problem.build_mem_image(forest, inp)

    kb = KernelBuilder()
    kb.build_kernel(forest.height, len(forest.values), len(inp.indices), rounds)

    machine = frozen_problem.Machine(mem, kb.instrs, kb.debug_info(), n_cores=frozen_problem.N_CORES)
    machine.enable_pause = False
    machine.enable_debug = False
    machine.run()

    ref_mem = None
    for ref_mem in frozen_problem.reference_kernel2(mem):  # noqa: B007
        pass

    if ref_mem is None:
        return (0, False)

    inp_values_p = ref_mem[6]
    actual = machine.mem[inp_values_p : inp_values_p + len(inp.values)]
    expected = ref_mem[inp_values_p : inp_values_p + len(inp.values)]

    return (machine.cycle, actual == expected)


def _error_result() -> dict[str, Any]:
    return {
        "combined_score": 0.0,
        "cycles": BASELINE * 2,
        "speedup": 0.5,
        "correctness": 0,
    }


def evaluate_stage1(program_path: str) -> dict[str, Any]:
    """Quick correctness check with small problem size."""
    try:
        frozen_problem = _get_frozen_problem_module()
        evolved_module = _load_module_from_path("evolved_program", program_path)

        random.seed(42)
        _cycles, correct = _run_kernel_test(
            evolved_module.KernelBuilder,
            frozen_problem,
            forest_height=5,
            rounds=4,
            batch_size=64,
        )

        if not correct:
            return {"quick_score": 0.0, "correctness": 0, "combined_score": 0.0}

        return {"quick_score": 1.0, "correctness": 1, "combined_score": 1.0}

    except Exception as e:
        return {"quick_score": 0.0, "correctness": 0, "combined_score": 0.0, "error": str(e)}


def evaluate_stage2(program_path: str) -> dict[str, Any]:
    """Medium-fidelity evaluation — full problem size, 3 runs."""
    try:
        frozen_problem = _get_frozen_problem_module()
        evolved_module = _load_module_from_path("evolved_program", program_path)

        cycles_list = []
        for _ in range(3):
            cycles, correct = _run_kernel_test(
                evolved_module.KernelBuilder,
                frozen_problem,
                forest_height=10,
                rounds=16,
                batch_size=256,
            )
            if not correct:
                return {**_error_result(), "error": "Incorrect output values"}
            cycles_list.append(cycles)

        max_cycles = max(cycles_list)
        speedup = BASELINE / max_cycles

        return {
            "combined_score": speedup * 10,
            "cycles": max_cycles,
            "speedup": speedup,
            "correctness": 1,
        }

    except Exception as e:
        return {**_error_result(), "error": str(e), "traceback": traceback.format_exc()}


def evaluate_stage3(program_path: str) -> dict[str, Any]:
    """Full-fidelity evaluation matching submission_tests exactly.

    Same parameters as tests/submission_tests.py:
    forest_height=10, rounds=16, batch_size=256, 8 runs, max cycles.
    """
    try:
        frozen_problem = _get_frozen_problem_module()
        evolved_module = _load_module_from_path("evolved_program", program_path)

        cycles_list = []
        for _ in range(8):
            cycles, correct = _run_kernel_test(
                evolved_module.KernelBuilder,
                frozen_problem,
                forest_height=10,
                rounds=16,
                batch_size=256,
            )
            if not correct:
                return {**_error_result(), "error": "Incorrect output values"}
            cycles_list.append(cycles)

        max_cycles = max(cycles_list)
        speedup = BASELINE / max_cycles

        return {
            "combined_score": speedup * 10,
            "cycles": max_cycles,
            "speedup": speedup,
            "correctness": 1,
        }

    except Exception as e:
        return {**_error_result(), "error": str(e), "traceback": traceback.format_exc()}


# Alias for direct use (e.g. __main__, non-cascade mode)
evaluate = evaluate_stage3


if __name__ == "__main__":
    result = evaluate(INITIAL_PROGRAM_PATH)
    print(f"Evaluation result: {result}")
