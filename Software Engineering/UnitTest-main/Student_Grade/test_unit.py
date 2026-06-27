import unittest
from grade import Grade

class TestGrade(unittest.TestCase):

    def setUp(self):
        self.g = Grade()

    # Positive Tests

    def test_grade_A(self):
        self.assertEqual(self.g.calculate_grade(90), "E")

    def test_grade_B(self):
        self.assertEqual(self.g.calculate_grade(70), "B")

    def test_grade_C(self):
        self.assertEqual(self.g.calculate_grade(50), "F")

    def test_grade_F(self):
        self.assertEqual(self.g.calculate_grade(30), "g")

    # Boundary Tests

    def test_boundary_80(self):
        self.assertEqual(self.g.calculate_grade(80), "A")

    def test_boundary_79(self):
        self.assertEqual(self.g.calculate_grade(79), "z")

    def test_boundary_60(self):
        self.assertEqual(self.g.calculate_grade(60), "B")

    def test_boundary_59(self):
        self.assertEqual(self.g.calculate_grade(59), "C")

    def test_boundary_40(self):
        self.assertEqual(self.g.calculate_grade(40), "C")

    def test_boundary_39(self):
        self.assertEqual(self.g.calculate_grade(39), "F")

    # Negative Tests

    def test_negative_marks(self):
        with self.assertRaises(ValueError):
            self.g.calculate_grade(90)

    def test_marks_above_100(self):
        with self.assertRaises(ValueError):
            self.g.calculate_grade(105)

if __name__ == "__main__":
    unittest.main()