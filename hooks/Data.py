from .functions import get_weapons, get_passives, get_characters, get_stages, get_arcanas, get_pickups, get_hunts, get_powerups, filter_dlc, add_if_not_exists, create_category, number_of_chests

import logging
# called after the game.json file has been loaded
def after_load_game_file(game_table: dict) -> dict:
    return game_table
# called after the items.json file has been loaded, before any item loading or processing has occurred
# if you need access to the items after processing to add ids, etc., you should use the hooks in World.py
def after_load_item_file(item_table: list) -> list:
    weapons = get_weapons()
    passives = get_passives()
    arcanas = get_arcanas()
    characters = get_characters()
    stages = get_stages()
    pickups = get_pickups()
    powerups = get_powerups()
    weapons.sort(key=lambda x: (x["Order"]))
    passives.sort(key=lambda x: (x["Order"]))
    arcanas.sort(key=lambda x: (x["Order"]))
    characters.sort(key=lambda x: (x["Order"]))
    stages.sort(key=lambda x: (x["Order"]))
    pickups.sort(key=lambda x: (x["Order"]))
    powerups.sort(key=lambda x: (x["Order"]))
    categories = []

    # Generate stages as items
    for item in stages:
        categories.clear()
        categories.append("Stages")
        if item["DLC"] != "None":
            categories.append(item["DLC"])
        item_table.append({
            "sort-key": item["Order"],
            "name": item["Stage"],
            "category": categories.copy(),
            "count":1,
            "progression":"true"
        })

    # Generate pickups as items
    for item in pickups:
        categories.clear()
        categories.append("Stages")
        if item["DLC"] != "None":
            categories.append(item["DLC"])
        item_table.append({
            "sort-key": item["Order"],
            "name": item["Item"],
            "category": categories.copy(),
            "count":1,
            "progression":"true"
        })

    # Generate weapons as items
    for item in weapons:
        categories.clear()
        categories.append("Weapons")
        if item["DLC"] != "None":
            categories.append(item["DLC"])
        if item["ItemSelector"] == "True":
            categories.append("Item Selectors")
        item_table.append({
            "sort-key": item["Order"],
            "name": item["Weapon"],
            "category": categories.copy(),
            "count":1,
            item["Progression"]:"true"
        })

    # Generate passives as items
    for item in passives:
        categories.clear()
        categories.append("Passives")
        if item["DLC"] != "None":
            categories.append(item["DLC"])
        item_table.append({
            "sort-key": item["Order"],
            "name": item["Item"],
            "category": categories.copy(),
            "count":1,
            item["Progression"]:"true"
        })

    # Generate arcanas as items
    for item in arcanas:
        categories.clear()
        categories.append("Arcanas")
        if item["DLC"] != "None":
            categories.append(item["DLC"])
        item_table.append({
            "sort-key": item["Order"],
            "name": item["Item"],
            "category": categories.copy(),
            "count":1,
            item["Progression"]:"true"
        })

    # Generate characters as items
    for item in characters:
        categories.clear()
        categories.append("Characters")
        if item["DLC"] != "None":
            categories.append(item["DLC"])
        item_table.append({
            "sort-key": item["Order"],
            "name": item["Character"],
            "category": categories.copy(),
            "count":1,
            "progression":"true"
        })

    # Generate powerups as items
    for item in powerups:
        categories.clear()
        categories.append("Powerups")
        name = "Powerup - " + item["Powerup"]
        item_table.append({
            "sort-key": item["Order"],
            "name": name,
            "category": categories.copy(),
            "count":int(item["Count"]),
            "useful":"true"
        })

    return item_table

# NOTE: Progressive items are not currently supported in Manual. Once they are,
#       this hook will provide the ability to meaningfully change those.
def after_load_progressive_item_file(progressive_item_table: list) -> list:
    return progressive_item_table

