"""
Kayfabe: Protect the Business — Master world builder script.

Run from Evennia shell:
    py from world.build_world import build_world; build_world()

Or import and call build_world() from any Evennia context.
"""

from evennia.utils.create import create_object, create_script
from evennia.utils.search import search_tag
from evennia.utils import logger


def build_world():
    """Build the entire game world from territory data."""
    from world.territories import TERRITORIES
    from world.backyard_npcs import generate_fed_roster

    logger.log_info("KAYFABE: Starting world build...")

    # Track created rooms by key for exit linking
    rooms = {}

    # Build the chargen limbo room
    chargen_room = _create_room(
        "chargen_limbo",
        "Character Creation",
        "typeclasses.rooms.ChargenRoom",
        tags=[("chargen_limbo", "chargen")],
    )
    rooms["chargen_limbo"] = chargen_room
    logger.log_info(f"  Created chargen limbo room: {chargen_room}")

    # Build each territory
    for terr_key, terr_data in TERRITORIES.items():
        logger.log_info(f"  Building territory: {terr_data['name']} ({terr_key})")

        # Create rooms
        for room_def in terr_data["rooms"]:
            tags = room_def.get("tags", [])
            # Add territory tag if not already present
            if not any(t[1] == "territory" for t in tags if isinstance(t, tuple)):
                tags.append((terr_key, "territory"))

            room = _create_room(
                room_def["key"],
                room_def["name"],
                room_def["typeclass"],
                desc=room_def.get("desc", ""),
                tags=tags,
            )

            # Set territory metadata
            room.db.territory_key = terr_key
            room.db.territory_name = terr_data["name"]
            room.db.tier = terr_data["tier"]

            # Apply extras
            extras = room_def.get("extras", {})
            for attr, val in extras.items():
                room.attributes.add(attr, val)

            rooms[room_def["key"]] = room

        # Create exits
        for exit_def in terr_data.get("exits", []):
            exit_name, from_key, to_key = exit_def
            from_room = rooms.get(from_key)
            to_room = rooms.get(to_key)
            if from_room and to_room:
                _create_exit(exit_name, from_room, to_room)
            else:
                logger.log_warn(
                    f"  Could not create exit '{exit_name}': "
                    f"from={from_key} ({from_room}), to={to_key} ({to_room})"
                )

        # Spawn backyard NPCs for tier 1 feds
        if terr_data["tier"] == 1:
            venue_key = None
            for room_def in terr_data["rooms"]:
                if "venue" in room_def["key"] or "arena" in room_def["key"].lower():
                    venue_key = room_def["key"]
                    break
            if venue_key and venue_key in rooms:
                _spawn_backyard_npcs(terr_key, rooms[venue_key])

    # Spawn all named NPCs and managers from npc_data.py
    _spawn_all_named_npcs(rooms)
    _spawn_all_managers(rooms)

    # Create global scripts
    _create_scheduler_script()
    _create_economy_script()

    # Create help entries
    from world.help_entries import create_help_entries
    create_help_entries()

    # Update the Limbo room (Evennia's default #2) with wrestling backstory
    _update_limbo_room()

    logger.log_info("KAYFABE: World build complete!")
    return rooms


def _create_room(key, name, typeclass, desc="", tags=None):
    """Create a room, deleting any existing room with the same tag."""
    # Clean up existing rooms with same key tag
    existing = search_tag(key, category="room_key")
    for obj in existing:
        logger.log_info(f"    Deleting existing room: {obj}")
        obj.delete()

    room = create_object(
        typeclass,
        key=name,
        tags=[(key, "room_key")] + (tags or []),
    )
    if desc:
        room.db.desc = desc
    return room


def _create_exit(name, from_room, to_room):
    """Create an exit between rooms. Skip if duplicate."""
    # Check for existing exit with same name from this room
    for ex in from_room.exits:
        if ex.key == name:
            return ex
    return create_object(
        "typeclasses.exits.Exit",
        key=name,
        location=from_room,
        destination=to_room,
    )


