"""

Define quantities and operations on them.

Copyright 2012, Casey W. Stark.

"""

from dimensionful.units import Unit

# util function
def unit_from_repr(unit_repr):
    """
    Takes a unit object, symbol, or powers array. Returns a unit object.

    """
    if isinstance(unit_repr, Unit):
        return unit_repr
    return Unit(unit_repr)

# @todo: Verify that we need type checks in all of the left and right operator
# methods (ex: __add__ and __radd__). I think they are only needed in the left
# case. If something hits the right operator method of a Quantity object, the
# left_object must not be a Quantity object. Leaving them until I can test more.

class Quantity:
    """
    A physical quantity. Attaches units to data.

    """
    def __init__(self, data, unit_repr):
        """
        Create a quantity. Combine units with the data.

        Parameters
        ----------
        data : object
            The data making up this quantity.
        unit_repr : Unit object or string
            The units the data are in.

        """
        self.data = data

        # make units
        if isinstance(unit_repr, Unit):
            self.units = unit_repr
        elif isinstance(unit_repr, Quantity):
            # not the cleanest behavior, but users might find this useful. Must
            # multiply data as if this is a unit with a prefactor in cgs.
            self.data *= unit_repr.data  # @todo: test this with arrays...
            self.units = unit_repr.units
        else:
            self.units = Unit(unit_repr)

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

        Parameters
        ----------
        unit_repr : Unit object or string
            The units you want the data in.

        """
        unit = self._unit_repr_check_same(unit_repr)
        self.data *= self.units.conversion_factor / unit.conversion_factor
        self.units = unit

    def get_in(self, unit_repr):
        """
        Returns a new quantity in the given units (manipulates data to match).
        Does not manipulate this object.

        Parameters
        ----------
        unit_repr : Unit object or string
            The units you want to get a new quantity in.

        Returns
        -------
        New Quantity

        """
        unit = self._unit_repr_check_same(unit_repr)
        return Quantity(self.data * self.units.conversion_factor / unit.conversion_factor, unit)

    def get_data_in(self, unit_repr):
        """
        Returns converted data only.

        Parameters
        ----------
        unit_repr : Unit object or string
            The units you want the data in.

        Returns
        -------
        data : object
            This quantity's data, in the desired units.

        """
        unit = self._unit_repr_check_same(unit_repr)

        # don't operate on data if given the same units
        if self.units == unit:
            return self.data

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

    def __add__(self, right_object):
        """
        Add this quantity to the object on the right of the `+` operator. Must
        check for the correct (same dimension) units. If the quantities have
        different units, we always use the units on the left.

        """
        if isinstance(right_object, Quantity):  # make sure it's a quantity before we check units attribute
            if not self.units.same_dimensions_as(right_object.units):
                raise Exception("You cannot add these quantities because their dimensions do not match. `%s + %s` is ill-defined" % (self.units, right_object.units))
        else:  # the only way this works is with a float so...
            if self.units.is_dimensionless:
                raise Exception("You cannot add a pure number to a dimensional quantity. `%s + %s` is ill-defined." % (self, right_object))

            # case of self + float
            return Quantity(self.data + right_object, self.units)

        # `get_data_in` will not apply the conversion if the units are the same
        return Quantity(self.data + right_object.get_data_in(self.units),
                        self.units)

    def __radd__(self, left_object):
        """
        Add this quantity to the object on the left of the `+` operator. Must
        check for the correct (same dimension) units. If the quantities have
        different units, we always use the units on the left.

        """
        if isinstance(left_object, Quantity):  # make sure it's a quantity before we check units attribute
            if not self.units.same_dimensions_as(left_object.units):
                raise Exception("You cannot add these quantities because their dimensions do not match. `%s + %s` is ill-defined" % (left_object.units, self.units))
        else:  # the only way this works is with a float so...
            if self.units.is_dimensionless:
                raise Exception("You cannot add a pure number to a dimensional quantity. `%s + %s` is ill-defined." % (left_object, self))

            # case of float + self
            return Quantity(left_object + self.data, self.units)

        # `get_data_in` will not apply the conversion if the units are the same
        return Quantity((left_object.data
                         + self.get_data_in(left_object.units)),
                        left_object.units)

    def __sub__(self, right_object):
        """
        Subtract the object on the right of the `-` from this quantity. Must
        check for the correct (same dimension) units. If the quantities have
        different units, we always use the units on the left.

        """
        if isinstance(right_object, Quantity):  # make sure it's a quantity before we check units attribute
            if not self.units.same_dimensions_as(right_object.units):
                raise Exception("You cannot add these quantities because their dimensions do not match. `%s - %s` is ill-defined" % (self.units, right_object.units))
        else:  # the only way this works is with a float so...
            if self.units.is_dimensionless:
                raise Exception("You cannot add a pure number to a dimensional quantity. `%s - %s` is ill-defined." % (self, right_object))

            # case of self + float
            return Quantity(self.data - right_object, self.units)

        # `get_data_in` will not apply the conversion if the units are the same
        return Quantity(self.data - right_object.get_data_in(self.units),
                        self.units)

    def __rsub__(self, left_object):
        """
        Subtract this quantity from the object on the left of the `-` operator.
        Must check for the correct (same dimension) units. If the quantities
        have different units, we always use the units on the left.

        """
        if isinstance(left_object, Quantity):  # make sure it's a quantity before we check units attribute
            if not self.units.same_dimensions_as(left_object.units):
                raise Exception("You cannot add these quantities because their dimensions do not match. `%s - %s` is ill-defined" % (left_object.units, self.units))
        else:  # the only way this works is with a float so...
            if self.units.is_dimensionless:
                raise Exception("You cannot add a pure number to a dimensional quantity. `%s - %s` is ill-defined." % (left_object, self))

            # case of float + self
            return Quantity(left_object - self.data, self.units)

        # `get_data_in` will not apply the conversion if the units are the same
        return Quantity((left_object.data
                         - self.get_data_in(left_object.units)),
                        left_object.units)

    def __mul__(self, right_object):
        """
        Multiply this quantity by the object on the right of the `*` operator.
        The unit objects handle being multiplied by each other.

        """
        if isinstance(right_object, Quantity):
            return Quantity(self.data * right_object.data,
                            self.units * right_object.units)

        # `right_object` is not a Quantity object, so try to use it as
        # dimensionless data.
        return Quantity(self.data * right_object, self.units)

    def __rmul__(self, left_object):
        """
        Multiply this quantity by the object on the left of the `*` operator.
        The unit objects handle being multiplied by each other.

        """
        if isinstance(left_object, Quantity):
            return Quantity(left_object.data * self.data,
                            left_object.units * self.units)

        # `left_object` is not a Quantity object, so try to use it as
        # dimensionless data.
        return Quantity(left_object * self.data, self.units)

    def __div__(self, right_object):
        """
        Divide this quantity by the object on the right of the `/` operator. The
        unit objects handle being divided by each other.

        """
        if isinstance(right_object, Quantity):
            return Quantity(self.data / right_object.data,
                            self.units / right_object.units)

        # `right_object` is not a Quantity object, so try to use it as
        # dimensionless data.
        return Quantity(self.data / right_object, self.units)

    def __rdiv__(self, left_object):
        """
        Divide the object on the left of the `/` operator by this quantity. The
        unit objects handle being divided by each other.

        """
        if isinstance(left_object, Quantity):
            return Quantity(left_object.data / self.data,
                            left_object.units / self.units)

        # `left_object` is not a Quantity object, so try to use it as
        # dimensionless data.
        # @todo: cleaner unit division syntax
        return Quantity(left_object / self.data, self.units**(-1))

    def __pow__(self, power):
        """
        Raise this quantity to some power.

        Parameters
        ----------
        power : float or dimensionless Quantity object
            The pow value.

        """
        if isinstance(power, Quantity):
            if power.units.is_dimensionless():
                return Quantity(self.data**power.data, self.units**power.data)
            else:
                raise Exception("The power argument must be dimensionless. (%s)**(%s) is ill-defined." % (self, power))

        return Quantity(self.data**power, self.units**power)

    ### less common operations
    def __abs__(self):
        return Quantity(abs(self.data), self.units)

    ### comparison operators
    # @todo: not sure if these behave as intended
    def __lt__(self, right_object):
        """ Test if this is less than the object on the right. """
        # Check that the other is a Quantity.
        if not isinstance(right_object, Quantity):
            raise Exception("You cannot compare a Quantity to a non-Quantity object. %s < %s is ill-defined." % (self, right_object))
        # Check that the dimensions are the same.
        if not self.units.same_dimensions_as(right_object.units):
            raise Exception("You cannot compare quantities of units %s and %s." % (self.units, right_object.units))

        if self.data < right_object.get_data_in(self.units):
            return True
        return False

    def __le__(self, right_object):
        """ Test if this is less than or equal to the object on the right. """
        # Check that the other is a Quantity.
        if not isinstance(right_object, Quantity):
            raise Exception("You cannot compare a Quantity to a non-Quantity object. %s <= %s is ill-defined." % (self, right_object))
        # Check that the dimensions are the same.
        if not self.units.same_dimensions_as(right_object.units):
            raise Exception("You cannot compare quantities of units %s and %s." % (self.units, right_object.units))

        if self.data <= right_object.get_data_in(self.units):
            return True
        return False

    def __eq__(self, right_object):
        """ Test if this is equal to the object on the right. """
        # Check that the other is a Quantity.
        if not isinstance(right_object, Quantity):
            raise Exception("You cannot compare a Quantity to a non-Quantity object. %s == %s is ill-defined." % (self, right_object))
        # Check that the dimensions are the same.
        if not self.units.same_dimensions_as(right_object.units):
            raise Exception("You cannot compare quantities of units %s and %s." % (self.units, right_object.units))

        if self.data == right_object.get_data_in(self.units):
            return True
        return False

    def __ne__(self, right_object):
        """ Test if this is not equal to the object on the right. """
        # Check that the other is a Quantity.
        if not isinstance(right_object, Quantity):
            raise Exception("You cannot compare a Quantity to a non-Quantity object. %s != %s is ill-defined." % (self, right_object))
        # Check that the dimensions are the same.
        if not self.units.same_dimensions_as(right_object.units):
            raise Exception("You cannot compare quantities of units %s and %s." % (self.units, right_object.units))

        if self.data != right_object.get_data_in(self.units):
            return True
        return False

    def __ge__(self, right_object):
        """
        Test if this is greater than or equal to the object on the right.

        """
        # Check that the other is a Quantity.
        if not isinstance(right_object, Quantity):
            raise Exception("You cannot compare a Quantity to a non-Quantity object. %s >= %s is ill-defined." % (self, right_object))
        # Check that the dimensions are the same.
        if not self.units.same_dimensions_as(right_object.units):
            raise Exception("You cannot compare quantities of units %s and %s." % (self.units, right_object.units))

        if self.data >= right_object.get_data_in(self.units):
            return True
        return False

    def __gt__(self, right_object):
        """ Test if this is greater than the object on the right. """
        # Check that the other is a Quantity.
        if not isinstance(right_object, Quantity):
            raise Exception("You cannot compare a Quantity to a non-Quantity object. %s > %s is ill-defined." % (self, right_object))
        # Check that the dimensions are the same.
        if not self.units.same_dimensions_as(right_object.units):
            raise Exception("You cannot compare quantities of units %s and %s." % (self.units, right_object.units))

        if self.data > right_object.get_data_in(self.units):
            return True
        return False
