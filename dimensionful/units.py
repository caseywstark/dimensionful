"""

Define units and operations on them.

Copyright 2012, Casey W. Stark. See LICENSE.txt for more information.

"""

from sympy import Expr, Mul, Number, Pow, Symbol, sympify
from sympy.parsing.sympy_parser import parse_expr

from dimensionful.dimensions import *

# Dictionary holding information of known unit symbols. The key is the symbol,
# the value is a tuple with the conversion factor to cgs, and the
# dimensionality.
unit_symbols_dict = {
    # base
    "g":  (1, mass),
    "cm": (1, length),
    "s":  (1, time),
    "K":  (1, temperature),

    # other cgs
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
    "ly": (9.46053e17, length),
    "pc": (3.08568e18, length),

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

def get_unit_data_from_expr(unit_expr, cgs_value=None, dimensions=None):
    """
    Gets total cgs_value and dimensions from a unit expression.

    """
    if cgs_value and dimensions:
        return (cgs_value, dimensions)

    if isinstance(unit_expr, Symbol):
        return get_unit_data_from_symbol(unit_expr, cgs_value, dimensions)

    elif isinstance(unit_expr, Number):
        return (1, 1)

    elif isinstance(unit_expr, Pow):
        unit_data = get_unit_data_from_expr(unit_expr.args[0])
        power = unit_expr.args[1]
        return (unit_data[0]**power, unit_data[1]**power)

    elif isinstance(unit_expr, Mul):
        for i, expr in enumerate(unit_expr.args):
            unit_data = get_unit_data_from_expr(expr)
            # @todo: stupid
            if cgs_value:
                cgs_value *= unit_data[0]
            else:
                cgs_value = unit_data[0]
            if dimensions:
                dimensions *= unit_data[1]
            else:
                dimensions = unit_data[1]

        return (cgs_value, dimensions)

    raise Exception("Cannot get unit data from '%s'." % str(unit_expr))

def get_unit_data_from_symbol(unit_expr, cgs_value, dimensions):
    """
    Utility for getting cgs_value and dimensions arguments, or pulling
    the info of a known unit symbol, for a single symbol.

    """
    if cgs_value or dimensions:
        # supplied one of them, so we are not depending on known symbols

        # get the most common case out of the way
        if cgs_value and dimensions:
            return (cgs_value, dimensions)

        # stupid checks
        if cgs_value and not dimensions:
            raise Exception("Not enough information creating Unit '%s'. Supplied a cgs value, but no dimensions." % str(unit_expr))
        if dimensions and not cgs_value:
            # assume they wanted it in cgs
            cgs_value = 1
        # make sure cgs_value is actually a number
        try:
            cgs_value = float(cgs_value)
        except ValueError:
            raise Exception("Supplied %s as the conversion factor to cgs values. Must supply a float." % cgs_value)

        # confirm that it's a valid dimensionality
        # @todo: actually confirm it is just a Mul of mass, length, ...
        # to some powers.
        if not isinstance(dimensions, Expr):
            raise Exception("Dimensions used to create a Unit object must be a sympy expression (sympy.core.basic.Basic)! '%s' is a %s." % (str(dimensions), type(dimensions)))

        return (cgs_value, dimensions)

    # try to find in known units
    return lookup_unit_symbol(str(unit_expr))

def lookup_unit_symbol(symbol_string):
    """
    Find the unit data of this symbol. Raise an exception if not found.

    """

    if symbol_string in unit_symbols_dict:
        # lookup successful, return the tuple directly
        return unit_symbols_dict[symbol_string]

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
            return (unit_data[0] * prefix_value, unit_data[1])

    # no dice
    raise Exception("Unknown unit symbol '%s'. Please supply them when creating this object." % symbol_string)


class Unit(Expr):
    """
    Using sympy to represent units as symbols. We just supply extra methods
    so sympy understands how units are related.

    """

    is_positive = True    # make sqrt(m**2) --> m
    is_commutative = True
    is_number = False

    __slots__ = ["symbol", "is_atomic", "expr", "cgs_value", "dimensions"]

    def __new__(cls, unit_expr=None, cgs_value=None, dimensions=None,
                **assumptions):
        """
        Build a new unit. May be an atomic unit (like a gram) or a combination
        of other units (like g / cm**3). Either way, you can make the unit
        symbol anything.

        Parameters
        ----------
        unit_expr : string or sympy.core.expr.Expr
            The symbolic expression. Symbol(g) for gram.
        cgs_value : float
            This unit's value in cgs. 1.0 for gram.
        dimensions : sympy.core.expr.Expr
            A sympy expression representing the dimensionality of this unit.
            Should just be a sympy.core.mul.Mul object of mass, length, time,
            and temperature objects to various powers. (mass) for gram.

        """
        # Check for no args
        if not unit_expr:
            unit_expr = sympify(1)

        # if we have a string, parse into an expression
        if isinstance(unit_expr, str):
            unit_expr = parse_expr(unit_expr)

        if not isinstance(unit_expr, Expr):
            raise Exception("Unit representation must be a string or sympy Expr. %s is a %s" % (unit_expr, type(unit_expr)))
        # done with argument checking...

        # see if the unit is atomic.
        is_atomic = False
        if isinstance(unit_expr, Symbol):
            is_atomic = True

        print ""
        print unit_expr
        print cgs_value
        print dimensions

        # this call handles if there is not enough information between the three
        # arguments and our known unit symbols
        this_cgs_value, this_dimensions = \
            get_unit_data_from_expr(unit_expr, cgs_value, dimensions)

        print this_cgs_value
        print this_dimensions
        print ""

        # init obj with superclass construct
        obj = Expr.__new__(cls, **assumptions)

        # attach attributes to obj
        obj.expr = unit_expr
        obj.is_atomic = is_atomic
        obj.cgs_value = this_cgs_value
        obj.dimensions = this_dimensions

        # return `obj` so __init__ can handle it.
        return obj

    ### some sympy conventions I guess
    def __getnewargs__(self):
        return (self.expr, self.is_atomic, self.cgs_value, self.dimensions)

    def __hash__(self):
        return super(Unit, self).__hash__()

    def _hashable_content(self):
        return (self.expr, self.is_atomic, self.cgs_value, self.dimensions)
    ### end sympy conventions

    def __repr__(self):
        return str(self.expr)

    def __str__(self):
        return str(self.expr)

    # for sympy.printing
    def _sympystr(self, *args):
        return str(self.expr)

    ### override sympy operations
    def __mul__(self, right_object):
        """ Multiply Unit with right_object (Unit). """
        return Unit(self.expr * right_object.expr,
                    self.cgs_value * right_object.cgs_value,
                    self.dimensions * right_object.dimensions)

    def __div__(self, right_object):
        """ Divide Unit by right_object (Unit). """
        print self.expr, right_object.expr, self.expr / right_object.expr
        print self.cgs_value, right_object.cgs_value, self.cgs_value / right_object.cgs_value
        print self.dimensions, right_object.dimensions, self.dimensions / right_object.dimensions

        return Unit(self.expr / right_object.expr,
                    self.cgs_value / right_object.cgs_value,
                    self.dimensions / right_object.dimensions)

    def __pow__(self, power):
        """ Take Unit to a power. """
        return Unit(self.expr**power, self.cgs_value**power,
                    self.dimensions**power)

    ### Comparison operators
    def same_dimensions_as(self, other_unit):
        """ Test if dimensions are the same. """
        return (self.dimensions / other_unit.dimensions) == 1

    def __eq__(self, other_unit):
        """ Test equality: dimensions and cgs_value. """
        return ( self.cgs_value == other_unit.cgs_value
                 and self.dimensions == other_unit.dimensions )

    @property
    def is_dimensionless(self):
        return self.dimensions == 1

# util function
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
