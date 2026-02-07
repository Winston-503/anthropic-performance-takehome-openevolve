import asyncio

import click
from dotenv import load_dotenv

from src import main

load_dotenv()


@click.command()
@click.option(
    "--config",
    default="config-gemini.yaml",
    help="Path to the configuration file.",
)
@click.option(
    "--checkpoint",
    default=None,
    help="Path to a checkpoint directory to resume from.",
)
def cli(config: str, checkpoint: str | None) -> None:
    asyncio.run(main(config, checkpoint=checkpoint))


if __name__ == "__main__":
    cli()
