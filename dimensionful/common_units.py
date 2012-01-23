"""

Define the common units, in the array of powers form.

Copyright 2012, Casey W. Stark.

"""


import numpy as np

# ones
mass   = np.array((1, 0, 0, 0))
length = np.array((0, 1, 0, 0))
time   = np.array((0, 0, 1, 0))
temp   = np.array((0, 0, 0, 1))

# inverses
per_mass    = np.array((-1, 0, 0, 0))
wave_number = np.array((0, -1, 0, 0))
rate        = np.array((0, 0, -1, 0))
per_kelvin  = np.array((0, 0, 0, -1))

# lengths
area = 2 * length
volume = 3 * length
space_time = 4 * length
phase_space_volume = 6 * length

# densities
surface_density = -area
number_density  = -volume
mass_density    = mass + number_density

# length per times
velocity = length - time
acceleration = length - 2*time
jerk = length - 3*time
snap = length - 4*time
crackle = length - 5*time
pop = length - 6*time

# common dims
momentum = mass + velocity
force  = mass + length - 2*time
energy = force + length
power = energy - time
charge = (energy + length) / 2

common_dimensions = {
    "momentum": np.array((1, 1, -1, 0)),
}

# ``unit_symbols_dict`` is a dictionary of common unit symbols, their dimension,
# and the conversion factor **to** CGS values. The symbol is the key and the
# dimension and conversion factor are held in the tuple value.
unit_symbols_dict = {
    # cgs
    "g":   (mass, 1),
    "cm":  (length, 1),
    "s":   (time, 1),
    "K":   (temp, 1),

    "dyne": (force, 1),
    "erg":  (energy, 1),
    "esu":  (charge, 1),

    # some SI
    "m": (length, 1e2),
    "J": (energy, 1e7),
    "Hz": (rate, 1),

    # times
    "min": (time, 60),
    "hr":  (time, 3600),
    "day": (time, 86400),     # check cf
    "yr":  (time, 31536000),  # check cf
    "t_H": (time, 4.3e8),     # check cf

    # Solar units
    "Msun": (mass, 1.98892e33),
    "Rsun": (length, 6.96e10),
    "Lsun": (power, 3.9e33),
    "Tsun": (temp, 5870),

    # astro distances
    "AU": (length, 1.49598e13),
    "pc": (length, 3.0857e18),

    # other astro
    "H_0": (rate, 2.3e-18),  # check cf
}

unit_prefixes = {
    'Y': 1e24,   # yotta
    'Z': 1e21,   # zetta
    'E': 1e18,   # exa
    'P': 1e15,   # peta
    'T': 1e12,   # tera
    'G': 1e9,    # giga
    'M': 1e6,    # mega
    'k': 1e3,    # kilo
    'd': 1e1,    # deci
    'c': 1e2,    # centi
    'm': 1e-3,   # mili
    'u': 1e-6,   # micro
    'n': 1e-9,   # nano
    'p': 1e-12,  # pico
    'f': 1e-15,  # femto
    'a': 1e-18,  # atto
    'z': 1e-21,  # zepto
    'y': 1e-24,  # yocto
}
