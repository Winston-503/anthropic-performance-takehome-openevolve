import os
from datetime import datetime

from openevolve import Config
from src.paths import CONFIG_DIR, RESULTS_DIR, TAKEHOME_DIR

PROBLEM_PY_PATH = os.path.join(TAKEHOME_DIR, "problem.py")


def create_output_dir(config_filename: str) -> str:
    """Create and return an output directory path based on config filename and current timestamp."""

    config_name = os.path.splitext(os.path.basename(config_filename))[0]
    timestamp = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
    output_dir = os.path.join(RESULTS_DIR, f"openevolve_output-{config_name}-{timestamp}")
    os.makedirs(output_dir, exist_ok=True)
    return output_dir


def load_config(filename: str) -> Config:
    """Load config from YAML file and substitute {problem_py} with problem.py content.

    Args:
        filename: Name of the config file (relative to CONFIG_DIR)

    Returns:
        Config object with problem.py content substituted into system_message

    Raises:
        ValueError: If {problem_py} placeholder is not found in prompt.system_message
    """
    config_path = os.path.join(CONFIG_DIR, filename)
    config = Config.from_yaml(config_path)

    with open(PROBLEM_PY_PATH) as f:
        problem_py_content = f.read()

    original_message = config.prompt.system_message
    try:
        config.prompt.system_message = original_message.format(problem_py=problem_py_content)
    except KeyError as e:
        raise ValueError(
            f"Unknown placeholder {e} in prompt.system_message. Only {{{{problem_py}}}} is supported."
        ) from e

    if config.prompt.system_message == original_message:
        raise ValueError(
            "Placeholder {problem_py} not found in prompt.system_message. "
            "The system prompt must include {problem_py} to inject the problem definition."
        )

    return config
