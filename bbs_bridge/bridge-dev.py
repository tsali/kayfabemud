"""
Dev bridge: listens on port 4033, connects to Evennia dev on port 4010.
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from bridge import main

if __name__ == "__main__":
    asyncio.run(main(listen_port=4033, evennia_port=4010))
