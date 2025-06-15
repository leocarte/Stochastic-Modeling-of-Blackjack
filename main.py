import numpy as np
from setup_variables import setup_variables
from set_strategy import set_strategy
from adv_single_hand import adv_single_hand

# %%% SETUP %%%

setup_variables()

# %%% COMPUTATIONS — BASIC STRATEGY %%%

strategy = set_strategy('basic')

deck = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 4], dtype=float) / 13


playerAdvantage = adv_single_hand(deck, strategy)

print("Player advantage (basic strategy):", playerAdvantage)


