import typing
from dataclasses import dataclass
from Options import Option, Toggle, Range, PerGameCommonOptions

class TitaniaPiecesRequired(Range):
    """How many pieces of Titania are required to complete the game."""
    display_name = "Titania Pieces Required"
    default = 5
    range_start = 0
    range_end = 8

class HardMaya(Toggle):
    """Choose to enable the hard version of the Living Quarters Maya fight."""
    display_name = "Hard Maya"

class Deathlink(Toggle):
    """Enable death link."""
    display_name = "Death Link"

@dataclass
class RustedMossOptions(PerGameCommonOptions):
    titania_pieces_required: TitaniaPiecesRequired
    hard_maya: HardMaya
    deathlink: Deathlink