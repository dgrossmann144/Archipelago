from BaseClasses import Item, ItemClassification

class RustedMossItem(Item):
    game: str = "Rusted Moss"

item_dict = {
    "Grappling_Hook": (ItemClassification.progression, 1),
    "Grappling_Hook_Upgrade": (ItemClassification.progression, 1),
    "Infinite_Grapple": (ItemClassification.progression, 1),
    "Charge_Jump": (ItemClassification.progression, 1),
    "Grenade": (ItemClassification.progression, 1),
    "Titania_Piece": (ItemClassification.progression, 8), # 8
    "HP_UP": (ItemClassification.useful, 7), # 7
    "MP_UP": (ItemClassification.useful, 9), # 9
    "TP_UP": (ItemClassification.useful, 9), # 9
    "Fae_Silver": (ItemClassification.useful, 17), # 17
    "Pistol": (ItemClassification.useful, 1),
    "Shotgun": (ItemClassification.progression, 1),
    "Rocket_Launcher": (ItemClassification.progression, 1),
    "Sniper": (ItemClassification.progression, 1),
    "Bolt_Dispenser": (ItemClassification.useful, 1),
    "Incendiary_Essence": (ItemClassification.useful, 1),
    "Tattered_Blindfold": (ItemClassification.useful, 1),
    "Giant_Chambers": (ItemClassification.useful, 1),
    "Magnet": (ItemClassification.useful, 1),
    "Ruby_Slippers": (ItemClassification.useful, 1),
    "Fairy_Ointment": (ItemClassification.useful, 1),
    "Energy_Refiner": (ItemClassification.useful, 1),
    "Lucky_Clover_Pearl": (ItemClassification.useful, 1),
    "Time_Manipulator": (ItemClassification.useful, 1),
    "Spiced_Gunpowder": (ItemClassification.useful, 1),
    "Powdered_Fae_Silver": (ItemClassification.useful, 1),
    "Sprites_Breath": (ItemClassification.useful, 1),
    "Wing_Clipper": (ItemClassification.useful, 1),
    "Powdered_Nightshade": (ItemClassification.useful, 1),
    "Cracked_Monocle": (ItemClassification.useful, 1),
    "Magnetic_Bullets": (ItemClassification.useful, 1),
    "Thorny_Rose": (ItemClassification.useful, 1),
    "Rusted_Coin": (ItemClassification.useful, 1),
    "Cleansing_Charm": (ItemClassification.useful, 1),
    "Erosive_Bullets": (ItemClassification.useful, 1),
    "Guardian_Fae": (ItemClassification.useful, 1),
    "Cricket_Bone_Whip": (ItemClassification.useful, 1),
    "Dandelion_Bomb": (ItemClassification.useful, 1),
    "Hp_Overload": (ItemClassification.useful, 1),
    "Heavy_Ammo": (ItemClassification.useful, 1),
    "Short_Fuse": (ItemClassification.useful, 1),
    "Thorny_Wings": (ItemClassification.useful, 1),
    "Mayas_Trinket": (ItemClassification.useful, 1),
    "Ferns_Trinket": (ItemClassification.useful, 1),
    "Fae_of_Love": (ItemClassification.useful, 1),
    "Fae_of_Hate": (ItemClassification.useful, 1),
    "Fae_of_Glass": (ItemClassification.useful, 1),
    "Titanias_Protection": (ItemClassification.useful, 1),
    "Energy_Disruptor": (ItemClassification.useful, 1),
}