import unittest
from datetime import date
from models import (
    Person, Employee, Student, Professor, Dean, Secretary,
    StudyGroup, Department, Faculty, Subject, Lesson, Schedule, Grade, GradeBook,
    ExpulsionOrder, Curriculum, Petition
)
from exceptions import (
    ScheduleConflictException, InvalidGradeException, StudentNotFoundException,
    InsufficientCreditsException, InvalidGroupTransferException, DormitoryFullException,
    ScholarshipDeniedException, ExpulsionRulesViolationException, InvalidDocumentFormatException,
    UnauthorizedAccessException, RetakeLimitExceededException
)


class TestUniversityStructure(unittest.TestCase):
    def setUp(self):
        self.student = Student(1, "Иван", "Иванов", date(2005, 1, 1), "RB-1")
        self.group = StudyGroup("101", 1, "Информатика")
        self.prof = Professor(2, "Петр", "Петров", date(1980, 5, 5), "Доцент", 2000.0, "К.Т.Н.")
        self.dept = Department("Кафедра ИТ", "101a")

    def test_person_methods(self):
        self.assertEqual(self.student.get_full_name(), "Иван Иванов")
        self.assertTrue(isinstance(self.student.calculate_age(), int))

    def test_student_enrollment(self):
        self.group.enroll_student(self.student)
        self.assertEqual(len(self.group.students), 1)
        self.assertEqual(self.student.study_group, self.group)

    def test_employee_bonus_and_salary_fund(self):
        self.dept.hire_employee(self.prof)
        self.prof.apply_bonus(10)  # +10%
        self.assertEqual(self.prof.salary, 2200.0)
        self.assertEqual(self.dept.get_total_salary_fund(), 2200.0)

        self.prof.terminate_employment()
        self.assertEqual(self.dept.get_total_salary_fund(), 0.0)

    def test_professor_methods(self):
        self.prof.publish_paper()
        self.assertEqual(self.prof.publications_count, 1)
        subject = Subject("Тест", 10, False)
        self.prof.assign_subject(subject)
        self.assertTrue(self.prof.conduct_exam(self.group, subject))

    def test_group_methods(self):
        self.group.enroll_student(self.student)
        self.group.elect_head_student(self.student)
        self.assertEqual(self.group.head_student, self.student)
        self.group.advance_course()
        self.assertEqual(self.group.course_year, 2)

    def test_group_split(self):
        for i in range(4):
            self.group.enroll_student(Student(10 + i, f"Студент{i}", "Тест", date(2005, 1, 1), f"R-{i}"))
        self.group.split_into_subgroups()
        self.assertEqual(len(self.group.subgroups), 2)
        self.assertEqual(self.group.subgroups[0].get_student_count(), 2)
        self.group.subgroups[0].assign_teacher(self.prof)
        self.assertEqual(self.group.subgroups[0].practice_teacher, self.prof)

    def test_department_and_faculty(self):
        faculty = Faculty("ФКН", "1")
        faculty.add_department(self.dept)
        self.dept.hire_employee(self.prof)
        self.dept.appoint_head(self.prof)
        self.assertEqual(self.dept.head_of_department, self.prof)
        self.assertEqual(faculty.get_faculty_staff_count(), 1)


