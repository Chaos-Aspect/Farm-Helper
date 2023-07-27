# constants.py

# Various constants are here

from resources import emojis

# Donator Tiers
DONATOR_TIER = {
    0: "Non Donor",
    1: "Common Donator",
    2: "Talented Donator",
    3: "Wise Donator",
    4: "Expert Donator",
    5: "Masterful Donator"
}

# Energy CD Reduction
DONATOR_REDUCTIONS = {
    0: 1,
    1: 1.1,
    2: 1.3,
    3: 1.55,
    4: 1.55,
    5: 1.55
}

# Donator Emojis
DONATOR_EMOJIS = {
    0: "",
    1: emojis.COMMON_WORKER,
    2: emojis.TALENTED_WORKER,
    3: emojis.WISE_WORKER,
    4: emojis.EXPERT_WORKER,
    5: emojis.MASTERFUL_WORKER
}

# Energy Regeneration Upgrade Values
ENERGY_REGENERATION_UPGRADE_VALUES = {
    0: 1,
    1: 1.2,
    2: 1.35,
    3: 1.5,
    4: 1.6,
    5: 1.7,
    6: 1.75,
    7: 1.8
}

# Energy Regenerated Mode Text
ENERGY_REGENERATED_MODE_MESSAGES = {
    0: "Whenever a new command becomes available.",
    1: "Whenever you gain an energy.",
    2: "Whenever your energy is full."
}