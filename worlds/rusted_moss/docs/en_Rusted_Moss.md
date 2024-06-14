# Rusted Moss

## What does randomization do to this game?
The location of items and abilities are randomized. The ability to teleport is granted to the player at the start, and the player can open the pause menu and click an option to teleport to any teleporter from that menu. The Maya boss fight in the Factory Roof which teleports to the player to the Snowy Outpost upon defeat is always there so the player can get teleported to the Snowy Outpost again. After the player has beaten Maya a first time, her health is set to 1. Some blocks which block the entrance to the Bonnie fight after it has been completed have been removed.

## What Rusted Moss items are randomized?
* Abilities such as the grappling hook, the grappling hook upgrade, the infinite use grappling hook, charge jump, grenade
   * The grappling hook items are treated as progressive upgrades, the first you receive will let you use the grappling hook, the second will let you use the upgraded grappling hook, and the third will let you use the infinite grappling hook.
* Titania Pieces
* HP, MP, and TP upgrades
* Fae Silver
* Flags
* Weapons
* Trinkets

## What does another world's item look like in Rusted Moss?

Items in Rusted Moss appear as they normally do and do not reflect if they are something else or from another game.

## Current Version (Alpha v0.1.0) Limitations and Issues
* There is no indication to the player in game that they have received an item.
* Many of the yaml settings are drastically underused with some only being considered in one or two rooms.
* If the sniper is one of your first items the seed might not be beatable because of the mana cost of firing the sniper. Within a room I only counted the Sniper to be in logic if it required \< 3 uses, but this does not consider if the player has to traverse multiple rooms consecutively. A similar limitation probably exists for grenade and damage boosts, but is much less likely to be an issue due to their lesser prevelance. I plan to resolve the sniper issue by hopefully modifying it to still be able to fire without mana, but also doing no damage if that is the case.
* No check for if the player has the TP to equip all required trinkets for logic is in place.
* Logic for combat arenas was always assumed to be doable based on room traversal alone, no accounting for the difficulty of the encounter was considered. This ties back to the hard combat yaml option being underused.
* Logic for bosses is similarly lacking, it does include loose logic for what would be required to do the fight hitless, but for some of the later bosses this is an unreasonable expectation to make of the player.
* Logic heavily relies on the player quick switching between weapons using the number keys to stack knockback. Logic that has this expectation should probably be put behind another yaml option to allow players on controller or players who are not comfortable with quick switching to generate always beatable seeds.