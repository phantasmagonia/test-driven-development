import unittest

from cart import cart_total


class CartTotalTests(unittest.TestCase):
    def test_sums_price_times_quantity(self):
        items = [{"price": 2.5, "quantity": 2}, {"price": 1.0, "quantity": 3}]
        self.assertEqual(cart_total(items), 8.0)

    def test_applies_percentage_discount(self):
        self.assertEqual(cart_total([{"price": 10.0, "quantity": 1}], discount_percent=25), 7.5)


if __name__ == "__main__":
    unittest.main()
