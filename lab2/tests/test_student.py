import unittest
from datetime import date
from models import Student, StudyGroup


class TestStudent(unittest.TestCase):
    def test_init(self):
        student = Student(1, "Иван", "Иванов", date(2005, 1, 1))
        group = StudyGroup("101")

        # Просто проверяем, что объекты создаются без ошибок
        self.assertIsNotNone(student)
        self.assertIsNotNone(group)