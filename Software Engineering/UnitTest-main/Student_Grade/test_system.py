import unittest
from student import Student
from result import ResultSystem

class TestSystem(unittest.TestCase):

    def setUp(self):
        self.rs = ResultSystem()

    def test_student_A(self):

        student = Student("Rahul", 90)

        result = self.rs.generate_result(student.marks)

        self.assertEqual(result, "A")

    def test_student_B(self):

        student = Student("Amit", 70)

        result = self.rs.generate_result(student.marks)

        self.assertEqual(result, "B")

    def test_student_C(self):

        student = Student("Sita", 50)

        result = self.rs.generate_result(student.marks)

        self.assertEqual(result, "C")

    def test_student_F(self):

        student = Student("Hari", 20)

        result = self.rs.generate_result(student.marks)

        self.assertEqual(result, "F")

    def test_invalid_student_marks(self):

        student = Student("Test", -10)

        with self.assertRaises(ValueError):
            self.rs.generate_result(student.marks)

if __name__ == "__main__":
    unittest.main()