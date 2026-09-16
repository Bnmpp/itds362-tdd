# Test list (Part A — Kitchen Quantity)
#
# [x] 200 g × 3 = 600 g
# [x] times() does not change the original quantity
# [x] two quantities with the same amount and unit are equal
# [x] grams and ounces with the same number are not equal
# [x] a Quantity does not equal a plain number
# [x] 200 g + 300 g reduces to 500 g
# [x] 200 g + 1 oz, reduced to grams with a conversion rate
# [x] scaling a mixed-unit sum with times()
#
# Deferred:
# [ ] __hash__ — defining __eq__ without it makes Quantity unhashable

from kitchen import Quantity, Converter, grams, ounces


def test_multiplication():
    flour = grams(200)
    assert flour.times(3) == grams(600)


def test_times_does_not_mutate_original():
    flour = grams(200)
    flour.times(3)
    assert flour == grams(200)


def test_equal_quantities():
    assert grams(200) == grams(200)
    assert grams(200) != grams(300)


def test_different_units_are_not_equal():
    assert grams(1) != ounces(1)


def test_quantity_does_not_equal_plain_number():
    assert grams(200) != 200


def test_simple_addition():
    result = grams(200).plus(grams(300))
    converter = Converter()
    assert converter.reduce(result, "g") == grams(500)


def test_mixed_unit_addition():
    converter = Converter()
    converter.add_rate("oz", "g", 28)
    result = grams(200).plus(ounces(1))
    assert converter.reduce(result, "g") == grams(228)


def test_scaling_a_mixed_sum():
    converter = Converter()
    converter.add_rate("oz", "g", 28)
    result = grams(200).plus(ounces(1)).times(2)
    assert converter.reduce(result, "g") == grams(456)
