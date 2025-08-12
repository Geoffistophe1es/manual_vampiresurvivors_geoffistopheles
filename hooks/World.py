# Object classes from AP core, to represent an entire MultiWorld and this individual World that's part of it
from worlds.AutoWorld import World
from BaseClasses import MultiWorld, CollectionState
from .functions import get_weapons, get_passives, get_characters, get_stages, filter_dlc, add_if_not_exists

# Object classes from Manual -- extending AP core -- representing items and locations that are used in generation
from ..Items import ManualItem
from ..Locations import ManualLocation

# Raw JSON data from the Manual apworld, respectively:
#          data/game.json, data/items.json, data/locations.json, data/regions.json
#
from ..Data import game_table, item_table, location_table, region_table

# These helper methods allow you to determine if an option has been set, or what its value is, for any player in the multiworld
from ..Helpers import is_option_enabled, get_option_value

# calling logging.info("message") anywhere below in this file will output the message to both console and log file
import logging

########################################################################################
## Order of method calls when the world generates:
##    1. create_regions - Creates regions and locations
##    2. create_items - Creates the item pool
##    3. set_rules - Creates rules for accessing regions and locations
##    4. generate_basic - Runs any post item pool options, like place item/category
##    5. pre_fill - Creates the victory location
##
## The create_item method is used by plando and start_inventory settings to create an item from an item name.
## The fill_slot_data method will be used to send data to the Manual client for later use, like deathlink.
########################################################################################



# Use this function to change the valid filler items to be created to replace item links or starting items.
# Default value is the `filler_item_name` from game.json
def hook_get_filler_item_name(world: World, multiworld: MultiWorld, player: int) -> str | bool:
    return False

# Called before regions and locations are created. Not clear why you'd want this, but it's here. Victory location is included, but Victory event is not placed yet.
def before_create_regions(world: World, multiworld: MultiWorld, player: int):
    pass

# Called after regions and locations are created, in case you want to see or modify that information. Victory location is included.
def after_create_regions(world: World, multiworld: MultiWorld, player: int):
    # Use this hook to remove locations from the world
    locationNamesToRemove = [] # List of location names

    # Add your code here to calculate which locations to remove

    for region in multiworld.regions:
        if region.player == player:
            for location in list(region.locations):
                if location.name in locationNamesToRemove:
                    region.locations.remove(location)
    if hasattr(multiworld, "clear_location_cache"):
        multiworld.clear_location_cache()

