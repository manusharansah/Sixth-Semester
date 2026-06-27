from grade import Grade

class ResultSystem:

    def generate_result(self, marks):
        grade = Grade()
        return grade.calculate_grade(marks)