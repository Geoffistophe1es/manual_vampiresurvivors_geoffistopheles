# added some convenience functions in here so we can access them from any hook files

import os
import pkgutil
import csv
import re

from io import StringIO

from worlds.AutoWorld import World

###
# File, item, and location functions
###

# we have to get the raw data from our CSV files to pass to a parser, so had to copy our own version of this method
# this gets the contents of the file from pkgutil and passes it back as a "file" for csv parsing later
def get_csv_file(*args) -> dict:
    fname = os.path.join("data", *args)
    package_base_name = re.sub(r'\.hooks\.\w+$', '.Data', __name__)

    try:
        filedata = pkgutil.get_data(package_base_name, fname).decode()
    except:
        filedata = ""

    return StringIO(filedata)

def get_stage_items() -> list:
    stage_items_file = 'stage_items.csv'
    rows = []

    with get_csv_file(stage_items_file) as opened_file:
        reader = csv.DictReader(opened_file)

        for row in reader:
            if (row["Type"] == "Passive"):
                rows.append(row)

    return rows

def get_stage_pickups() -> list:
    stage_items_file = 'stage_items.csv'
    rows = []

    with get_csv_file(stage_items_file) as opened_file:
        reader = csv.DictReader(opened_file)

        for row in reader:
            if (row["Type"] == "Pickup"):
                rows.append(row)

    return rows

def get_weapons() -> list:
    weapons_file = 'weapons.csv' 
    rows = []

    with get_csv_file(weapons_file) as opened_file:
        reader = csv.DictReader(opened_file)

        for row in reader:
            rows.append(row)

    return rows

def get_passives() -> list:
    passives_file = 'passives.csv' 
    rows = []

    with get_csv_file(passives_file) as opened_file:
        reader = csv.DictReader(opened_file)

        for row in reader:
            rows.append(row)

    return rows

def get_characters() -> list:
    characters_file = 'characters.csv' 
    rows = []

    with get_csv_file(characters_file) as opened_file:
        reader = csv.DictReader(opened_file)

        for row in reader:
            rows.append(row)

    return rows

def get_stages() -> list:
    stages_file = 'stages.csv' 
    rows = []

    with get_csv_file(stages_file) as opened_file:
        reader = csv.DictReader(opened_file)

        for row in reader:
            rows.append(row)

    return rows


def get_stage_by_item(item: str, madGrooveRequired: bool) -> list:
    rows = []
    
    for row in get_stage_items():
        if row["Item"] == item:
            if row["Stage"] == "Boss Rash":
                if madGrooveRequired:
                    rows.append(row["Stage"])
            else:
                rows.append(row["Stage"])

    return rows

def get_castlevania_pickup_list(category: str) -> list:
    pickup_file = ''
    rows = []

    if category == "Weapons":
        pickup_file = "cvpickups_weapons.csv"
    elif category == "Characters":
        pickup_file = "cvpickups_characters.csv"
    else:
        return rows
    
    with get_csv_file(pickup_file) as opened_file:
        reader = csv.DictReader(opened_file)

        for row in reader:
            rows.append(row)

    return rows

def filter_dlc(world: World, items: list) -> list:
    for item in items:
        dlc = item["DLC"]
        if dlc == "None":
            continue
        elif dlc == "Moonspell":
            if world.options.include_moonspell_dlc == 0:
                items.remove(item)
        elif dlc == "Foscari":
            if world.options.include_foscari_dlc == 0:
                items.remove(item)
        elif dlc == "Among Us":
            if world.options.include_emergency_meeting_dlc == 0:
                items.remove(item)
        elif dlc == "Operation Guns":
            if world.options.include_operation_guns_dlc == 0:
                items.remove(item)
        elif dlc == "Castlevania":
            if world.options.include_castlevania_dlc == 0:
                items.remove(item)
        elif dlc == "Emerald":
            if world.options.include_emerald_diorama_dlc == 0:
                items.remove(item)
    
    return items

def add_if_not_exists(items: list, item: str) -> list:
    items.append(item) if item not in items else items

    return items
