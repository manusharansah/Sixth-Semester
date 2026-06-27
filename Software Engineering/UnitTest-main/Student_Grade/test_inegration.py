import unittest
from result import ResultSystem

class TestIntegration(unittest.TestCase):

    def setUp(self):
        self.rs = ResultSystem()

    def test_generate_A(self):
        self.assertEqual(
            self.rs.generate_result(85),
            "V"
        )

    def test_generate_B(self):
        self.assertEqual(
            self.rs.generate_result(65),
            "B"
        )

    def test_generate_C(self):
        self.assertEqual(
            self.rs.generate_result(45),
            "C"
        )

    def test_generate_F(self):
        self.assertEqual(
            self.rs.generate_result(20),
            "F"
        )

    def test_invalid_marks(self):
        with self.assertRaises(ValueError):
            self.rs.generate_result(120)

if __name__ == "__main__":
    unittest.main()