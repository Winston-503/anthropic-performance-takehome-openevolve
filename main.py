#!/usr/bin/env python3
"""Main entry point."""

import asyncio

from dotenv import load_dotenv

from src.evolve import main

load_dotenv()

if __name__ == "__main__":
    asyncio.run(main())
