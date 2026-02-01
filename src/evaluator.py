"""Evaluator for OpenEvolve optimization of the Anthropic Performance Takehome."""

from __future__ import annotations

import importlib.util
import random
import sys
import traceback
from typing import Any

from .utils import INITIAL_PROGRAM_PATH, TAKEHOME_DIR

BASELINE = 147734


def _load_module_from_path(module_name: str, file_path: str) -> Any:
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load module from {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def _get_frozen_problem_module() -> Any:
    frozen_problem_path = f"{TAKEHOME_DIR}/tests/frozen_problem.py"

    if TAKEHOME_DIR not in sys.path:
        sys.path.insert(0, TAKEHOME_DIR)

    return _load_module_from_path("frozen_problem", frozen_problem_path)


def evaluate(program_path: str) -> dict[str, Any]:
    try:
        frozen_problem = _get_frozen_problem_module()
        Machine = frozen_problem.Machine
        build_mem_image = frozen_problem.build_mem_image
        reference_kernel2 = frozen_problem.reference_kernel2
        Tree = frozen_problem.Tree
        Input = frozen_problem.Input
        N_CORES = frozen_problem.N_CORES

        evolved_module = _load_module_from_path("evolved_program", program_path)
        KernelBuilder = evolved_module.KernelBuilder

        forest_height = 10
        rounds = 16
        batch_size = 256

        cycles_list = []
        for _ in range(8):
            forest = Tree.generate(forest_height)
            inp = Input.generate(forest, batch_size, rounds)
            mem = build_mem_image(forest, inp)

            kb = KernelBuilder()
            kb.build_kernel(forest.height, len(forest.values), len(inp.indices), rounds)

            machine = Machine(mem, kb.instrs, kb.debug_info(), n_cores=N_CORES)
            machine.enable_pause = False
            machine.enable_debug = False
            machine.run()

            ref_mem = None
            for ref_mem in reference_kernel2(mem):  # noqa: B007
                pass

            if ref_mem is None:
                return {
                    "combined_score": 0.0,
                    "cycles": BASELINE * 2,
                    "speedup": 0.5,
                    "correctness": 0,
                    "error": "Reference kernel returned no result",
                }

            inp_values_p = ref_mem[6]
            actual = machine.mem[inp_values_p : inp_values_p + len(inp.values)]
            expected = ref_mem[inp_values_p : inp_values_p + len(inp.values)]
            if actual != expected:
                return {
                    "combined_score": 0.0,
                    "cycles": BASELINE * 2,
                    "speedup": 0.5,
                    "correctness": 0,
                    "error": "Incorrect output values",
                }

            cycles_list.append(machine.cycle)

        cycles = max(cycles_list)
        speedup = BASELINE / cycles
        combined_score = (BASELINE / cycles) * 10

        return {
            "combined_score": combined_score,
            "cycles": cycles,
            "speedup": speedup,
            "correctness": 1,
        }

    except Exception as e:
        return {
            "combined_score": 0.0,
            "cycles": BASELINE * 2,
            "speedup": 0.5,
            "correctness": 0,
            "error": str(e),
            "traceback": traceback.format_exc(),
        }


def evaluate_stage1(program_path: str) -> dict[str, Any]:
    try:
        frozen_problem = _get_frozen_problem_module()
        Machine = frozen_problem.Machine
        build_mem_image = frozen_problem.build_mem_image
        reference_kernel2 = frozen_problem.reference_kernel2
        Tree = frozen_problem.Tree
        Input = frozen_problem.Input
        N_CORES = frozen_problem.N_CORES

        evolved_module = _load_module_from_path("evolved_program", program_path)
        KernelBuilder = evolved_module.KernelBuilder

        forest_height = 5
        rounds = 4
        batch_size = 64

        random.seed(42)
        forest = Tree.generate(forest_height)
        inp = Input.generate(forest, batch_size, rounds)
        mem = build_mem_image(forest, inp)

        kb = KernelBuilder()
        kb.build_kernel(forest.height, len(forest.values), len(inp.indices), rounds)

        machine = Machine(mem, kb.instrs, kb.debug_info(), n_cores=N_CORES)
        machine.enable_pause = False
        machine.enable_debug = False
        machine.run()

        ref_mem = None
        for ref_mem in reference_kernel2(mem):  # noqa: B007
            pass

        if ref_mem is None:
            return {"quick_score": 0.0, "correctness": 0}

        inp_values_p = ref_mem[6]
        actual = machine.mem[inp_values_p : inp_values_p + len(inp.values)]
        expected = ref_mem[inp_values_p : inp_values_p + len(inp.values)]
        if actual != expected:
            return {"quick_score": 0.0, "correctness": 0}

        return {"quick_score": 1.0, "correctness": 1}

    except Exception as e:
        return {"quick_score": 0.0, "correctness": 0, "error": str(e)}


if __name__ == "__main__":
    result = evaluate(INITIAL_PROGRAM_PATH)
    print(f"Evaluation result: {result}")
