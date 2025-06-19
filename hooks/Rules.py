from typing import Optional
from worlds.AutoWorld import World
from ..Helpers import clamp, get_items_with_value
from BaseClasses import MultiWorld, CollectionState
from .functions import get_stage_by_item

import re

# Sometimes you have a requirement that is just too messy or repetitive to write out with boolean logic.
# Define a function here, and you can use it in a requires string with {function_name()}.
def hasArmaDioAccess(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """Does the player have access to Arma Dio?"""
    if state.has("Arma Dio", player):
        return True
    if world.options.early_arma_dio.value > 0:
        if world.options.include_stage_items.value > 0 and (state.has("Laborratory", player) or state.has("Neo Galuga", player) or state.has("Ode to Castlevania", player)):
            return True
        if hasCharacter(world, multiworld, state, player, "Santa Ladonna"):
            return True
    return False

def hasRevival(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """Does the player have access to a revival as any character?"""
    # Weapon Power-Up is accounted for in JSON outside Neo Galuga, since @Operation Guns DLC:1 is far easier than listing out potential weapons that would spawn one.
    if state.has("Powerup - Revival", player) or hasItem(world, multiworld, state, player, "Tirajisu") or hasArmaDioAccess(world, multiworld, state, player) or state.has("Neo Galuga", player) or hasItem(world, multiworld, state, player, "Academy Badge") or state.has("IV - Awake", player):
        return True
    return False
    
def hasCharacter(world: World, multiworld: MultiWorld, state: CollectionState, player: int, character: str):
    """Does the player have access to a specific character?"""
    # Not the best way of doing this, but it matters in all of 6 cases out of 183, so this is easier.
    if character == "Imelda Belpaese":
        if ((world.options.charactersanity.value > 0 and state.has(character, player)) or (world.options.charactersanity.value == 0 and state.has("Magic Wand", player))):
            return True
        return False
    if character == "Poe Ratcho":
        if ((world.options.charactersanity.value > 0 and state.has(character, player)) or (world.options.charactersanity.value == 0 and state.has("Garlic", player))):
            return True
        return False
    if character == "She-Moon Eeta":
        if ((world.options.charactersanity.value > 0 and state.has(character, player)) or (world.options.charactersanity.value == 0 and state.has("Glass Fandango", player))):
            return True
        return False
    if character == "Santa Ladonna":
        if ((world.options.charactersanity.value > 0 and state.has(character, player)) or (world.options.charactersanity.value == 0 and state.has("Santa Javelin", player))):
            return True
        return False
    if character == "Sara Trantoul":
        if ((world.options.charactersanity.value > 0 and state.has(character, player)) or (world.options.charactersanity.value == 0 and state.has("Star Flail", player))):
            return True
        return False
    if character == "Juste Belmont":
        if ((world.options.charactersanity.value > 0 and state.has(character, player)) or (world.options.charactersanity.value == 0 and state.has("Vibhuti Whip", player))):
            return True
        return False
    return False

def hasItem(world: World, multiworld: MultiWorld, state: CollectionState, player: int, item: str):
    """Does the player have access to a specific item?"""
    if state.has(item, player):
        return True
    if hasArmaDioAccess(world, multiworld, state, player):
        return True
    if world.options.include_stage_items.value > 0:
        for stage in get_stage_by_item(item):
            if state.has(stage, player):
                return True
    return False

def hasMaxedItem(world: World, multiworld: MultiWorld, state: CollectionState, player: int, item: str):
    """Does the player have the ability to fully level a specific item?"""
    # Generally this requires the item unlocked, but there's a few edge cases
    if state.has(item, player):
        return True
    # Stage items - these stages have enough pickups to max out the item without unlocking it.
    if world.options.include_stage_items > 0:
        if item == "Tirajisu" and state.has("Ode to Castlevania", player):
            return True
        if (item == "Candelabrador" or item == "Empty Tome") and state.has("Space 54", player):
            return True
        # Arma Dio - If there's access to Arma Dio and a stage item, passives with 2 levels can be maxed out.
        if world.options.include_stage_items.value > 0 and hasArmaDioAccess(world, multiworld, state, player):
            if item == "Tirajisu" or item == "Duplicator":
                for stage in get_stage_by_item(item):
                    if state.has(stage, player):
                        return True
    # Characters - Adventure reward characters started with a maxed item.
    if item == "Empty Tome" and hasCharacter(world, multiworld, state, player, "Imelda Belpaese"):
        return True
    if item == "Pummarola" and hasCharacter(world, multiworld, state, player, "Poe Ratcho"):
        return True
    if item == "Wings" and hasCharacter(world, multiworld, state, player, "She-Moon Eeta"):
        return True
    return False
