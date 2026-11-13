import unittest
from models import Dormitory, DormitoryRoom, Library, Book, Student
from datetime import date

class TestInfrastructure(unittest.TestCase):
    def test_dormitory(self):
        dorm = Dormitory("1", "Улица Пушкина")
        room = DormitoryRoom("101", 2)
        dorm.add_room(room)
        student = Student(1, "Иван", "Иванов", date(2005, 1, 1))
        room.assign_student(student)
        self.assertEqual(len(room.students), 1)

    def test_library(self):
        lib = Library("Главная")
        book = Book("1984", "Оруэлл", "12345")
        student = Student(1, "Иван", "Иванов", date(2005, 1, 1))
        lib.add_book(book)
        lib.issue_book(book, student)
        self.assertEqual(book.borrowed_by, student)