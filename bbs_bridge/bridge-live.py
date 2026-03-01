"""
Live bridge: listens on port 4023, connects to Evennia live on port 4000.
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from bridge import main

if __name__ == "__main__":
    asyncio.run(main(listen_port=4023, evennia_port=4000))
