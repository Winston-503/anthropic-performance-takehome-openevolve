import asyncio

from dotenv import load_dotenv

from src import main

load_dotenv()

if __name__ == "__main__":
    config_filename = "config-lightweight.yaml"
    asyncio.run(main(config_filename))
