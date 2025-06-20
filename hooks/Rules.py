from typing import Optional
from worlds.AutoWorld import World
from ..Helpers import clamp, get_items_with_value
from BaseClasses import MultiWorld, CollectionState
from .functions import get_stage_by_item, get_castlevania_pickup_list

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
        if hasCharacter(world, multiworld, state, player, "Santa Ladonna") or hasCharacter(world, multiworld, state, player, "Engineer Gino"):
            return True
        if state.has("X - Hail from the Future", player):
            return True
    return False

def hasMultipleArmaDioAccess(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """Does the player have access to multiple Arma Dios?"""
    # Ways to get multiple Arma Dios
    #   Having it unlocked and access to a stage where it's an item
    #   Including locked stage items and access to a stage where multiple Arma Dios are found
    # Stages where multiple Arma Dios are found - Neo Galuga, Ode to Castlevania
    if state.has("Arma Dio", player) and (state.has("Laborratory", player) or state.has("Neo Galuga", player) or state.has("Ode to Castlevania", player)):
        return True
    if world.options.early_arma_dio.value > 0:
        if world.options.include_stage_items.value > 0 and (state.has("Neo Galuga", player) or state.has("Ode to Castlevania", player)):
            return True
        if state.has("Engineer Gino", player) or state.has("X - Hail from the Future", player):
            return True
        # Opting to remove this requirement for multiples, as this adds RNG of getting Arma Dio before level 40
        # if hasCharacter(world, multiworld, state, player, "Santa Ladonna"):
        #    return True
    return False

def hasRevival(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """Does the player have access to a revival as any character?"""
    hasStage = False
    # Weapon Power-Up can be used with Neo Galuga if stage items are allowed, or Neo Galuga and the item unlocked, but Academy Badge needs to be leveled to provide revival.
    #   Accounted for in JSON outside Neo Galuga, since @Operation Guns DLC:2 is far easier than listing out potential weapons that would spawn one.
    if ((world.options.include_stage_items.value > 0 or state.has("Weapon Power-Up", player)) and state.has("Neo Galuga", player)) or (state.has("Academy Badge", player) and (state.has("Lake Foscari", player) or state.has("Abyss Foscari", player))):
        hasStage = True
    if state.has("Powerup - Revival", player) or hasItem(world, multiworld, state, player, "Tirajisu") or hasArmaDioAccess(world, multiworld, state, player) or hasStage or state.has("IV - Awake", player):
        return True
    return False
    
def hasCharacter(world: World, multiworld: MultiWorld, state: CollectionState, player: int, character: str):
    """Does the player have access to a specific character?"""
    # Not the best way of doing this, but it matters in 7 cases out of 183, so this is easier.
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
    if character == "Saint Germain":
        if ((world.options.charactersanity.value > 0 and state.has(character, player)) or (world.options.charactersanity.value == 0 and state.has("Globus", player))):
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
        for stage in get_stage_by_item(item, state.has("VIII - Mad Groove", player)):
            if state.has(stage, player):
                return True
    return False

def hasItems(world: World, multiworld: MultiWorld, state: CollectionState, player: int, item1: str, item2: str):
    """Does the player have access to two specific items?"""
    first_item = False
    second_item = False

    first_unlocked = False
    first_armadio = False
    first_stage = False
    first_stages = []
    second_unlocked = False
    second_armadio = False
    second_stage = False
    second_stages = []

    # For weapons with multiple requirements, we want to be sure we aren't assuming the same Arma Dio is being used multiple times or returning true because two separate stages are used.
    if state.has(item1, player):
        first_unlocked = True
        first_item = True
    if hasArmaDioAccess(world, multiworld, state, player):
        usedArmaDio = True
        first_armadio = True
        first_item = True
    if world.options.include_stage_items.value > 0:
        for stage in get_stage_by_item(item1, state.has("VIII - Mad Groove", player)):
            if state.has(stage, player):
                first_item = True
                first_stage = True
                first_stages.append(stage)
    if first_item:
        if state.has(item2, player):
            second_item = True
            second_unlocked = True
        if hasArmaDioAccess(world, multiworld, state, player):
            second_item = True
            second_armadio = True
        if world.options.include_stage_items.value > 0:
            for stage in get_stage_by_item(item2, state.has("VIII - Mad Groove", player)):
                if state.has(stage, player):
                    second_item = True
                    second_stage = True
                    second_stages.append(stage)
    
    if first_item and second_item:
        if (first_unlocked and second_item) or (second_unlocked and first_item): # One item unlocked, other item however
            return True
        if (first_stage and second_armadio) or (first_armadio and second_stage): # One item through stage, one item through Arma Dio
            return True
        if (first_armadio and second_armadio and hasMultipleArmaDioAccess(world, multiworld, state, player)): # Both items through Arma Dio, if multiple access exists
            return True
        if (first_stage and second_stage): # Both items through the same stage
            for stage1 in first_stages:
                for stage2 in second_stages:
                    if stage1 == stage2:
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
                for stage in get_stage_by_item(item, state.has("VIII - Mad Groove", player)):
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

def hasMaxedItems(world: World, multiworld: MultiWorld, state: CollectionState, player: int, item1: str, item2: str):
    """Does the player have the ability to fully level two specific items?"""
    # As of Emerald Diorama, there is no way for this to return true if both items aren't unlocked, but futureproofing now.
    first_item = False
    second_item = False

    first_unlocked = False
    first_character = False
    first_stage = False
    first_stages = []
    first_armadio = False

    second_unlocked = False
    second_character = False
    second_stage = False
    second_stages = []
    second_armadio = False
    if state.has(item1, player):
        first_item = True
        first_unlocked
    # Characters - Adventure reward characters started with a maxed item.
    if item1 == "Empty Tome" and hasCharacter(world, multiworld, state, player, "Imelda Belpaese"):
        first_item = True
        first_character = True
    if item1 == "Pummarola" and hasCharacter(world, multiworld, state, player, "Poe Ratcho"):
        first_item = True
        first_character = True
    if item1 == "Wings" and hasCharacter(world, multiworld, state, player, "She-Moon Eeta"):
        first_item = True
        first_character = True
    # Stage items - these stages have enough pickups to max out the item without unlocking it.
    if world.options.include_stage_items > 0:
        if item1 == "Tirajisu" and state.has("Ode to Castlevania", player):
            first_item = True
            first_stage = True
            first_stages.append("Ode to Castlevania")
        elif (item1 == "Candelabrador" or item1 == "Empty Tome") and state.has("Space 54", player):
            first_item = True
            first_stage = True
            first_stages.append("Space 54")
    # Arma Dio - If there's access to Arma Dio and a stage item, passives with 2 levels can be maxed out.
    if world.options.include_stage_items.value > 0 and hasArmaDioAccess(world, multiworld, state, player):
        if item1 == "Tirajisu" or item1 == "Duplicator":
            for stage in get_stage_by_item(item1, state.has("VIII - Mad Groove", player)):
                if state.has(stage, player):
                    first_item = True
                    first_armadio = True
                    first_stages.append(stage)
    if first_item:
        if state.has(item2, player):
            second_item = True
            second_unlocked = True
        # Characters - Adventure reward characters started with a maxed item.
        if item2 == "Empty Tome" and hasCharacter(world, multiworld, state, player, "Imelda Belpaese"):
            second_item = True
            second_character = True
        if item2 == "Pummarola" and hasCharacter(world, multiworld, state, player, "Poe Ratcho"):
            second_item = True
            second_character = True
        if item2 == "Wings" and hasCharacter(world, multiworld, state, player, "She-Moon Eeta"):
            second_item = True
            second_character = True
        # Stage items - these stages have enough pickups to max out the item without unlocking it.
        if world.options.include_stage_items > 0:
            if item2 == "Tirajisu" and state.has("Ode to Castlevania", player):
                second_item = True
                second_stage = True
                second_stages.append("Ode to Castlevania")
            elif (item2 == "Candelabrador" or item2 == "Empty Tome") and state.has("Space 54", player):
                second_item = True
                second_stage = True
                second_stages.append("Space 54")
        # Arma Dio - If there's access to Arma Dio and a stage item, passives with 2 levels can be maxed out.
        if world.options.include_stage_items.value > 0 and hasArmaDioAccess(world, multiworld, state, player):
            if item2 == "Tirajisu" or item2 == "Duplicator":
                for stage in get_stage_by_item(item2, state.has("VIII - Mad Groove", player)):
                    if state.has(stage, player):
                        second_item = True
                        second_armadio = True
                        second_stages.append(stage)
    
    if first_item and second_item:
        if (first_unlocked and second_item) or (second_unlocked and first_item): # One item unlocked, other item however
            return True
        if (first_character and (second_stage or second_armadio)) or (second_character and (first_stage or first_armadio)): # One item through character, one item through stage or Arma Dio
            return True
        if (first_stage and second_armadio) or (first_armadio and second_stage) or (first_stage and second_stage) or (first_armadio and second_armadio and hasMultipleArmaDioAccess(world, multiworld, state, player)): # Both items through the same stage or Arma Dio, if multiple access exists
            for stage1 in first_stages:
                for stage2 in second_stages:
                    if stage1 == stage2:
                        return True
            
    return False

def canPickupCastlevania(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    if state.has("Ode to Castlevania", player):
        return True
    search = ""
    
    if world.options.charactersanity.value > 0:
        search = "Characters"
    else:
        search = "Weapons"
    
    for item in get_castlevania_pickup_list(search):
        if state.has(item["Item"], player):
            return True
    
    return False