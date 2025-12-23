from BaseClasses import Item, ItemClassification, Location
from itertools import chain

class RustedMossItem(Item):
    game: str = "Rusted Moss"

class RustedMossLocation(Location):
    game: str = "Rusted Moss"

base_id = 144000000

item_locations = {
    "Incendiary_Essence": (ItemClassification.useful, ["Barrows Ceiling Incendiary Essence"]),  #00
    "Tattered_Blindfold": (ItemClassification.useful, ["Ichor Refinery Tattered Blindfold"]),   #01
    "Giant_Chambers": (ItemClassification.useful, ["Factory Roof Giant Chambers"]),             #02
    "Magnet": (ItemClassification.useful, ["Factory Roof Magnet"]),                             #03
    "Ruby_Slippers": (ItemClassification.progression, ["Mountainside Ruby Slippers"]),          #04
    "Fairy_Ointment": (ItemClassification.useful, ["Elfame Fairy Ointment"]),                   #05
    "Energy_Refiner": (ItemClassification.useful, ["Mountainside Energy Refiner"]),             #06
    "Lucky_Clover_Pearl": (ItemClassification.useful, ["Living Quarters Lucky Clover Pearl"]),  #07
    "Time_Manipulator": (ItemClassification.useful, ["Flatlands Time Manipulator"]),            #08
    "Spiced_Gunpowder": (ItemClassification.useful, ["Factory Roof Spiced Gunpowder"]),         #09
    "Powdered_Fae_Silver": (ItemClassification.useful, ["Elfame Powdered Fae Silver"]),         #10
    "Sprites_Breath": (ItemClassification.useful, ["Smoked Forest Sprite's Breath"]),           #11
    "Wing_Clipper": (ItemClassification.useful, ["Living Quarters Wing Clipper"]),              #12
    "Powdered_Nightshade": (ItemClassification.useful, ["Smoked Forest Powdered Nightshade"]),  #13
    "Cracked_Monocle": (ItemClassification.useful, ["Living Quarters Cracked Monocle"]),        #14
    "Magnetic_Bullets": (ItemClassification.useful, ["Lake Magnetic Bullets"]),                 #15
    "Thorny_Rose": (ItemClassification.useful, ["Factory Roof Thorny Rose"]),                   #16
    "Rusted_Coin": (ItemClassification.useful, ["Lab Rusted Coin"]),                            #17
    "Cleansing_Charm": (ItemClassification.progression, ["Ichor Refinery Cleansing Charm"]),    #18
    "Erosive_Bullets": (ItemClassification.useful, ["Factory Roof Erosive Bullets"]),           #19
    "Guardian_Fae": (ItemClassification.useful, ["Mountainside Guardian Fae"]),                 #20
    "Cricket_Bone_Whip": (ItemClassification.useful, ["Barrows Ceiling Cricket Bone Whip"]),    #21
    "Dandelion_Bomb": (ItemClassification.progression, ["Lake Dandelion Bomb"]),                #22
    "Hp_Overload": (ItemClassification.useful, ["Flatlands HP Overload"]),                      #23
    "Heavy_Ammo": (ItemClassification.progression, ["Elfame Heavy Ammo"]),                      #24
    "Short_Fuse": (ItemClassification.useful, ["Smoked Forest Short Fuse"]),                    #25
    "Thorny_Wings": (ItemClassification.useful, ["Flatlands Thorny Wings"]),                    #26
    "Mayas_Trinket": (ItemClassification.progression, ["Lab Maya's Trinket"]),                  #27
    "Ferns_Trinket": (ItemClassification.progression, ["Elfame Fern's Trinket"]),               #28
    "Fae_of_Love": (ItemClassification.useful, ["Lab Fae of Love"]),                            #29
    "Fae_of_Hate": (ItemClassification.useful, ["Lake Fae of Hate"]),                           #30
    "Fae_of_Glass": (ItemClassification.useful, ["Lake Fae of Glass"]),                         #31
    "Titanias_Protection": (ItemClassification.useful, ["Smoked Forest Titania's Protection"]), #32
    "Energy_Disruptor": (ItemClassification.progression, ["Snowy Outpost Energy Disruptor"]),   #33
    "Energy_Converter": (ItemClassification.progression, ["Sunken Library Energy Converter"]),  #34
    "Soft_Fae": (ItemClassification.progression, ["Tundra Temple Soft Fae"]),                   #35
    "Glass_Coin": (ItemClassification.useful, ["Temple of Wild Dance Glass Coin"]),             #36
    "Mossy_Wings": (ItemClassification.progression, ["Court of Ash Mossy Wings"]),              #37
    "Grappling_Hook": (ItemClassification.progression, ["Flatlands Grappling Hook", "Living Quarters Grappling Hook Upgrade", "Elfame Infinite Grapple"]), #38 38-40
    "Charge_Jump": (ItemClassification.progression, ["Factory Roof Charge Jump"]),                                                                         #39 41
    "Grenade": (ItemClassification.progression, ["Snowy Outpost Grenade"]),                                                                                #40 42
    "Titania_Piece": (ItemClassification.progression, ["Flatlands Titania Piece","Smoked Forest Titania Piece","Mountainside Titania Piece","Lab Titania Piece","Ichor Refinery Titania Piece","Living Quarters Titania Piece","Living Quarters Titania Piece (Head)","Lake Titania Piece"]), #41 43-50
    "HP_UP": (ItemClassification.useful, ["Flatlands HP UP (Bottom)","Flatlands HP UP (Top Left)","Flatlands HP UP (Top Right)","Smoked Forest HP UP","Mountainside HP UP","Living Quarters HP UP","Barrows Ceiling HP UP"]), #42 51-57
    "MP_UP": (ItemClassification.useful, ["Flatlands MP UP (Bottom Left)","Flatlands MP UP (Top Right)","Factory Roof MP UP","Smoked Forest MP UP","Mountainside MP UP (Top)","Mountainside MP UP (Bottom)","Ichor Refinery MP UP","Living Quarters MP UP","Lake MP UP"]), #43 58-66
    "TP_UP": (ItemClassification.useful, ["Flatlands TP UP","Factory Roof TP UP (Bottom Left)","Factory Roof TP UP (Middle)","Factory Roof TP UP (Top Right)","Smoked Forest TP UP","Ichor Refinery TP UP","Living Quarters TP UP","Lake TP UP","Barrows Ceiling TP UP"]), #44 67-75
    "Fae_Silver": (ItemClassification.useful, ["Smoked Forest Fae Silver (Bottom Left)","Smoked Forest Fae Silver (Top Right)","Mountainside Fae Silver (Top)","Mountainside Fae Silver (Bottom)","Lab Fae Silver (Left)","Lab Fae Silver (Middle)","Lab Fae Silver (Right)","Ichor Refinery Fae Silver (Top Left)","Ichor Refinery Fae Silver (Bottom Right)","Living Quarters Fae Silver (Top Right)","Living Quarters Fae Silver (Bottom Left)","Lake Fae Silver (Left)","Lake Fae Silver (Right)","Elfame Fae Silver (Left)","Elfame Fae Silver (Middle)","Elfame Fae Silver (Right)","Barrows Ceiling Fae Silver"]), #45 76-92
    "Flag": (ItemClassification.progression, ["Flatlands Flag","Factory Roof Flag","Smoked Forest Flag","Mountainside Flag","Ichor Refinery Flag","Living Quarters Flag"]), #46 93-98
    "Pistol": (ItemClassification.progression, ["Factory Roof Pistol"]), #47 99
    "Shotgun": (ItemClassification.progression, ["Ichor Refinery Shotgun"]), #48 100
    "Rocket_Launcher": (ItemClassification.progression, ["Lake Rocket Launcher"]), #49 101
    "Sniper": (ItemClassification.progression, ["Smoked Forest Sniper"]), #50 102
    "Bolt_Dispenser": (ItemClassification.useful, ["Living Quarters Bolt Dispenser"]), #51 103
    "Rifle": (ItemClassification.useful, []), #52
    "Chest": (ItemClassification.filler, []), #53
}

def get_locations():
    return chain(*(value[1] for value in item_locations.values()))

def get_location_names_to_ids():
    return {item: id for id, item in enumerate(get_locations(), base_id)}

def get_item_name_to_ids():
    return {item: id for id, item in enumerate(item_locations.keys(), base_id)}