def _spawn_backyard_npcs(fed_key, venue_room, count=6):
    """Spawn random backyard NPCs in a venue."""
    from world.backyard_npcs import generate_fed_roster

    logger.log_info(f"    Spawning {count} backyard NPCs for {fed_key}")
    roster = generate_fed_roster(fed_key, count=count)

    for npc_data in roster:
        npc = create_object(
            "typeclasses.npcs.BackyardNPC",
            key=npc_data["ring_name"],
            location=venue_room,
            tags=[(fed_key, "territory"), ("backyard_npc", "npc_type")],
        )
        npc.db.alignment = npc_data["alignment"]
        npc.db.finisher_name = npc_data["finisher_name"]
        npc.db.finisher_type = npc_data["finisher_type"]
        npc.db.level = npc_data["level"]
        npc.db.home_territory = fed_key
        stats = npc_data["stats"]
        npc.setup_stats(
            stats["str"], stats["agi"], stats["tec"],
            stats["cha"], stats["tou"], stats["psy"],
        )


# ============================================================
# TERRITORY → ROOM KEY MAPPING
# ============================================================
# Maps territory keys to room keys where NPCs should be placed.
# Each entry is: {role: room_key}
# If a territory isn't in this map, NPCs for it are skipped
# (they'll be added when those territories are built in Phase 4).

TERRITORY_ROOM_MAP = {
    # Tier 2 — Training Schools
    "pensacola": {
        "trainer": "pens_floor",
        "wrestler": "pens_ring",
        "announcer": "pens_civic",
        "authority": "pens_afa_house",
        "default": "pens_ring",
    },
    "slaughterhouse": {
        "trainer": "slaught_floor",
        "wrestler": "slaught_ring",
        "default": "slaught_ring",
    },
    "beast_works": {
        "trainer": "beast_floor",
        "wrestler": "beast_ring",
        "default": "beast_ring",
    },
    "conservatory": {
        "trainer": "cons_floor",
        "wrestler": "cons_ring",
        "default": "cons_ring",
    },
    "dungeon_holds": {
        "trainer": "dung_floor",
        "wrestler": "dung_ring",
        "default": "dung_ring",
    },
    "proving_grounds": {
        "trainer": "prov_floor",
        "wrestler": "prov_ring",
        "default": "prov_ring",
    },
    # Tier 3 — Regional Territories
    "memphis": {
        "trainer": "mem_gym",
        "wrestler": "mem_arena",
        "announcer": "mem_arena",
        "authority": "mem_office",
        "default": "mem_arena",
    },
    "midsouth": {
        "trainer": "ms_gym",
        "wrestler": "ms_arena",
        "announcer": "ms_arena",
        "authority": "ms_office",
        "default": "ms_arena",
    },
    "midatlantic": {
        "trainer": "ma_gym",
        "wrestler": "ma_arena",
        "announcer": "ma_arena",
        "authority": "ma_office",
        "default": "ma_arena",
    },
    "florida": {
        "trainer": "fl_gym",
        "wrestler": "fl_arena",
        "announcer": "fl_arena",
        "authority": "fl_office",
        "default": "fl_arena",
    },
    "georgia": {
        "trainer": "ga_gym",
        "wrestler": "ga_arena",
        "announcer": "ga_arena",
        "authority": "ga_office",
        "default": "ga_arena",
    },
    "wccw": {
        "trainer": "wc_gym",
        "wrestler": "wc_arena",
        "announcer": "wc_arena",
        "authority": "wc_office",
        "default": "wc_arena",
    },
    "awa": {
        "trainer": "awa_gym",
        "wrestler": "awa_arena",
        "announcer": "awa_arena",
        "authority": "awa_office",
        "default": "awa_arena",
    },
    "stampede": {
        "trainer": "stm_gym",
        "wrestler": "stm_arena",
        "announcer": "stm_arena",
        "authority": "stm_office",
        "default": "stm_arena",
    },
    "pnw": {
        "trainer": "pnw_gym",
        "wrestler": "pnw_arena",
        "announcer": "pnw_arena",
        "authority": "pnw_office",
        "default": "pnw_arena",
    },
    # Tier 3.5 — Developmental
    "ovw": {
        "trainer": "ovw_gym",
        "wrestler": "ovw_arena",
        "announcer": "ovw_arena",
        "authority": "ovw_corwin",
        "default": "ovw_arena",
    },
    "fcw": {
        "trainer": "fcw_gym",
        "wrestler": "fcw_arena",
        "announcer": "fcw_arena",
        "default": "fcw_arena",
    },
    "dsw": {
        "trainer": "dsw_gym",
        "wrestler": "dsw_arena",
        "announcer": "dsw_arena",
        "authority": "dsw_office",
        "default": "dsw_arena",
    },
    "hwa": {
        "trainer": "hwa_gym",
        "wrestler": "hwa_arena",
        "announcer": "hwa_arena",
        "default": "hwa_arena",
    },
    # Tier 4 — National / International
    "wwf": {
        "trainer": "wwf_gym",
        "wrestler": "wwf_arena",
        "announcer": "wwf_arena",
        "authority": "wwf_office",
        "default": "wwf_arena",
    },
    "wcw": {
        "trainer": "wcw_gym",
        "wrestler": "wcw_arena",
        "announcer": "wcw_arena",
        "authority": "wcw_office",
        "default": "wcw_arena",
    },
    "ecw": {
        "trainer": "ecw_gym",
        "wrestler": "ecw_arena",
        "announcer": "ecw_arena",
        "authority": "ecw_office",
        "default": "ecw_arena",
    },
    "uk": {
        "trainer": "uk_gym",
        "wrestler": "uk_arena",
        "announcer": "uk_arena",
        "default": "uk_arena",
    },
    "japan": {
        "trainer": "jp_gym",
        "wrestler": "jp_arena",
        "announcer": "jp_arena",
        "authority": "jp_office",
        "default": "jp_arena",
    },
}


