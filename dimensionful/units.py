"""

Define units and operations.

Copyright 2012, Casey W. Stark.

"""

from sympy.core import AtomicExpr, Basic, Integer, Symbol
from sympy.parsing.sympy_parser import parse_expr

from dimensions import *

unit_symbols_dict = {
    "g":  (1, mass),
    "cm": (1, length),
    "s":  (1, time),
    "K":  (1, temperature),

    "dyne": (1, force),
    "erg":  (1, energy),
    "esu":  (1, charge),

    # some SI
    "m": (1e2, length),
    "J": (1e7, energy),
    "Hz": (1, rate),

    # times
    "min": (60, time),
    "hr":  (3600, time),
    "day": (86400, time),     # check cf
    "yr":  (31536000, time),  # check cf

    # Solar units
    "Msun": (1.98892e33, mass),
    "Rsun": (6.96e10, length),
    "Lsun": (3.9e33, power),
    "Tsun": (5870, temperature),

    # astro distances
    "AU": (1.49598e13, length),
    "pc": (3.0857e18, length),

    # other astro
    "H_0": (2.3e-18, rate),  # check cf
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

class Unit(AtomicExpr):
    """
    Using sympy to represent units as symbols. We just supply extra methods
    so sympy understands how units are related.

    """

    is_positive = True    # make sqrt(m**2) --> m
    is_commutative = True
    is_number = False

    __slots__ = ["symbol", "cgs_value", "dimensions"]

    def __new__(cls, symbol_string, cgs_value=None, dimensions=None,
                **assumptions):
        """
        Build a unit out of symbol string.

        Parameters
        ----------
        symbol_string : string
            This unit's symbol. Used to create the sympy Symbol object
            representing this unit in symbolic expressions.
        cgs_value : float
            This unit's value in cgs.
        dimensions : sympy.core.basic.Basic
            A sympy expression representing the dimensionality of this unit.
            Should just be a sympy.core.mul.Mul object of mass, length, time,
            and temperature to various powers.

        """
        # init obj with superclass construct
        obj = AtomicExpr.__new__(cls, **assumptions)

        ### Handle symbol_string
        # confirm that symbol_string is a string and not empty.
        if not ( isinstance(symbol_string, str) and repr(type(symbol_string)) ):
            raise Exception("Unit objects must be created with a unit symbol string. %s is invalid." % symbol_string)

        # parse it and confirm it gives a symbol
        symbol = Symbol(symbol_string)
        # attach to obj
        obj.symbol = symbol

        ### Handle cgs_value and dimensions
        if cgs_value or dimensions:
            # supplied one of them, so we are not depending on known symbols

            # stupid checks
            if cgs_value and not dimensions:
                raise Exception("Not enough information creating Unit '%s'. Supplied a cgs value, but no dimensions." % symbol_string)
            if dimensions and not cgs_value:
                # assume they wanted it in cgs
                cgs_value = 1
            try:
                cgs_value = float(cgs_value)
            except ValueError:
                raise Exception("Supplied %s as the conversion factor to cgs values. Must supply a float." % cgs_value)

            # confirm that it's a valid dimensionality
            # @todo: actually confirm it is just a Mul of mass, length, ... to
            # some powers
            if not isinstance(dimensions, Basic):
                raise Exception("Dimensions used to create a Unit object must be a sympy expression (sympy.core.basic.Basic)! '%s' is a %s." % (dimensions, type(dimensions)))

            # attach to obj
            obj.cgs_value = cgs_value
            obj.dimensions = dimensions
        else:
            # lookup in default cgs_expressions
            if symbol_string in unit_symbols_dict:
                # lookup successful, attach to obj
                unit_data = unit_symbols_dict[symbol_string]
                obj.cgs_value = unit_data[0]
                obj.dimensions = unit_data[1]
            else:
                # could still be a known symbol with a prefix
                possible_prefix = symbol_string[0]
                if possible_prefix in unit_prefixes:
                    # the first character could be a prefix, check the rest of
                    # the symbol
                    symbol_wo_prefix = symbol_string[1:]

                    if symbol_wo_prefix in unit_symbols_dict:
                        # lookup successful, it's a symbol with a prefix
                        unit_data = unit_symbols_dict[symbol_wo_prefix]
                        prefix_value = unit_prefixes[possible_prefix]
                        # don't forget to account for the prefix value!
                        obj.cgs_value = unit_data[0] * prefix_value
                        obj.dimensions = unit_data[1]
                    else:
                        # no dice
                        raise Exception("Unknown unit symbol '%s'. Please supply them when creating this object." % symbol_string)
                else:
                    # no dice
                    raise Exception("Unknown unit symbol '%s'. Please supply them when creating this object." % symbol_string)

        # return `obj` so __init__ can handle it.
        return obj

    ### some sympy conventions I guess
    def __getnewargs__(self):
        return (self.symbol, self.cgs_value, self.dimensions)

    def __hash__(self):
        return super(Unit, self).__hash__()

    def _hashable_content(self):
        return (self.symbol, self.cgs_value, self.dimensions)
    ### end sympy conventions

    def __repr__(self):
        return str(self.symbol)

    def __str__(self):
        return str(self.symbol)

    # for sympy.printing
    def _sympystr(self, *args):
        return str(self.symbol)

    ### Comparison operators
    def same_dimensions_as(self, other_unit):
        """ Test if dimensions are the same. """
        return (self.dimensions / other_unit.dimensions) == 1

def get_conversion_factor(old_units, new_units):
    """
    Use the conversion factors table to figure out the factor between these two
    units.

    Parameters
    ----------
    old_units: Unit object
        The current units.
    new_units : Unit object
        The units we want.

    Returns
    -------
    conversion_factor : float
        ``old_units / new_units``
    """
    return old_units.cgs_value / new_units.cgs_value
