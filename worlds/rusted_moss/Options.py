from dataclasses import dataclass
from Options import Toggle, Choice, PerGameCommonOptions, Range

# class TitaniaPiecesRequired(Range):
#     """How many pieces of Titania are required to complete the game."""
#     display_name = "Titania Pieces Required"
#     default = 5
#     range_start = 0
#     range_end = 8

class Ending(Choice):
    """The ending of the game required to win"""
    display_name = "Required Ending"
    option_ending_a = 0
    option_ending_b = 1
    option_ending_c = 2
    option_ending_d = 3
    option_ending_e = 4
    default = 0

class RouteRequired(Choice):
    """Main route of the game required to win"""
    display_name = "Required Route"
    option_neutral = 0
    option_pacifist = 1
    option_genocide = 2
    option_all_routes = 3
    default = 0

class Character(Choice):
    """The character you want to play as, currnently only fern and gimmick are supported"""
    display_name = "Character"
    option_fern = 0
    option_maya = 1
    option_ameli = 2
    option_gimmick = 3
    default = 0

class HardMaya(Toggle):
    """Choose to enable the hard version of the Living Quarters Maya fight"""
    display_name = "Hard Maya"

class Deathlink(Toggle):
    """Enable death link."""
    display_name = "Death Link"

class DamageBoost(Toggle):
    """Locations which require a damage boost to access will be considered in logic"""
    display_name = "Damage Boost"

class GrenadeBoost(Toggle):
    """Locations which require a grenade boost to access will be considered in logic"""
    display_name = "Grenade Boost"

class PreciseMovement(Toggle):
    """Locations which require precise movement to access will be considered in logic"""
    display_name = "Precise Movement"

class PreciseGrapple(Toggle):
    """Locations which require precise grappling hook usage to access will be considered in logic"""
    display_name = "Precise Grapple"
    default = 1

class BunnyHopping(Toggle):
    """Locations which require preservation of momentum through bunny hopping will be considered in logic"""
    display_name = "Bunny Hopping"

class HardCombat(Toggle):
    """Locations which require more proficiency in combat to access will be considered in logic"""
    display_name = "Hard Combat"

class ShopDiscountPercentage(Range):
    """Discount percentage to apply to shop prices to reduce money farming requirement"""
    display_name = "Shop Item Cost Percentage"
    default = 50
    range_start = 1
    range_end = 100

class MinMP(Range):
    """Minimum MP value. Value of at least 5 makes Sniper and Grenade jumps more forgiving"""
    display_name = "Minimum MP"
    default = 5
    range_start = 0
    range_end = 39

@dataclass
class RustedMossOptions(PerGameCommonOptions):
    # titania_pieces_required: TitaniaPiecesRequired
    ending: Ending
    character: Character
    hard_maya: HardMaya
    deathlink: Deathlink
    damage_boost: DamageBoost
    grenade_boost: GrenadeBoost
    precise_movement: PreciseMovement
    precise_grapple: PreciseGrapple
    bunny_hopping: BunnyHopping
    hard_combat: HardCombat
    shop_discount_percentage: ShopDiscountPercentage
    min_mp: MinMP