"""
Kayfabe: Protect the Business — Exit typeclasses.
"""

from evennia.objects.objects import DefaultExit

from .objects import ObjectParent


class Exit(ObjectParent, DefaultExit):
    """Standard exit between rooms."""
    pass


class TerritoryExit(ObjectParent, DefaultExit):
    """
    Exit that crosses territory boundaries. Checks tier requirements
    and charges travel costs.
    """

    def at_object_creation(self):
        super().at_object_creation()
        self.db.required_tier = 0  # minimum tier to use
        self.db.travel_cost = 0    # dollars to use
        self.db.required_level = 0  # minimum level

    def at_traverse(self, traversing_object, target_location, **kwargs):
        """Check requirements before allowing travel."""
        char = traversing_object

        # Check chargen
        if hasattr(char.db, 'chargen_complete') and not char.db.chargen_complete:
            char.msg("You need to finish character creation first.")
            return

        # Check level requirement
        req_level = self.db.required_level or 0
        if req_level > 0 and hasattr(char.db, 'level'):
            if (char.db.level or 1) < req_level:
                char.msg(f"You need to be at least level {req_level} to travel here.")
                return

        # Check travel cost
        cost = self.db.travel_cost or 0
        if cost > 0 and hasattr(char.db, 'money'):
            if (char.db.money or 0) < cost:
                char.msg(f"You need ${cost} for travel. You have ${char.db.money or 0}.")
                return
            char.db.money -= cost
            char.msg(f"|yYou pay ${cost} for travel.|n")

        super().at_traverse(traversing_object, target_location, **kwargs)
