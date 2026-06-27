class Grade:

    def calculate_grade(self, marks):

        if marks < 0 or marks > 100:
            raise ValueError("Marks must be between 0 and 100")

        if marks >= 80:
            return "A"
        elif marks >= 60:
            return "B"
        elif marks >= 40:
            return "C"
        else:
            return "F"