"""
One-shot migration: patch existing NPCs with signature_moves from npc_data.
Run from inside Evennia: py import world.migrate_signature_moves
"""

from world.npc_data import NPC_WRESTLERS
from evennia.utils.search import search_tag
from evennia.utils import logger

def run():
    sig_map = {}
    for nd in NPC_WRESTLERS:
        if nd.get("signature_moves"):
            sig_map[nd["npc_id"]] = nd["signature_moves"]

    npcs = search_tag("named_npc", category="npc_type")
    patched = 0
    for npc in npcs:
        npc_id = npc.db.npc_id
        if npc_id in sig_map:
            npc.db.signature_moves = sig_map[npc_id]
            patched += 1

    msg = f"Patched {patched} NPCs with signature_moves (of {len(sig_map)} defined)."
    logger.log_info(f"MIGRATION: {msg}")
    return msg

# Auto-run on import
result = run()
print(result)
