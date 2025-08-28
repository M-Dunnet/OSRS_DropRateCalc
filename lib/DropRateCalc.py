'''
Drop-rate calculator for old-school RuneScape.
Given a drop rate, it calculates the chance of getting at least one drop
after a certain number of kills.
'''
import math
import random
import numpy as np
from scipy import stats


### Functions for single drop rate calculations ###
def drop_chance(drop_rate, kills):
    """
    Calculate the chance of getting at least one drop after a certain number of kills.

    Parameters:
    drop_rate (float): The drop rate (e.g., 1/128 for a 1 in 128 chance).
    kills (int): The number of kills.
    """
    if drop_rate <= 0 or kills <= 0:
        return 0.0
    no_drop_chance = (1 - drop_rate) ** kills
    print(f"Chance of drop after {kills} rolls: {(1 - no_drop_chance) * 100:.4f}%")
    

def kills_for_confidence(drop_rate, confidence):
    """
    Calculate the number of kills needed to achieve a certain confidence level of getting at least one drop.

    Parameters:
    drop_rate (float): The drop rate (e.g., 1/128 for a 1 in 128 chance).
    confidence (float): The desired confidence level (between 0 and 1).
    """
    if drop_rate <= 0 or confidence <= 0 or confidence >= 1:
        return float('inf')
    if drop_rate >= 1:  # guaranteed drop every kill
        return 1
    kills = math.log(1 - confidence) / math.log(1 - drop_rate)

    print(f"Rolls needed for {confidence*100:.2f}% chance of drop: {math.ceil(kills)}")


def drop_rate_interval(drop_rate, interval=0.95):
    """
    Calculate the range of kills in which a given percentage of players are expected
    to receive at least one drop.

    This is based on the geometric distribution. For example, with a 95% confidence
    interval and a 1/128 drop rate, 95% of players will get their first drop between
    the lower and upper bounds returned.

    Parameters:
    drop_rate (float): The drop rate (0 < drop_rate <= 1, e.g. 1/128 for a 1 in 128 chance).
    confidence_interval (float): The desired confidence level (default is 0.95, i.e. 95%).

    Returns:
    tuple: (lower_bound, upper_bound) number of kills where the first drop is expected
           to occur for the given confidence interval.
    """
    if not (0 < drop_rate <= 1):
        return (float('inf'), float('inf'))
    if not (0 < interval < 1):
        return (float('inf'), float('inf'))
    if drop_rate == 1:
        return (1, 1)

    alpha = 1 - interval
    lower = stats.geom.ppf(alpha / 2, drop_rate)
    upper = stats.geom.ppf(1 - alpha / 2, drop_rate)

    print(f"{interval*100:.2f}% of players will get their first drop between {int(lower)} and {int(upper)} rolls.")



### Class and Methods for multiple drop rate calculations ###
class MultiDropSimulator:
    """
    Simulates kills to collect all desired drops from a monster with given drop rates.
    """
    def __init__(self, drops, simulations=100000):
        """
        Initialize the simulator and run the Monte Carlo simulation.

        Parameters:
        drops (dict): item -> drop_rate (0 < drop_rate <= 1)
        simulations (int): number of simulations to estimate the distribution
        """
        self.drops = drops
        self.simulations = simulations
        self.items = list(drops.keys())
        self.probs = [drops[item] for item in self.items]
        self.kills_per_sim = self._run_simulation()

    def _run_simulation(self):
        kills_per_sim = []
        for _ in range(self.simulations):
            obtained = set()
            kills = 0
            while len(obtained) < len(self.items):
                kills += 1
                for i, p in enumerate(self.probs):
                    if random.random() < p:
                        obtained.add(self.items[i])
            kills_per_sim.append(kills)
        return np.array(kills_per_sim)


    def combined_expected_kills(self):
        """
        Return the average number of kills needed to collect all items.
        """
        print(f"Average rolls for all drops: {math.ceil(np.mean(self.kills_per_sim))}")


    def combined_kills_for_confidence(self, confidence=0.95):
        """
        Return the number of kills needed such that there is a 'confidence' chance
        of obtaining all items.
        
        Parameters:
        confidence (float): Desired probability (0 < confidence < 1)
        """
        if not (0 < confidence < 1):
            print("Confidence must be between 0 and 1.")
        else:
            print(f"Rolls needed for {confidence*100:.2f}% chance of all drops: {int(np.percentile(self.kills_per_sim, confidence * 100))}")

    
    def individual_drop_rate_intervals(self, confidence=0.95):
        """
        Compute the expected interval of kills for each item drop rate
        based on a geometric distribution approximation.

        Parameters:
        confidence_interval (float): Desired confidence (default 0.95)

        Returns:
        dict: item -> (lower_bound, upper_bound) number of kills
        """
        intervals = {}
        for item, drop_rate in self.drops.items():
            if not (0 < drop_rate <= 1):
                intervals[item] = (float('inf'), float('inf'))
            elif drop_rate == 1:
                intervals[item] = (1, 1)
            elif not (0 < confidence < 1):
                intervals[item] = (float('inf'), float('inf'))
            else:
                alpha = 1 - confidence
                lower = stats.geom.ppf(alpha / 2, drop_rate)
                upper = stats.geom.ppf(1 - alpha / 2, drop_rate)
                intervals[item] = (int(lower), int(upper))

        print(f"Individual item rolls needed for a {confidence*100:.2f}% chance of drop:")
        for item, bounds in intervals.items():
            print(f"\t{item}: {bounds[0]} to {bounds[1]} rolls")


    def combined_drop_interval(self, confidence_interval=0.95):
        """
        Compute the expected interval of kills needed to collect all items
        based on the simulated distribution.

        Parameters:
        confidence_interval (float): Desired confidence (default 0.95)

        Returns:
        tuple: (lower_bound, upper_bound) number of kills for the given confidence
        """
        if not (0 < confidence_interval < 1):
            return (float('inf'), float('inf'))

        alpha = 1 - confidence_interval
        lower = np.percentile(self.kills_per_sim, alpha / 2 * 100)
        upper = np.percentile(self.kills_per_sim, (1 - alpha / 2) * 100)

        print(f"{confidence_interval*100:.2f}% of players will get all drop between {int(lower)} and {int(upper)} rolls.")



