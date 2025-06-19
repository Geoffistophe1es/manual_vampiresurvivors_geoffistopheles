# Object classes from AP that represent different types of options that you can create
from Options import FreeText, NumericOption, Toggle, DefaultOnToggle, Choice, TextChoice, Range, NamedRange

# These helper methods allow you to determine if an option has been set, or what its value is, for any player in the multiworld
from ..Helpers import is_option_enabled, get_option_value



####################################################################
# NOTE: At the time that options are created, Manual has no concept of the multiworld or its own world.
#       Options are defined before the world is even created.
#
# Example of creating your own option:
#
#   class MakeThePlayerOP(Toggle):
#       """Should the player be overpowered? Probably not, but you can choose for this to do... something!"""
#       display_name = "Make me OP"
#
#   options["make_op"] = MakeThePlayerOP
#
#
# Then, to see if the option is set, you can call is_option_enabled or get_option_value.
#####################################################################


# To add an option, use the before_options_defined hook below and something like this:
#   options["total_characters_to_win_with"] = TotalCharactersToWinWith
#
class WeaponSlots(Range):
    """Set how many weapon slots to start with. There are 6 slots total, and any remaining slots above this choice will be added to the item pool."""
    display_name = "Number of starting weapon slots"
    range_start = 1
    range_end = 6
    default = 3

class Hunts(Toggle):
    """Adds checks for defeating specific enemies"""
    display_name = "Hunts"
    default = False
#####################################################################
# Geoffistopheles: Commented out while debating these requirements. The special weapons don't work this way in base game and seems unnecessarily restrictive.
#                   Current thought is to change the logic to allow an unlock so long as one of the requisite weapons is unlocked.
#class SpecialWeapons(Toggle):
#    """Adds 5 checks for completing the requirements for the Special Weapons in Ode to Castlevania. WARNING: These each require many items and will likely take a long time to complete. *Requires the Ode to Castlevania DLC"""
#    display_name = "Special Weapons"
#    default = False
#####################################################################

class Charactersanity(Toggle):
    """Adds all characters to the item pool as well as a location check for each."""
    display_name = "Charactersanity"
    default = False

class IncludeOperationGunsDLC(Toggle):
    """Whether or not the Operation Guns DLC is included."""
    display_name = "Include Operation Guns DLC"
    default = True

class IncludeMoonspellDLC(Toggle):
    """Whether or not the Legacy of the Moonspell DLC is included."""
    display_name = "Include Legacy of the Moonspell DLC"
    default = True

class IncludeEmergencyMeetingDLC(Toggle):
    """Whether or not the Emergency Meeting DLC is included."""
    display_name = "Include Emergency Meeting DLC"
    default = True

class IncludeFoscariDLC(Toggle):
    """Whether or not the Tides of the Foscari DLC is included."""
    display_name = "Include Tides of the Foscari DLC"
    default = True

class IncludeCastlevaniaDLC(Toggle):
    """Whether or not the Ode to Castlevania DLC is included."""
    display_name = "Include Ode to Castlevania DLC"
    default = True

class IncludeEmeraldDioramaDLC(Toggle):
    """Whether or not the Emerald Diorama DLC is included."""
    display_name = "Include Emerald Diorama DLC"
    default = True

class IncludeStageItems(Toggle):
    """Whether or not items found in a stage are considered in logic."""
    display_name = "Include Stage Items"
    default = True

class IncludeItemSelectors(Toggle):
    """Whether or not items that can be used to select other items can be unlocked. This includes Candybox, Arma Dio, Morning Star, Coat of Arms, Belnades Spellbook, Spectral Sword, Ebony Diabolique, and Intuition."""
    display_name = "Include Item Selectors"
    default = True

class EarlyArmaDio(Toggle):
    """Arma Dio can be substituted for nineteen items without unlocking them, and can be found in four locations without unlocking it. Requires Include Item Selectors to function.
    True: Early Arma Dio usage is potentially expected in logic.
    False: Arma Dio usage is prohibited until unlocked."""
    display_name = "Early Arma Dio"
    default = False

# This is called before any manual options are defined, in case you want to define your own with a clean slate or let Manual define over them
def before_options_defined(options: dict) -> dict:
    options["starting_weapon_slots"] = WeaponSlots
    options["charactersanity"] = Charactersanity
    options["hunts"] = Hunts
    options["include_stage_items"] = IncludeStageItems
    options["include_item_selectors"] = IncludeItemSelectors
    options["early_arma_dio"] = EarlyArmaDio
    # options["special_weapons"] = SpecialWeapons
    options["include_moonspell_dlc"] = IncludeMoonspellDLC
    options["include_foscari_dlc"] = IncludeFoscariDLC
    options["include_emergency_meeting_dlc"] = IncludeEmergencyMeetingDLC
    options["include_operation_guns_dlc"] = IncludeOperationGunsDLC
    options["include_castlevania_dlc"] = IncludeCastlevaniaDLC
    options["include_emerald_diorama_dlc"] = IncludeEmeraldDioramaDLC
    return options

# This is called after any manual options are defined, in case you want to see what options are defined or want to modify the defined options
def after_options_defined(options: dict) -> dict:
    return options