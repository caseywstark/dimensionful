"""

Define quantities and operations on them.

Copyright 2012, Casey W. Stark.

"""

from dimensionful.units import Unit

# util function
def unit_from_repr(unit_repr):
    """
    Takes a unit object, symbol, or powers array, returns a unit object.

    """
    if isinstance(unit_repr, Unit):
        return unit_repr
    return Unit(unit_repr)

class Quantity:
    """ A physical quantity. So that the machine may understand. """

    def __init__(self, data, units):
        """
        Wrap up the data with the given dimensions and conversion factor.
        Convert the number to different units if needed.

        """
        self.data = data

        # make units
        if isinstance(units, Unit):
            self.units = units
        elif isinstance(units, Quantity):
            # not the cleanest behavior, but users might find this useful. Must
            # multiply data as if this is a unit with a prefactor in cgs.
            self.data *= units.data  # @todo: test this with arrays...
            self.units = units.units
        else:
            self.units = Unit(units)

    def __repr__(self):
        return "%s %s" % (self.data, self.units)

    def __str__(self):
        return "%s %s" % (self.data, self.units)

    def _unit_repr_check_same(self, unit_repr):
        """
        Get unit, whichever representation, and check that it is compatible with
        this quantity.

        """
        unit = unit_from_repr(unit_repr)

        if not self.units.same_dimensions_as(unit):
            raise Exception("Cannot convert to units with different dimensionality. Current unit is %s, argument is %s" % (self.units, unit))

        return unit

    def convert_to(self, unit_repr):
        """
        Convert the data and units to given unit. This does not return the new
        data -- it overwrites the ``data`` and ``units`` attributes. Use it
        wisely.

        """
        unit = self._unit_repr_check_same(unit_repr)
        self.data *= self.units.conversion_factor / unit.conversion_factor
        self.units = unit

    def get_in(self, unit_repr):
        """
        Returns a new quantity in the given units (manipulates data to match).
        Does not manipulate this object.

        """
        unit = self._unit_repr_check_same(unit_repr)
        return Quantity(self.data * self.units.conversion_factor / unit.conversion_factor, unit)

    def get_data_in(self, unit_repr):
        """ Returns converted data only. """
        unit = self._unit_repr_check_same(unit_repr)
        return self.data * self.units.conversion_factor / unit.conversion_factor

    # Could add convert_to_cgs method here.

    def get_in_cgs(self):
        """ Returns a new quantity with CGS values and units. """
        return Quantity(self.data * self.units.conversion_factor, self.units.dimensions)

    def get_data_in_cgs(self):
        """
        Returns data in CGS. Avoids the conversion operation if already in CGS.

        """
        if self.units.conversion_factor != 1.0:
            return self.data * self.units.conversion_factor
        return self.data

    def __add__(self, other_quant):
        """
        Add two quantities, returning a new one. Note the unit behavior!

        If they are in the same units, the data is added directly and the new
        quantity is made with the same units.

        If they are in different units, the second quantity's data is converted
        to the units of the first before addition. The new quantity is made with
        the first quantity's units.

        """
        if not self.units.same_dimensions_as(other_quant.units):
            raise Exception("You can't add these quantities because their dimensions do not match. `%s + %s` is ill-defined" % (self.units, other_quant.units))

        # unit dimension is the same, but might not be the same value
        if self.units == other_quant.units:
            return Quantity((self.data + other_quant.data), self.units)

        # units are not the same, so our units
        return Quantity((self.data + other_quant.get_data_in(self.units)), self.units)

    def __sub__(self, other_quant):
        """
        Subtract two quantities, returning a new one. Note the unit behavior!

        If they are in the same units, the data is subtracted directly and the
        new quantity is made with the same units.

        If they are in different units, the second quantity's data is converted
        to the units of the first before subtraction. The new quantity is made
        with the first quantity's units.

        """
        if not self.units.same_dimensions_as(other_quant.units):
            raise Exception("You can't subtract these quantities because their dimensions do not match. `%s + %s` is ill-defined" % (self.units, other_quant.units))

        # unit dimension is the same, but might not be the same value
        if self.units == other_quant.units:
            return Quantity((self.data - other_quant.data), self.units)

        # units are not the same, so our units
        return Quantity((self.data - other_quant.get_data_in(self.units)), self.units)

    def __mul__(self, other_quant):
        """
        Multiply this quantity by another, or just another number/array. The
        unit objects handle being multiplied by each other.

        """
        if isinstance(other_quant, Quantity):
            return Quantity(self.data * other_quant.data,
                            self.units * other_quant.units)
        return Quantity(self.data * other_quant, self.units)

    def __div__(self, other_quant):
        """
        Divide this quantity by another, or just another number/array. The unit
        objects handle being divided by each other.

        """
        if isinstance(other_quant, Quantity):
            return Quantity(self.data / other_quant.data,
                            self.units / other_quant.units)
        return Quantity(self.data / other_quant, self.units)

    def __pow__(self, power):
        """ Raise this quantity to some power. """
        return Quantity(self.data**power, self.units**power)

    ### less common operations
    def __abs__(self):
        return Quantity(abs(self.data), self.units)

    ### comparison operators
    def __eq__(self, other_quant):
        """ Test equality of data and units. """
        if not self.units.same_dimensions_as(other_quant.units):
            raise Exception("You cannot compare quantities of units %s and %s" % (self.units, other_quant.units))

        if self.data == other_quant.get_data_in(self.units):
            return True
        return False

    def __gt__(self, other_quant):
        """ Test if this data is > other quantity's data. """
        if not self.units.same_dimensions_as(other_quant.units):
            raise Exception("You cannot compare quantities of units %s and %s" % (self.units, other_quant.units))

        if self.data > other_quant.get_data_in(self.units):
            return True
        return False

    def __lt__(self, other_quant):
        """ Test if this data is < other quantity's data. """
        if not self.units.same_dimensions_as(other_quant.units):
            raise Exception("You cannot compare quantities of units %s and %s" % (self.units, other_quant.units))

        if self.data < other_quant.get_data_in(self.units):
            return True
        return False

