"""

Define dimensionalities of common types of quantities.

Copyright 2012, Casey W. Stark. See LICENSE.txt for more information.

"""

from sympy import Symbol, Rational

# NB: For sanity, we use Gaussian E&M conventions. That is, charge is not
# a fundamental unit and you must use the appropriate form of E&M laws.

# Number of base dimensions
num_base = 4

# The base dimensions
mass = Symbol("(mass)", positive=True)
length = Symbol("(length)", positive=True)
time = Symbol("(time)", positive=True)
temperature = Symbol("(temperature)", positive=True)
base_dimensions = [mass, length, time, temperature]

# If something is dimensionless, its dimension is just 1.
dimensionless = mass**0 * length**0 * time**0 * temperature**0

# inverses
per_mass    = mass**-1
wave_number = length**-1
rate        = time**-1
per_kelvin  = temperature**-1

# lengths
area               = length**2
volume             = length**3
space_time         = length**4
phase_space_volume = length**6

# densities
surface_density = area**-1
number_density  = volume**-1
mass_density    = mass / volume

# length per times
velocity     = length / time
acceleration = length / time**2
jerk         = length / time**3
snap         = length / time**4
crackle      = length / time**5
pop          = length / time**6

# common physics dims
momentum = mass * velocity
force    = mass * acceleration
energy   = force * length
power    = energy / time
charge   = (energy * length)**Rational(1, 2)  # proper 1/2 power

electric_field = charge / length**2
magnetic_field = electric_field
