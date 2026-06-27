import unittest
from product import Product
from billing import Billing

class TestSystem(unittest.TestCase):

    def setUp(self):
        self.billing = Billing()

    def test_complete_purchase(self):

        product = Product(
            "Mobile",
            20000
        )

        amount = self.billing.generate_bill(
            product,
            3
        )

        self.assertEqual(amount, 60000)

    def test_single_purchase(self):

        product = Product(
            "Headphone",
            5000
        )

        amount = self.billing.generate_bill(
            product,
            1
        )

        self.assertEqual(amount, 5000)

    def test_invalid_purchase(self):

        product = Product(
            "Laptop",
            50000
        )

        with self.assertRaises(ValueError):
            self.billing.generate_bill(
                product,
                -1
            )

if __name__ == "__main__":
    unittest.main()