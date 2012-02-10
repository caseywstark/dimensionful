"""

Define dimensionalities of common types of quantities.

Copyright 2012, Casey W. Stark.

"""

from sympy import Symbol

# NB: For sanity, we use Gaussian E&M conventions. That is, charge is not
# a fundamental unit and you must use the appropriate form of E&M laws.
num_base = 4

mass = Symbol("(mass)")
length = Symbol("(length)")
time = Symbol("(time)")
temperature = Symbol("(temperature)")

dimensionless = mass**0 * length**0 * time**0 * temperature**0

# inverses
per_mass    = mass**-1
wave_number = length**-1
rate        = time**-1
per_kelvin  = temperature**-1

# lengths
area = length**2
volume = length**3
space_time = length**4
phase_space_volume = length**6

# densities
surface_density = area**-1
number_density  = volume**-1
mass_density    = mass / volume

# length per times
velocity = length / time
acceleration = length / time**2
jerk = length / time**3
snap = length / time**4
crackle = length / time**5
pop = length / time**6

# common dims
momentum = mass * velocity
force  = mass * acceleration
energy = force * length
power = energy / time
charge = (energy * length)**(1/2)
