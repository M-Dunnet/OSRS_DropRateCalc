'''
Drop rate calculator for Old School RuneScape.
--------------------------
How it works:
--------------------------
For individual drops:
- drop_chance(drop_rate, kills): Calculates the chance of getting at least one drop after a certain number of kills.
- kills_for_confidence(drop_rate, confidence): Calculates the number of kills needed to achieve a certain confidence level of getting at least one drop.
- drop_rate_interval(drop_rate, interval=0.95): Calculates the range of kills in which a given percentage of players are expected to receive at least one drop.

For multiple drops:
- MultiDropSimulator(drops, simulations=100000): Class to simulate kills to collect all desired drops from a monster with given drop rates.
- combined_expected_kills(): Calculates the expected number of kills to collect all drops.
- combined_kills_for_confidence(confidence): Calculates the number of kills needed to achieve a certain confidence level of collecting all drops.
- individual_drop_rate_intervals(interval=0.95): Calculates the drop rate intervals for each individual drop.
- combined_drop_interval(interval=0.95): Calculates the combined drop rate interval for collecting all drops.

The MutliDropSimulator requires a python dictionary of drop names and their respective drop rates. 
Python dictionary format: {"Drop1 Name": drop_rate_fraction, "Drop2 Name: drop_rate_fraction, ...}
Example (Note the drop name must be in quotes and the drop rate must be in fraction format): 
drops = {"Dragon 2h sword": 1/358, "Dragon pickaxe": 1/358, "Skull of vet'ion": 1/618}
'''
from lib.DropRateCalc import MultiDropSimulator, drop_chance, kills_for_confidence, drop_rate_interval

###############
## See the ReadMe file for instructions on how to use this script ##
## Use Hash (#) to comment out lines you don't want to run ##
## Example usage below (replace with desired drop rates and parameters) ##
###############

# Individual drop calculations
drop_chance(drop_rate=1/50, kills=75)
kills_for_confidence(drop_rate=1/50, confidence=0.90)
drop_rate_interval(drop_rate=1/50, interval=0.5)

# Multiple drop calculations
drops = {
    "Dragon 2h sword": 1/358,
    "Dragon pickaxe": 1/358,
    "Skull of vet'ion": 1/618
}

simulator = MultiDropSimulator(drops)
simulator.combined_expected_kills()
simulator.combined_kills_for_confidence(confidence=0.9)
simulator.individual_drop_rate_intervals(interval=0.5)
simulator.combined_drop_interval(interval=0.5)