def _get_npc_room(territory_key, role, rooms):
    """Get the appropriate room for an NPC based on territory and role."""
    mapping = TERRITORY_ROOM_MAP.get(territory_key)
    if not mapping:
        return None
    room_key = mapping.get(role, mapping.get("default"))
    if not room_key:
        return None
    return rooms.get(room_key)


def _spawn_all_named_npcs(rooms):
    """Spawn all named NPC wrestlers from npc_data.py into their home territories."""
    from world.npc_data import NPC_WRESTLERS

    # Clean up existing named NPCs
    existing = search_tag("named_npc", category="npc_type")
    if existing:
        logger.log_info(f"    Cleaning up {len(existing)} existing named NPCs")
        for obj in existing:
            obj.delete()

    spawned = 0
    skipped = 0

    for npc_data in NPC_WRESTLERS:
        territory = npc_data["territory"]
        role = npc_data.get("role", "wrestler")
        room = _get_npc_room(territory, role, rooms)

        if not room:
            skipped += 1
            continue

        npc = create_object(
            "typeclasses.npcs.NPCWrestler",
            key=npc_data["name"],
            location=room,
            tags=[
                (territory, "territory"),
                ("named_npc", "npc_type"),
                (f"npc_{npc_data['npc_id']}", "npc_id"),
            ],
        )
        npc.db.npc_id = npc_data["npc_id"]
        npc.db.based_on = npc_data.get("based_on", "")
        npc.db.role = role
        npc.db.alignment = npc_data.get("alignment", "Face")
        npc.db.finisher_name = npc_data.get("finisher_name", "")
        npc.db.finisher_type = npc_data.get("finisher_type", "power")
        npc.db.level = npc_data.get("level", 1)
        npc.db.home_territory = territory

        s = npc_data.get("stats", (10, 10, 10, 10, 10, 10))
        npc.setup_stats(s[0], s[1], s[2], s[3], s[4], s[5])
        spawned += 1

    logger.log_info(
        f"    Named NPCs: {spawned} spawned, {skipped} skipped "
        f"(territory not yet built)"
    )


