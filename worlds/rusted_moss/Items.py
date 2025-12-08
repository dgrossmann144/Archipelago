from BaseClasses import Item, ItemClassification, Location
from itertools import chain

class RustedMossItem(Item):
    game: str = "Rusted Moss"

class RustedMossLocation(Location):
    game: str = "Rusted Moss"

base_id = 144000000

item_locations = {
    "Grappling_Hook": (ItemClassification.progression, ["Flatlands Grappling Hook", "Living Quarters Grappling Hook Upgrade", "Elfame Infinite Grapple"]),
    "Charge_Jump": (ItemClassification.progression, ["Factory Roof Charge Jump"]),
    "Grenade": (ItemClassification.progression, ["Snowy Outpost Grenade"]),
    "Titania_Piece": (ItemClassification.progression, ["Flatlands Titania Piece","Smoked Forest Titania Piece","Mountainside Titania Piece","Lab Titania Piece","Ichor Refinery Titania Piece","Living Quarters Titania Piece","Living Quarters Titania Piece (Head)","Lake Titania Piece"]),
    "HP_UP": (ItemClassification.useful, ["Flatlands HP UP (Bottom)","Flatlands HP UP (Top Left)","Flatlands HP UP (Top Right)","Smoked Forest HP UP","Mountainside HP UP","Living Quarters HP UP","Barrows Ceiling HP UP"]),
    "MP_UP": (ItemClassification.useful, ["Flatlands MP UP (Bottom Left)","Flatlands MP UP (Top Right)","Factory Roof MP UP","Smoked Forest MP UP","Mountainside MP UP (Top)","Mountainside MP UP (Bottom)","Ichor Refinery MP UP","Living Quarters MP UP","Lake MP UP"]),
    "TP_UP": (ItemClassification.useful, ["Flatlands TP UP","Factory Roof TP UP (Bottom Left)","Factory Roof TP UP (Middle)","Factory Roof TP UP (Top Right)","Smoked Forest TP UP","Ichor Refinery TP UP","Living Quarters TP UP","Lake TP UP","Barrows Ceiling TP UP"]),
    "Chest": (ItemClassification.filler, []),
    "Lore": (ItemClassification.deprioritized, []),
    "Fae_Silver": (ItemClassification.useful, ["Smoked Forest Fae Silver (Bottom Left)","Smoked Forest Fae Silver (Top Right)","Mountainside Fae Silver (Top)","Mountainside Fae Silver (Bottom)","Lab Fae Silver (Left)","Lab Fae Silver (Middle)","Lab Fae Silver (Right)","Ichor Refinery Fae Silver (Top Left)","Ichor Refinery Fae Silver (Bottom Right)","Living Quarters Fae Silver (Top Right)","Living Quarters Fae Silver (Bottom Left)","Lake Fae Silver (Left)","Lake Fae Silver (Right)","Elfame Fae Silver (Left)","Elfame Fae Silver (Middle)","Elfame Fae Silver (Right)","Barrows Ceiling Fae Silver"]),
    "Flag": (ItemClassification.progression, ["Flatlands Flag","Factory Roof Flag","Smoked Forest Flag","Mountainside Flag","Ichor Refinery Flag","Living Quarters Flag"]),
    "Pistol": (ItemClassification.progression, ["Factory Roof Pistol"]),
    "Shotgun": (ItemClassification.progression, ["Ichor Refinery Shotgun"]),
    "Rocket_Launcher": (ItemClassification.progression, ["Lake Rocket Launcher"]),
    "Sniper": (ItemClassification.progression, ["Smoked Forest Sniper"]),
    "Bolt_Dispenser": (ItemClassification.useful, ["Living Quarters Bolt Dispenser"]),
    "Incendiary_Essence": (ItemClassification.useful, ["Barrows Ceiling Incendiary Essence"]),
    "Tattered_Blindfold": (ItemClassification.useful, ["Ichor Refinery Tattered Blindfold"]),
    "Giant_Chambers": (ItemClassification.useful, ["Factory Roof Giant Chambers"]),
    "Magnet": (ItemClassification.useful, ["Factory Roof Magnet"]),
    "Ruby_Slippers": (ItemClassification.progression, ["Mountainside Ruby Slippers"]),
    "Fairy_Ointment": (ItemClassification.useful, ["Elfame Fairy Ointment"]),
    "Energy_Refiner": (ItemClassification.useful, ["Mountainside Energy Refiner"]),
    "Lucky_Clover_Pearl": (ItemClassification.useful, ["Living Quarters Lucky Clover Pearl"]),
    "Time_Manipulator": (ItemClassification.useful, ["Flatlands Time Manipulator"]),
    "Spiced_Gunpowder": (ItemClassification.useful, ["Factory Roof Spiced Gunpowder"]),
    "Powdered_Fae_Silver": (ItemClassification.useful, ["Elfame Powdered Fae Silver"]),
    "Sprites_Breath": (ItemClassification.useful, ["Smoked Forest Sprite's Breath"]),
    "Wing_Clipper": (ItemClassification.useful, ["Living Quarters Wing Clipper"]),
    "Powdered_Nightshade": (ItemClassification.useful, ["Smoked Forest Powdered Nightshade"]),
    "Cracked_Monocle": (ItemClassification.useful, ["Living Quarters Cracked Monocle"]),
    "Magnetic_Bullets": (ItemClassification.useful, ["Lake Magnetic Bullets"]),
    "Thorny_Rose": (ItemClassification.useful, ["Factory Roof Thorny Rose"]),
    "Rusted_Coin": (ItemClassification.useful, ["Lab Rusted Coin"]),
    "Cleansing_Charm": (ItemClassification.progression, ["Ichor Refinery Cleansing Charm"]),
    "Erosive_Bullets": (ItemClassification.useful, ["Factory Roof Erosive Bullets"]),
    "Guardian_Fae": (ItemClassification.useful, ["Mountainside Guardian Fae"]),
    "Cricket_Bone_Whip": (ItemClassification.useful, ["Barrows Ceiling Cricket Bone Whip"]),
    "Dandelion_Bomb": (ItemClassification.progression, ["Lake Dandelion Bomb"]),
    "Hp_Overload": (ItemClassification.useful, ["Flatlands HP Overload"]),
    "Heavy_Ammo": (ItemClassification.progression, ["Elfame Heavy Ammo"]),
    "Short_Fuse": (ItemClassification.useful, ["Smoked Forest Short Fuse"]),
    "Thorny_Wings": (ItemClassification.useful, ["Flatlands Thorny Wings"]),
    "Mayas_Trinket": (ItemClassification.progression, ["Lab Maya's Trinket"]),
    "Ferns_Trinket": (ItemClassification.progression, ["Elfame Fern's Trinket"]),
    "Fae_of_Love": (ItemClassification.useful, ["Lab Fae of Love"]),
    "Fae_of_Hate": (ItemClassification.useful, ["Lake Fae of Hate"]),
    "Fae_of_Glass": (ItemClassification.useful, ["Lake Fae of Glass"]),
    "Titanias_Protection": (ItemClassification.useful, ["Smoked Forest Titania's Protection"]),
    "Energy_Disruptor": (ItemClassification.progression, ["Snowy Outpost Energy Disruptor"]),
}

def get_locations():
    return chain(*(value[1] for value in item_locations.values()))

def get_location_names_to_ids():
    return {item: id for id, item in enumerate(get_locations(), base_id)}

def get_item_name_to_ids():
    return {item: id for id, item in enumerate(item_locations.keys(), base_id)}