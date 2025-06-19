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
    stage_items_file = 'stage_items.csv' # has the list of available packs
    rows = []

    with get_csv_file(stage_items_file) as opened_file:
        reader = csv.DictReader(opened_file)

        for row in reader:
            rows.append(row)

    return rows

def get_stage_by_item(item: str) -> list:
    rows = []
    
    for row in get_stage_items():
        if row["Item"] == item:
            rows.append(row["Stage"])

    return rows
