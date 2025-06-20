# Vampire Survivors - Manual AP

## About
Vampire Survivors is an action roguelike game with a multitude of throwbacks to vampire-killing video games of yesteryear. This Manual AP implementation includes randomized weapons, Passives, stages, modes and more! Grow stronger and eventually defeat the Reaper to make the dark night safe again!

This apworld assumes that you have a full-clear save. You can select which DLCs you own in the yaml options.

The original apworld was created by Entropy.

## Setup

* In the Power Up menu, refund all powerups. Max out Reroll, Skip, Banish, and all four Seals.
* In the Collection menu, seal all base weapons and passives. Leave pickups alone. Assuming all DLC, here are the totals as of Emerald Diorama:
* * Version 1.0: 49
* * EXTRA: 57
* * Legacy of the Moonspell: 64
* * Tides of the Foscari: 72
* * Emergency Meeting: 88
* * Operation Guns: 100
* * Ode to Castlevania: 167
* * Emerald Diorama: 184
* At the character select screen, uncheck Eggs and set Max Weapons to the chosen number of weapon slots.
* At the stage select screen, uncheck Hyper, Hurry, Arcanas, Limit Break, Inverse, and Endless.

## Rules

* As you earn items through AP:
* * Unseal weapons and passives in collections.
* * Purchase each powerup that comes in from the main screen.
* Stages, characters, and arcana cannot be sealed. To handle those:
* * You can only play stages you have received through AP.
* * Re-enable the Arcanas modifier when you receive one and limit yourself to only those received.
* * Character selection is based on the **Charactersanity** setting. If it is on, only unlocked characters can be used. If it is off, any character can be used so long as the weapon is unlocked.
* Stage items are determined by the **Stage Items** setting. If it is on, you can pick up items in the stage, but they should still be sealed and thus can't be leveled. If it is off, you must quit the stage if you select a locked item.

## Check Rewards

* Weapons
* Passives
* Arcana
* Powerups
* Stages
* Stage Modes
* Weapon Slots
* Characters (**Charactersanity** only)

## Check Locations

* Regular chests
* Stage pickups
* Surviving stages
* Evolving weapons
* Filling your weapon, accessory, or Arcana slots
* Eliminating **Hunt** targets - see [this map](https://storage.googleapis.com/seedbot/Ode%20to%20Castlevania%20Map.png) for hunt locations in the Ode to Castlevania DLC
* Surviving a stage with specific characters (**Charactersanity** only)

## YAML Options

* **Starting Weapon Slots**: Set how many weapon slots to begin with, between 1 and 6, defaults to 3. The remaining slots will be added to the item pool.
* **Charactersanity**: Adds all characters to the item pool as well as a check for surviving with that character.
* **Hunts**: Adds location checks for defeating specific bosses.
* **Item Selectors**: Adds item selectors into the pool: Arma Dio, Candybox, Morning Star, Coat of Arms, Belnades Spellbook, Spectral Sword, Ebony Diabologue, and Intuition. Unlocking these weapons does *not* unseal all included weapons and are intended to be helpful more than progression.
* **Stage Items**: When enabled, adds logic that may expect picking up sealed stage items for evolutions.
* **Early Arma Dio**: When enabled, adds logic that may expect pulling a sealed item out of Arma Dio for evolutions. When disabled, it is expected that Arma Dio screens are skipped until the item is unlocked.
* **Include DLC**: Each paid DLC has a separate option to enable.

## Victory Condition

* Defeating the Reaper