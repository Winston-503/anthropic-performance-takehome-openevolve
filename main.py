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
def cli(config: str) -> None:
    asyncio.run(main(config))


if __name__ == "__main__":
    cli()
