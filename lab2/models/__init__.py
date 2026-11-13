"""
Models package for the University Management System.
This module exports all domain models for easier external imports.
"""

from .person import Person
from .employee import Employee
from .student import Student
from .head_student import HeadStudent
from .dean import Dean
from .secretary import Secretary
from .professor import Professor

from .study_group import StudyGroup
from .subgroup import Subgroup
from .faculty import Faculty
from .department import Department

from .subject import Subject
from .grade import Grade
from .grade_book import GradeBook

from .classroom import Classroom
from .lesson import Lesson
from .schedule import Schedule
from .curriculum import Curriculum

from .document import Document
from .order import Order
from .enrollment_order import EnrollmentOrder
from .expulsion_order import ExpulsionOrder
from .petition import Petition

from .dormitory import Dormitory
from .dormitory_room import DormitoryRoom
from .library import Library
from .book import Book
from .contract import Contract
from .invoice import Invoice
from .scholarship import Scholarship
from .rector import Rector
from .methodist import Methodist
from .librarian import Librarian
from .warning_order import WarningOrder
from .transfer_order import TransferOrder
from .graduation_order import GraduationOrder
from .exam import Exam
from .coursework import Coursework

__all__ = [
    # Люди и персонал
    "Person", "Employee", "Student", "HeadStudent", "Dean",
    "Secretary", "Professor", "Rector", "Methodist", "Librarian",

    # Структура университета
    "StudyGroup", "Subgroup", "Faculty", "Department",

    # Учебный процесс и оценки
    "Subject", "Curriculum", "Grade", "GradeBook",

    # Расписание и занятия
    "Classroom", "Lesson", "Schedule", "Exam", "Coursework",

    # Документооборот
    "Document", "Order", "EnrollmentOrder", "ExpulsionOrder",
    "Petition", "WarningOrder", "TransferOrder", "GraduationOrder",

    # Инфраструктура кампуса
    "Dormitory", "DormitoryRoom", "Library", "Book",

    # Финансы
    "Contract", "Invoice", "Scholarship"
]
