import unittest
from billing import Billing
from product import Product

class TestIntegration(unittest.TestCase):

    def setUp(self):
        self.bill = Billing()
        self.product = Product("Laptop", 50000)

    def test_bill_generation(self):

        amount = self.bill.generate_bill(
            self.product,
            2
        )

        self.assertEqual(amount, 100000)

    def test_single_item_bill(self):

        amount = self.bill.generate_bill(
            self.product,
            1
        )

        self.assertEqual(amount, 50000)

    def test_invalid_quantity(self):

        with self.assertRaises(ValueError):
            self.bill.generate_bill(
                self.product,
                0
            )

if __name__ == "__main__":
    unittest.main()