# called after the locations.json file has been loaded, before any location loading or processing has occurred
# if you need access to the locations after processing to add ids, etc., you should use the hooks in World.py
def after_load_location_file(location_table: list) -> list:
    weapons = get_weapons()
    passives = get_passives()
    arcanas = get_arcanas()
    characters = get_characters()
    stages = get_stages()
    pickups = get_pickups()
    hunts = get_hunts()
    weapons.sort(key=lambda x: (x["Order"]))
    passives.sort(key=lambda x: (x["Order"]))
    arcanas.sort(key=lambda x: (x["Order"]))
    characters.sort(key=lambda x: (x["Order"]))
    stages.sort(key=lambda x: (x["Order"]))
    pickups.sort(key=lambda x: (x["Order"]))
    hunts.sort(key=lambda x: (x["Order"]))
    evolutionType = ""
    requires = ""
    name = ""
    categories = []
    insertedUnions = []
    vowels = ["A","E","I","O","U"]

    # Generate evolutions as locations
    for location in weapons:
        evolutionType = location["EvolutionType"]
        # There are six evolution types: Item, Union, Gift, Self, Morph, None, and Special.
        # None does not create a location.
        # Special comprises gifts, which do not have enough examples to properly programmatically handle, or complex evolutions.
        # These are handled in the json as normal.
        if evolutionType == "None" or location["ProgressiveName"] in insertedUnions:
            continue
        categories.clear()
        requires = ""
        name = ""
        
        # Create requirements by Item evolution
        if evolutionType == "Item":
            categories.append("Evolutions")
            name = "Evolve the " + location["Weapon"]
            requires = "|" + location["Weapon"] + "| AND "
            # Singular item required
            if location["Item2"] == "None":
                if location["I1Max"] == "True":
                    requires += "{hasMaxedItem(" + location["Item1"] + ")}"
                else:
                    requires += "{hasItem(" + location["Item1"] + ")}"
            #Multiple items required
            else:
                if location["I2Max"] == "True":
                    requires += "{hasMaxedItems(" + location["Item1"] + ", " + location["Item2"] + ")}"
                else:
                    requires += "{hasItems(" + location["Item1"] + ", " + location["Item2"] + ")}"
        # Create requirements by Union 
        elif evolutionType == "Union":
            insertedUnions.append(location["ProgressiveName"])
            categories.append("Unions")
            requires = "|" + location["Weapon"] + "| AND |"
            # Union of two weapons
            if location["Item2"] == "None":
                name = "Unite the " + location["Weapon"] + " and " + location["Item1"]
                requires += location["Item1"] + "|"
            elif location["Item3"] == "None":
                # Union of three weapons
                name = "Unite the " + location["Weapon"] + ", " + location["Item1"] + ", and " + location["Item2"]
                if location["I2Max"] == "True":
                    requires += location["Item1"] + "| AND |" + location["Item2"] + "|"
                # Union of two weapons and an item
                else:
                    requires += location["Item1"] + "| AND {hasItem(" + location["Item2"] + ")}"
            # Union of four weapons
            else:
                name = "Unite the " + location["Weapon"] + ", " + location["Item1"] + ", " + location["Item2"] + ", and " + location["Item3"]
                requires += location["Item1"] + "| AND |" + location["Item2"] + "| AND |" + location["Item3"] + "|"
        # Create requirements by Gift evolution
        elif evolutionType == "Gift":
            categories.append("Gifts")
            name = "Receive the " + location["ProgressiveName"]
            requires = "|" + location["Weapon"] + "| AND {hasItem(" + location["Item1"] + ")}"
        # Create requirements by Self evolution
        elif evolutionType == "Self":
            categories.append("Evolutions")
            name = "Evolve the " + location["Weapon"]
            requires = "|" + location["Weapon"] + "|"
        # Create requirements by Morph evolution
        elif evolutionType == "Morph":
            categories.append("Morphs")
            name = "Evolve the " + location["Weapon"] + " with " + location["Item2"]
            requires = "|" + location["Weapon"] + "| AND |" + location["Item1"] + "| AND {hasCharacter(" + location["Item2"] + ")}"
        # Create requirements for Special evolution
        elif evolutionType == "Special":
            if location["Weapon"] == "Alucard Swords":
                categories.append("Gifts")
                name = "Receive the " + location["ProgressiveName"]
                requires = "|Alucart Sworb| AND {hasEvolutions(6)}"
            if location["Weapon"] == "Spirit Rings":
                categories.append("Evolutions")
                name = "Evolve the " + location["Weapon"]
                requires = "|" + location["Weapon"] + "| AND |@Passives:5|"
        # Generate the check
        if location["DLC"] != "None":
            categories.append(location["DLC"])
        location_table.append({
            "sort-key": location["Order"],
            "name": name,
            "category": categories.copy(),
            "requires": requires
        })
        # All locations added under this comment are done to preserve order without altering the CSV
        if location["ProgressiveName2"] != "None":
            location_table.append({
                "sort-key": location["Order"],
                "name": "Evolve the " + location["ProgressiveName"],
                "category": categories.copy(),
                "requires": requires
            })
        if location["Weapon"] == "Umbra":
            categories.clear()
            categories.append("Gifts")
            categories.append(location["DLC"])
            location_table.append({
                "sort-key": location["Order"],
                "name": "Receive the Universitas",
                "category": categories.copy(),
                "requires": "|Luminatio| AND |Umbra| AND {hasMaxedItems(Crown,Attractorb)}"
            })



    # Generate chests and stages as locations
    # chest = number_of_chests()
    chest = 20
    name = ""

    for location in stages:
        requires = ""
        requires = "|" + location["Stage"] + "|"
        # Generate chests
        categories.clear()
        categories.append("Chests")
        if location["DLC"] != "None":
            categories.append(location["DLC"])
        for i in range(1, (chest * int(location["Multiplier"])) + 1):
            location_table.append({
                "sort-key": location["Order"],
                "name": location["Stage"] + " Chest " + str(i),
                "category": categories.copy(),
                "requires": requires
            })
        # Generate stage
        requires += " AND {hasPower(5)}"
        location_table.append({
            "sort-key": location["Order"],
            "name": "Complete " + location["Stage"],
            "category": categories.copy(),
            "requires": requires
        })

    # Generate pickups as locations
    indefinite = "a"
    specialPickups = ["Gold Finger", "Sorbetto", "Crystallized Soul"]
    
    for location in pickups:
        categories.clear()
        requires = "{hasPickup(" + location["Item"] + ")}"
        indefinite = "a "
        categories.append("Pickups")
        firstCharacter = location["Item"][0]
        if (firstCharacter in vowels):
            indefinite = "an "
        if location["DLC"] != "None":
            categories.append(location["DLC"])
            if location["DLC"] == "Operation Guns":
                requires = "AND |@Operation Guns: 1|"
            elif location["DLC"] == "Ode to Castlevania":
                requires = "AND {canPickupCastlevania()}"
        if location["Item"] in specialPickups:
            if location["Item"] == "Gold Finger":
                requires = "AND |Astral Stair| OR |Space 54| OR |X - Hail from the Future|"
            elif location["Item"] == "Sorbetto":
                requires = "AND |XII - Out of Bounds| OR |X - Hail from the Future| OR |Whiteout| OR {hasCharacter(Saint Germain)}"
            elif location["Item"] == "Crystallized Soul":
                requires = "AND |XII - Crystal Cries|"
        location_table.append({
            "sort-key": location["Order"],
            "name": "Pick up " + indefinite + location["Item"],
            "category": categories.copy(),
            "requires": requires
        })

    # Generate characters as locations
    for location in characters:
        categories.clear()
        categories.append("Characters")
        requires = ""
        name = "Survive with " + location["Character"]
        requires = "|" + location["Character"] + "| AND {hasPower(2)}"
        if location["DLC"] != "None":
            categories.append(location["DLC"])
        location_table.append({
            "sort-key": location["Order"],
            "name": name,
            "category": categories.copy(),
            "requires": requires
        })

    # Generate hunts as locations
    invalidAreas = ["None", "Inverse", "Hyper/Hurry"]
    for location in hunts:
        categories.clear()
        categories.append("Hunts")
        timer = int(location["Time"])
        if location["Stage"] != "All":
            requires = "|" + location["Stage"] + "|"
        else:
            requires = "|@Stages: 1|"
        if location["Area"] != "None" and "AND" not in location["Area"]:
            requires += " " + location["Area"]
        if timer >= 25:
            requires += " AND {hasPower(5)}"
        elif timer >= 20:
            requires += " AND {hasPower(3)}"
        elif timer >= 15:
            requires += " AND {hasPower(2)}"
        elif timer >= 10:
            requires += " AND {hasPower(1)}"
        name = "Hunt "
        if location["Definite"] != "":
            name += location["Definite"] + " "
        name += location["Boss"] + " "
        if location["Area"] not in invalidAreas:
            name += "in the " + location["Area"] + " "
        if location["Stage"] != "All":
            name += "in " + location["Stage"] + " "
        if timer > 0:
            name += "at " + location["Time"] + ":00"
        if location["DLC"] != "None":
            categories.append(location["DLC"])
        location_table.append({
            "sort-key": location["Order"],
            "name": name,
            "category": categories.copy(),
            "requires": requires
        })
    # for _ in range(5):
    #    stage = random.choice(stages)
    #    character = random.choice(characters)
    #    location_table.append({
    #        "name": "Beat " + stage["Stage"] + " with " + character["Character"],
    #        "requires": "|" + stage["Stage"] + "| AND |" + character["Character"] + "|",
    #        "category": ["Challenges"]
    #    })
    return location_table

# called after the locations.json file has been loaded, before any location loading or processing has occurred
# if you need access to the locations after processing to add ids, etc., you should use the hooks in World.py
def after_load_region_file(region_table: dict) -> dict:
    return region_table

# called after the categories.json file has been loaded
def after_load_category_file(category_table: dict) -> dict:
    return category_table

# called after the meta.json file has been loaded and just before the properties of the apworld are defined. You can use this hook to change what is displayed on the webhost
# for more info check https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/world%20api.md#webworld-class
def after_load_meta_file(meta_table: dict) -> dict:
    return meta_table

# called when an external tool (eg Univeral Tracker) ask for slot data to be read
# use this if you want to restore more data
# return True if you want to trigger a regeneration if you changed anything
def hook_interpret_slot_data(world, player: int, slot_data: dict[str, any]) -> bool:
    return False