class TestAcademicProcess(unittest.TestCase):
    def setUp(self):
        self.student = Student(1, "Иван", "Иванов", date(2005, 1, 1), "RB-1")
        self.gb = GradeBook(self.student, "GB-1")
        self.student.issue_grade_book(self.gb)
        self.subject = Subject("Математика", 100, True)
        self.prof = Professor(2, "Петр", "Петров", date(1980, 1, 1), "Доцент", 2000, "К.Т.Н.")
        self.group = StudyGroup("101", 1, "ИТ")
        self.schedule = Schedule(self.group, 1)

    def test_grade_recording_and_average(self):
        self.assertEqual(self.gb.calculate_average_score(), 0.0)
        self.gb.record_grade(Grade(self.subject, 8, date.today(), self.prof))
        self.gb.record_grade(Grade(self.subject, 9, date.today(), self.prof))
        self.assertEqual(self.gb.calculate_average_score(), 8.5)
        self.assertFalse(self.gb.has_debts())

    def test_curriculum_and_subject(self):
        self.subject.update_hours(20)
        self.assertEqual(self.subject.total_hours, 120)
        self.assertEqual(self.subject.get_control_type(), "Экзамен")
        curr = Curriculum("ИТ", 1)
        curr.add_subject(self.subject)
        self.assertEqual(curr.calculate_total_workload(), 120)

    def test_lesson_methods(self):
        lesson = Lesson(self.subject, self.prof, "Ауд.1", "Вторник", 1)
        self.schedule.add_lesson(lesson)
        self.assertEqual(len(self.schedule.get_lessons_for_day("Вторник")), 1)

        lesson.cancel_lesson()
        self.assertTrue(lesson.is_cancelled)
        self.assertEqual(len(self.schedule.get_lessons_for_day("Вторник")), 0)

        lesson.assign_substitute(Professor(99, "А", "Б", date(1990, 1, 1), "Асс", 100, ""))
        self.assertFalse(lesson.is_cancelled)

    def test_invalid_grade_exception(self):
        with self.assertRaises(InvalidGradeException):
            self.gb.record_grade(Grade(self.subject, 15, date.today(), self.prof))

    def test_schedule_conflict_exception(self):
        lesson1 = Lesson(self.subject, self.prof, "Ауд.1", "Понедельник", 1)
        lesson2 = Lesson(self.subject, self.prof, "Ауд.2", "Понедельник", 1)
        self.schedule.add_lesson(lesson1)
        with self.assertRaises(ScheduleConflictException):
            self.schedule.add_lesson(lesson2)


class TestAdministrativeProcess(unittest.TestCase):
    def setUp(self):
        self.student = Student(1, "Иван", "Иванов", date(2005, 1, 1), "RB-1")
        self.dean = Dean(2, "Декан", "Деканов", date(1970, 1, 1), 3000)
        self.sec = Secretary(3, "Секретарь", "Секретарева", date(1990, 1, 1), 1000)

    def test_expulsion_order(self):
        order = self.dean.approve_expulsion(self.student, "Академическая неуспеваемость")
        self.assertTrue(order.is_signed)
        self.assertEqual(self.student.status, "Enrolled")

        # Проверка повторного подписания
        self.assertFalse(self.dean.sign_document(order))

        success = order.execute_order()
        self.assertTrue(success)
        self.assertEqual(self.student.status, "Expelled: Академическая неуспеваемость")
        self.assertIsNone(self.student.study_group)
        self.assertFalse(order.execute_order())  # Повторное выполнение

    def test_secretary_and_petition(self):
        order = self.sec.draft_order("Тест", "Текст")
        self.assertEqual(len(self.sec.processed_documents), 1)
        self.sec.register_document(order)  # Дубликат не должен добавиться
        self.assertEqual(len(self.sec.processed_documents), 1)

        order.assign_executor(self.sec)
        self.assertEqual(order.executor, self.sec)
        self.assertTrue("Черновик" in order.get_summary())

        pet = Petition("P1", date.today(), self.student, "Прошу")
        pet.approve(self.dean)
        self.assertEqual(pet.status, "Одобрено")
        self.assertTrue(pet.is_signed)

        pet2 = Petition("P2", date.today(), self.student, "Прошу")
        pet2.reject("Нет")
        self.assertEqual(pet2.status, "Отклонено: Нет")


class TestExceptionsInitialization(unittest.TestCase):
    def test_all_custom_exceptions(self):
        # Проверяем, что все исключения корректно инициализируются
        exceptions = [
            StudentNotFoundException(1),
            InsufficientCreditsException("Иван"),
            InvalidGroupTransferException("Иван", "102"),
            DormitoryFullException("4"),
            ScholarshipDeniedException("Иван", "Долги"),
            ExpulsionRulesViolationException("Иван"),
            InvalidDocumentFormatException("DOC-1"),
            UnauthorizedAccessException("Студент", "Удаление"),
            RetakeLimitExceededException("Иван", "Математика")
        ]
        for exc in exceptions:
            self.assertTrue(isinstance(exc, Exception))


if __name__ == '__main__':
    unittest.main()