# The item pool before starting items are processed, in case you want to see the raw item pool at that stage
def before_create_items_starting(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    return item_pool

# The item pool after starting items are processed but before filler is added, in case you want to see the raw item pool at that stage
def before_create_items_filler(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    # Use this hook to remove items from the item pool
    itemNamesToRemove = [] # List of item names

    # Add your code here to calculate which items to remove.
    #
    # Because multiple copies of an item can exist, you need to add an item name
    # to the list multiple times if you want to remove multiple copies of it.

    for itemName in itemNamesToRemove:
        item = next(i for i in item_pool if i.name == itemName)
        item_pool.remove(item)

    # Generate our filtered list of weapons and stages.

    starting_items = []
    weapons = filter_dlc(world, get_weapons())
    stages = filter_dlc(world, get_stages())

    # Basic starting stages need to be 30 minutes and have no scaling. Otherwise, pick one.
    stage_pool = []
    for stage in stages:
        if world.options.basic_starting_stage > 0:
            if int(stage["Timer"]) < 30 or stage["Scaling"] == "True":
                continue
        stage_pool.append(stage)

    starting_stage = world.random.choice(stage_pool)
    starting_items.append(starting_stage["Stage"])

    # If starters must evolve, remove weapons that don't evolve or would require an unfair advantage in more starting items.
    # Remove Lifesign Scan from the starting pool, as it and Ghost Lino cannot damage enemies.
    weapon_pool = []
    for weapon in weapons:
        if weapon["Item"] == "None" or weapon["Weapon"] == "Vento Sacro" or weapon["Weapon"] == "Spirit Rings":
            if world.options.starter_must_evolve.value > 0:
                continue
        if weapon["Weapon"] in ["Lifesign Scan", "Clock Lancet", "Laurel"]:
            continue
        weapon_pool.append(weapon)

    starting_weapon = world.random.choice(weapon_pool)
    starting_items.append(starting_weapon["Weapon"])
    paired_item = starting_weapon["Item"]
    passives = filter_dlc(world, get_passives())
    for passive in passives:
        if passive["Item"] == "Weapon Power-Up":
            passives.remove(passive)
            break      

    # If a weapon is listed as a Union, player gets the union weapons but no passives.
    # If a weapon does not require anything to evolve, player gets a random passive.
    # Otherwise, player gets the evolution passive required.
    # If a weapon is from Operation Guns, Weapon Power-Up is required and not considered an advantage.
    # If evolution requirements are off, players gets a random passive.
    if world.options.starter_must_evolve.value > 0:
        if paired_item == "Union":
            weapon_name = starting_weapon["Weapon"]
            if weapon_name in ["Peachone", "Ebony Wings"]:
                add_if_not_exists(starting_items, "Peachone")
                add_if_not_exists(starting_items, "Ebony Wings")
            elif weapon_name in ["Phiera Der Tuphello", "Eight the Sparrow"]:
                add_if_not_exists(starting_items, "Phiera Der Tuphello")
                add_if_not_exists(starting_items, "Eight the Sparrow")
                add_if_not_exists(starting_items, "Tirajisu")
            elif weapon_name in ["SpellString", "SpellStream", "SpellStrike"]:
                add_if_not_exists(starting_items, "SpellString")
                add_if_not_exists(starting_items, "SpellStream")
                add_if_not_exists(starting_items, "SpellStrike")
            elif weapon_name in ["Dextro Custos", "Sinestros Custos", "Centralis Custos"]:
                add_if_not_exists(starting_items, "Dextro Custos")
                add_if_not_exists(starting_items, "Sinestros Custos")
                add_if_not_exists(starting_items, "Centralis Custos")
            elif weapon_name in ["Dominus Anger", "Dominus Hatred", "Dominus Agony"]:
                add_if_not_exists(starting_items, "Dominus Anger")
                add_if_not_exists(starting_items, "Dominus Hatred")
                add_if_not_exists(starting_items, "Dominus Agony")
        elif paired_item == "Self":
            starting_items.append(world.random.choice(passives)["Item"])
        else:
            starting_items.append(paired_item)
        if starting_weapon["DLC"] ==  "Operation Guns":
            starting_items.append("Weapon Power-Up")
    else:
        starting_items.append(world.random.choice(passives)["Item"])

    characters = filter_dlc(world, get_characters())
    starting_characters = []
    
    # Roll the character in the event of Charactersanity
    if world.options.charactersanity.value > 0:
        if world.options.character_must_match.value == 0 and world.options.hidden_characters.value > 0 and world.options.secret_characters.value > 0:
            for character in characters:
                add_if_not_exists(starting_characters, character["Character"])
        else:  
            for character in characters:
                # Remove Ghost Lino from the pool, as he cannot deal damage.
                if character["Character"] in ["Ghost Lino"]:
                    characters.remove(character)
            if world.options.character_must_match.value > 0:
                for character in characters:
                    if character["Weapon"] == starting_weapon["Weapon"]:
                        add_if_not_exists(starting_characters, character["Character"])
            if world.options.hidden_characters.value > 0:
                for character in characters:
                    if character["Weapon"] == "Hidden":
                        if world.options.character_must_match.value > 0:
                            if character["Base"] == starting_weapon["Weapon"]:
                                add_if_not_exists(starting_characters, character["Character"])
                        else:
                            add_if_not_exists(starting_characters, character["Character"])
            if world.options.secret_characters.value > 0:
                for character in characters:
                    if character["Weapon"] != character["Base"]:
                        if world.options.character_must_match.value > 0:
                            if character["Base"] == starting_weapon["Weapon"]:
                                add_if_not_exists(starting_characters, character["Character"])
                        else:
                            add_if_not_exists(starting_characters, character["Character"])
        starting_character = world.random.choice(starting_characters)
        starting_items.append(starting_character)

    starting_items_in_pool = [i for i in item_pool if i.name in starting_items]
    # logging.info(starting_items_in_pool)
    for item in starting_items_in_pool:
        multiworld.push_precollected(item)
        item_pool.remove(item)

    return item_pool

    

# The complete item pool prior to being set for generation is provided here, in case you want to make changes to it
def after_create_items(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    return item_pool

# Called before rules for accessing regions and locations are created. Not clear why you'd want this, but it's here.
def before_set_rules(world: World, multiworld: MultiWorld, player: int):
    pass

# Called after rules for accessing regions and locations are created, in case you want to see or modify that information.
def after_set_rules(world: World, multiworld: MultiWorld, player: int):
    # Use this hook to modify the access rules for a given location

    def Example_Rule(state: CollectionState) -> bool:
        # Calculated rules take a CollectionState object and return a boolean
        # True if the player can access the location
        # CollectionState is defined in BaseClasses
        return True

    ## Common functions:
    # location = world.get_location(location_name, player)
    # location.access_rule = Example_Rule

    ## Combine rules:
    # old_rule = location.access_rule
    # location.access_rule = lambda state: old_rule(state) and Example_Rule(state)
    # OR
    # location.access_rule = lambda state: old_rule(state) or Example_Rule(state)

# The item name to create is provided before the item is created, in case you want to make changes to it
def before_create_item(item_name: str, world: World, multiworld: MultiWorld, player: int) -> str:
    return item_name

# The item that was created is provided after creation, in case you want to modify the item
def after_create_item(item: ManualItem, world: World, multiworld: MultiWorld, player: int) -> ManualItem:
    return item

# This method is run towards the end of pre-generation, before the place_item options have been handled and before AP generation occurs
def before_generate_basic(world: World, multiworld: MultiWorld, player: int) -> list:
    pass

# This method is run at the very end of pre-generation, once the place_item options have been handled and before AP generation occurs
def after_generate_basic(world: World, multiworld: MultiWorld, player: int):
    pass

# This is called before slot data is set and provides an empty dict ({}), in case you want to modify it before Manual does
def before_fill_slot_data(slot_data: dict, world: World, multiworld: MultiWorld, player: int) -> dict:
    return slot_data

# This is called after slot data is set and provides the slot data at the time, in case you want to check and modify it after Manual is done with it
def after_fill_slot_data(slot_data: dict, world: World, multiworld: MultiWorld, player: int) -> dict:
    return slot_data

# This is called right at the end, in case you want to write stuff to the spoiler log
def before_write_spoiler(world: World, multiworld: MultiWorld, spoiler_handle) -> None:
    pass

# This is called when you want to add information to the hint text
def before_extend_hint_information(hint_data: dict[int, dict[int, str]], world: World, multiworld: MultiWorld, player: int) -> None:
    
    ### Example way to use this hook: 
    # if player not in hint_data:
    #     hint_data.update({player: {}})
    # for location in multiworld.get_locations(player):
    #     if not location.address:
    #         continue
    #
    #     use this section to calculate the hint string
    #
    #     hint_data[player][location.address] = hint_string
    
    pass

def after_extend_hint_information(hint_data: dict[int, dict[int, str]], world: World, multiworld: MultiWorld, player: int) -> None:
    pass
