class Quantity:
    def __init__(self, amount, unit):
        self.amount = amount
        self.unit = unit

    def times(self, factor):
        return Quantity(self.amount * factor, self.unit)

    def plus(self, addend):
        return Sum(self, addend)

    def reduce(self, converter, unit):
        if self.unit == unit:
            return self
        converted = self.amount * converter.rate(self.unit, unit)
        return Quantity(converted, unit)

    def __eq__(self, other):
        if not isinstance(other, Quantity):
            return NotImplemented
        return self.amount == other.amount and self.unit == other.unit

    def __repr__(self):
        return f"Quantity({self.amount} {self.unit})"


class Sum:
    def __init__(self, augend, addend):
        self.augend = augend
        self.addend = addend

    def reduce(self, converter, unit):
        a = self.augend.reduce(converter, unit).amount
        b = self.addend.reduce(converter, unit).amount
        return Quantity(a + b, unit)

    def times(self, factor):
        return Sum(self.augend.times(factor), self.addend.times(factor))


class Converter:
    def __init__(self):
        self._rates = {}

    def add_rate(self, from_unit, to_unit, multiplier):
        self._rates[(from_unit, to_unit)] = multiplier

    def rate(self, from_unit, to_unit):
        return self._rates[(from_unit, to_unit)]

    def reduce(self, source, unit):
        return source.reduce(self, unit)


def grams(amount):
    return Quantity(amount, "g")


def ounces(amount):
    return Quantity(amount, "oz")
