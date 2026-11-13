import unittest
from datetime import date
from models import GradeBook, Student, Subject, Professor, Grade


class TestGradeBook(unittest.TestCase):
    def test_init(self):
        student = Student(1, "Иван", "Иванов", date(2005, 1, 1))

        # Убрали лишний аргумент "SUB-1", теперь ровно 4 аргумента с self
        subject = Subject("Математика", 100, True)
        prof = Professor(
            2, "Петр", "Петров", date(1980, 1, 1),
            "Доцент", 2000, "К.Т.Н."
        )

        gb = GradeBook("GB-1", student)
        grade = Grade(subject, 8, date.today(), prof)

        self.assertIsNotNone(gb)
        self.assertIsNotNone(grade)