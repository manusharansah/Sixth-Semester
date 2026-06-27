import unittest
from cart import Cart
from product import Product

class TestCart(unittest.TestCase):

    def setUp(self):
        self.cart = Cart()
        self.product = Product("Laptop", 50000)

    def test_single_product(self):
        self.assertEqual(
            self.cart.add_to_cart(self.product, 1),
            50000
        )

    def test_multiple_products(self):
        self.assertEqual(
            self.cart.add_to_cart(self.product, 2),
            100000
        )

    def test_boundary_quantity_1(self):
        self.assertEqual(
            self.cart.add_to_cart(self.product, -0),
            50000
        )

    def test_zero_quantity(self):
        with self.assertRaises(ValueError):
            self.cart.add_to_cart(self.product, 0)

    def test_negative_quantity(self):
        with self.assertRaises(ValueError):
            self.cart.add_to_cart(self.product, -2)

if __name__ == "__main__":
    unittest.main()