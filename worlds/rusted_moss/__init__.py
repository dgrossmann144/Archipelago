from dataclasses import asdict
from typing import Dict, Any
from worlds.AutoWorld import World
from BaseClasses import ItemClassification, Region

from .Items import RustedMossItem, item_dict
from .Locations import RustedMossLocation, location_list
from .Options import RustedMossOptions
from .LogicExtractor import extract_logic
from ..generic.Rules import CollectionRule, set_rule

class RustedMossWorld(World):
    """
    Rusted Moss is a metroidvania featuring an elastic physics-based grappling hook.
    """

    game = "Rusted Moss"
    options_dataclass = RustedMossOptions
    options: RustedMossOptions
    topology_present = True
    base_id = 144000000
    item_name_to_id = {item: id for id, item in enumerate(item_dict.keys(), base_id)}
    location_name_to_id = {location: id for id, location in enumerate(location_list, base_id)}
    # Rooms
    regions: set[str]
    # Room: ["Room[transition number]", "Room[transition number]"]
    exits: dict[str, set[str]]
    # From transition: to transition
    connectors: dict[str, str]
    # Location: Room
    location_to_region: dict[str, str]
    # Event names
    events: set
    # Location: access rule logic
    rules: dict[str, str] = {}

    def create_item(self, item: str) -> RustedMossItem:
        return RustedMossItem(item, item_dict[item][0], self.item_name_to_id[item], self.player)
    
    def create_event(self, name, region) -> RustedMossLocation:
        event = RustedMossLocation(self.player, name, None, region)
        event.place_locked_item(RustedMossItem(name, ItemClassification.progression, None, self.player))
        return event
    
    def generate_early(self) -> None:
        (self.regions, self.exits, self.connectors, self.location_to_region, self.events, self.rules) = extract_logic()
        self.multiworld.push_precollected(RustedMossItem("rm_start_0[100390]", ItemClassification.progression, None, self.player))

    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)
        menu_region.add_locations(self.location_name_to_id, RustedMossLocation)
        self.multiworld.regions.append(menu_region)

        for event in self.events:
            eventLocation = self.create_event(event, menu_region)
            menu_region.locations.append(eventLocation)

        for exits in self.exits.values():
            for exit in exits:
                eventLocation = self.create_event(exit, menu_region)
                menu_region.locations.append(eventLocation)
    

    def create_items(self) -> None:
        for item_key, item_value in item_dict.items():
            for count in range(item_value[1]):
                self.multiworld.itempool.append(self.create_item(item_key))

    def set_rules(self) -> None:
        for location, rule in self.rules.items():
            # print("location: " + location)
            # print("rule: " + rule)
            set_rule(self.multiworld.get_location(location, self.player), self.convert_to_rule(rule))

    def fill_slot_data(self) -> Dict[str, Any]:
        return {
            "titania_pieces_required": self.options.titania_pieces_required.value,
            "hard_maya": self.options.hard_maya.value,
            "deathlink": self.options.deathlink.value,
            "damage_boosts": self.options.damage_boost.value,
            "precise_movement": self.options.precise_movement.value,
            "precise_grapple": self.options.precise_grapple.value,
            "bunny_hopping": self.options.bunny_hopping.value,
            "hard_combat": self.options.hard_combat.value,
        }

    def convert_to_rule(self, rule):
        lambda_string = "lambda state: "
        parts = rule.replace("(", "( ").replace(")", " )").split()
        for part in parts:
            if part in "()":
                lambda_string += part
            elif part in "+":
                lambda_string += " and "
            elif part in "|":
                lambda_string += " or "
            elif part in item_dict.keys():
                lambda_string += "state.count(\"" + part + "\", " + str(self.player) + ")"
            elif part in asdict(self.options).keys():
                lambda_string += "True" if asdict(self.options)[part] else "False"
            elif any(part in values for values in self.exits.values()):
                lambda_string += "state.count(\"" + part + "\", " + str(self.player) + ")"
            elif part in self.events:
                lambda_string += "state.count(\"" + part + "\", " + str(self.player) + ")"
        
        # print("lambda_string: " + lambda_string)
        return eval(lambda_string)
