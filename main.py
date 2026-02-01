#!/usr/bin/env python3
"""Main entry point."""

import asyncio
import sys

from dotenv import load_dotenv

from src.evolve import main

load_dotenv()

if __name__ == "__main__":
    config_path = sys.argv[1] if len(sys.argv) > 1 else None
    asyncio.run(main(config_path))
