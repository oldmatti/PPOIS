import unittest
from datetime import date
from models import (
    Rector, Methodist, Librarian, Coursework,
    Professor, Student, Library
)

class TestStaffAndAcademics(unittest.TestCase):
    def test_staff(self):
        rector = Rector(
            1, "Алексей", "Петров", date(1970, 1, 1),
            5000, "Ректор", "Д.Т.Н."
        )
        self.assertEqual(rector.degree, "Д.Т.Н.")

        methodist = Methodist(
            2, "Анна", "Иванова", date(1980, 1, 1),
            2000, "Методист"
        )
        self.assertEqual(methodist.position, "Методист")

        lib = Library("Научная")
        librarian = Librarian(
            3, "Мария", "Смирнова", date(1990, 1, 1),
            1500, "Библиотекарь", lib
        )
        self.assertEqual(librarian.library.name, "Научная")

    def test_academics(self):
        student = Student(1, "Иван", "Иванов", date(2005, 1, 1))
        prof = Professor(
            2, "Петр", "Петров", date(1980, 5, 5),
            "Доцент", 2000.0, "К.Т.Н."
        )
        cw = Coursework("Нейросети", student, prof)
        self.assertEqual(cw.title, "Нейросети")