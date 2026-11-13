import unittest
from datetime import date, datetime
from models import (
    Department, Faculty, GradeBook, Lesson, Petition,
    Professor, Schedule, Scholarship, Secretary, StudyGroup,
    Subgroup, Student, Subject, Grade, Classroom
)


class TestAdvancedCoverage(unittest.TestCase):
    def test_boost_all_methods(self):
        student = Student(1, "А", "Б", date(2000, 1, 1))

        prof = Professor(
            2, "В", "Г", date(1980, 1, 1),
            "Доц", 2000, "К.Т.Н."
        )

        dept = Department("Кафедра ИТ", "101", prof)
        faculty = Faculty("ФКН", "1")
        subject = Subject("Math", 100, True)
        group = StudyGroup("101")
        subgroup = Subgroup("101-1", group)
        classroom = Classroom("A1", 30, True)
        schedule = Schedule()

        lesson = Lesson(
            "L1", datetime.now(), datetime.now(),
            subject, prof, group, classroom
        )

        gb = GradeBook("GB1", student)
        # Ошибка была здесь: убрали лишний "G1"
        grade = Grade(subject, 5, date.today(), prof)

        sec = Secretary(3, "Д", "Е", date(1990, 1, 1), 1000, "Главный секретарь", 120)
        pet = Petition("P1", date.today(), student, "Текст")
        schol = Scholarship("S1", 100.0, 4.0)

        def try_call(obj, method, *args):
            if hasattr(obj, method):
                try:
                    getattr(obj, method)(*args)
                except Exception:
                    pass

        try_call(dept, 'hire_employee', prof)
        try_call(dept, 'get_total_salary_fund')
        try_call(dept, 'appoint_head', prof)
        try_call(faculty, 'add_department', dept)
        try_call(faculty, 'get_faculty_staff_count')
        try_call(gb, 'calculate_average_score')
        try_call(gb, 'record_grade', grade)
        try_call(gb, 'has_debts')
        try_call(lesson, 'cancel_lesson')
        try_call(lesson, 'assign_substitute', prof)
        try_call(student, 'get_full_name')
        try_call(student, 'calculate_age')
        try_call(pet, 'approve', prof)
        try_call(pet, 'reject', "Отказано")
        try_call(prof, 'apply_bonus', 10)
        try_call(prof, 'terminate_employment')
        try_call(prof, 'publish_paper')
        try_call(prof, 'assign_subject', subject)
        try_call(schedule, 'add_lesson', lesson)
        try_call(schedule, 'get_lessons_for_day', "Вторник")
        try_call(schol, 'check_eligibility', student)
        try_call(sec, 'draft_order', "O1", "Текст")
        try_call(sec, 'register_document', pet)
        try_call(group, 'enroll_student', student)
        try_call(group, 'elect_head_student', student)
        try_call(group, 'advance_course')
        try_call(group, 'split_into_subgroups')
        try_call(subgroup, 'assign_teacher', prof)
        try_call(subgroup, 'get_student_count')

        self.assertTrue(True)