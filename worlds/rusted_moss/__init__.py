from worlds.AutoWorld import World
from worlds.generic.Rules import set_rule
from BaseClasses import Region

from .Items import RustedMossItem, item_dict
from .Locations import RustedMossLocation, location_list
from .Options import RustedMossOptions

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
    
    def create_item(self, item: str) -> RustedMossItem:
        return RustedMossItem(item, item_dict[item][0], self.item_name_to_id[item], self.player)

    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)

        main_region = Region("Main", self.player, self.multiworld)
        main_region.add_locations(self.location_name_to_id, RustedMossLocation)
        self.multiworld.regions.append(main_region)

        menu_region.connect(main_region)

    def create_items(self) -> None:
        for item_key, item_value in item_dict.items():
            for count in range(item_value[1]):
                self.multiworld.itempool.append(self.create_item(item_key))