def _spawn_all_managers(rooms):
    """Spawn all NPC managers from npc_data.py into their home territories."""
    from world.npc_data import NPC_MANAGERS

    # Clean up existing managers
    existing = search_tag("npc_manager", category="npc_type")
    if existing:
        logger.log_info(f"    Cleaning up {len(existing)} existing managers")
        for obj in existing:
            obj.delete()

    spawned = 0
    skipped = 0

    for mgr_data in NPC_MANAGERS:
        territory = mgr_data["territory"]
        # Managers go to the default room for their territory
        room = _get_npc_room(territory, "default", rooms)

        if not room:
            skipped += 1
            continue

        mgr = create_object(
            "typeclasses.npcs.NPCManager",
            key=mgr_data["name"],
            location=room,
            tags=[
                (territory, "territory"),
                ("npc_manager", "npc_type"),
                (f"npc_{mgr_data['npc_id']}", "npc_id"),
            ],
        )
        mgr.db.npc_id = mgr_data["npc_id"]
        mgr.db.based_on = mgr_data.get("based_on", "")
        mgr.db.alignment = mgr_data.get("alignment", "Heel")
        mgr.db.style = mgr_data.get("style", "")
        mgr.db.specialty = mgr_data.get("specialty", "")
        mgr.db.home_territory = territory
        mgr.db.retainer_cost = mgr_data.get("retainer_cost", 100)
        mgr.db.cut_percent = mgr_data.get("cut_percent", 20)
        mgr.db.available = True

        mgr.setup_stats(
            mgr_data.get("cha", 12),
            mgr_data.get("psy", 12),
        )
        spawned += 1

    logger.log_info(
        f"    Managers: {spawned} spawned, {skipped} skipped "
        f"(territory not yet built)"
    )


def _create_scheduler_script():
    """Create the global NPCSchedulerScript if it doesn't exist."""
    from evennia.scripts.models import ScriptDB

    existing = ScriptDB.objects.filter(db_key="npc_scheduler")
    if existing.exists():
        logger.log_info("    NPCSchedulerScript already exists, skipping")
        return

    script = create_script(
        "typeclasses.scripts.NPCSchedulerScript",
        key="npc_scheduler",
        persistent=True,
    )
    logger.log_info(f"    Created NPCSchedulerScript: {script}")


def _create_economy_script():
    """Create the global EconomyTickScript if it doesn't exist."""
    from evennia.scripts.models import ScriptDB

    existing = ScriptDB.objects.filter(db_key="economy_tick")
    if existing.exists():
        logger.log_info("    EconomyTickScript already exists, skipping")
        return

    script = create_script(
        "typeclasses.scripts.EconomyTickScript",
        key="economy_tick",
        persistent=True,
    )
    logger.log_info(f"    Created EconomyTickScript: {script}")


def _update_limbo_room():
    """Update the default Limbo room (#2) with wrestling backstory."""
    from evennia.objects.models import ObjectDB

    try:
        limbo = ObjectDB.objects.get(id=2)
    except ObjectDB.DoesNotExist:
        logger.log_warn("    Limbo room (#2) not found, skipping")
        return

    limbo.key = "Behind the Curtain"
    limbo.db.desc = (
        "\n"
        "|w============================================================|n\n"
        "\n"
        "|xSomewhere beyond the curtain, between the roar of the crowd\n"
        "and the silence of an empty arena, you stand at the threshold.|n\n"
        "\n"
        "|xThis is a world where all eras of professional wrestling exist\n"
        "at once — where backyard brawlers tape matches on camcorders in\n"
        "VFW halls, where young lions take bumps on concrete floors in\n"
        "Pensacola, where territory kings rule Memphis and Mid-South, and\n"
        "where the bright lights of Madison Square Garden beckon to those\n"
        "with enough talent, grit, and kayfabe to make it.|n\n"
        "\n"
        "|xThe year doesn't matter here. What matters is the |wbusiness|x.|n\n"
        "\n"
        "|xFrom the dusty county fairgrounds of the Gulf Coast to the\n"
        "neon glow of World Class Championship Wrestling in Dallas, from\n"
        "the blood-soaked canvas of ECW's Bingo Hall to the roaring crowds\n"
        "of the Tokyo Dome — every territory is alive, every card is\n"
        "running, and every ring is waiting for someone to step through\n"
        "the ropes.|n\n"
        "\n"
        "|xThe question is: |wcan you protect the business?|n\n"
        "\n"
        "|w============================================================|n\n"
        "\n"
        "  |xYou are about to create your wrestler.|n\n"
        "  |xThe curtain parts. The crowd is waiting.|n\n"
    )
    limbo.save()
    logger.log_info(f"    Updated Limbo room: {limbo.key} (#{limbo.id})")
