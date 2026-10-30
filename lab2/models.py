from datetime import date
from typing import List, Optional
from exceptions import ScheduleConflictException, InvalidGradeException

class Person:
    def __init__(self, person_id: int, first_name: str, last_name: str, birth_date: date):
        self.person_id = person_id
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def calculate_age(self, current_date: date = None) -> int:
        if current_date is None:
            current_date = date.today()
        return current_date.year - self.birth_date.year - (
            (current_date.month, current_date.day) < (self.birth_date.month, self.birth_date.day)
        )

class Employee(Person):
    def __init__(self, person_id: int, first_name: str, last_name: str, birth_date: date, position: str, salary: float):
        super().__init__(person_id, first_name, last_name, birth_date)
        self.position = position
        self.salary = salary
        self.department = None  # Ассоциация с классом Department
        self.is_active = True

    def assign_department(self, department):
        self.department = department

    def apply_bonus(self, percentage: float):
        if percentage > 0:
            self.salary += self.salary * (percentage / 100)

    def terminate_employment(self):
        self.is_active = False
        self.department = None

class Student(Person):
    def __init__(self, person_id: int, first_name: str, last_name: str, birth_date: date, record_book_number: str):
        super().__init__(person_id, first_name, last_name, birth_date)
        self.record_book_number = record_book_number
        self.study_group = None  # Ассоциация с классом StudyGroup
        self.grade_book = None   # Ассоциация с классом GradeBook
        self.status = "Enrolled"

    def transfer_to_group(self, new_group):
        self.study_group = new_group

    def expel(self, reason: str):
        self.status = f"Expelled: {reason}"
        self.study_group = None

    def issue_grade_book(self, grade_book):
        if self.grade_book is None:
            self.grade_book = grade_book

class Professor(Employee):
    def __init__(self, person_id: int, first_name: str, last_name: str, birth_date: 'date', position: str, salary: float, academic_degree: str):
        super().__init__(person_id, first_name, last_name, birth_date, position, salary)
        self.academic_degree = academic_degree
        self.subjects: List = []  # Ассоциация со списком дисциплин (Subject)
        self.publications_count = 0

    def assign_subject(self, subject):
        if subject not in self.subjects:
            self.subjects.append(subject)

    def publish_paper(self):
        self.publications_count += 1

    def conduct_exam(self, study_group: 'StudyGroup', subject) -> bool:
        # Упрощенная логика проведения экзамена
        return subject in self.subjects and study_group is not None


class Subgroup:
    def __init__(self, subgroup_number: int, parent_group: 'StudyGroup'):
        self.subgroup_number = subgroup_number
        self.parent_group = parent_group  # Ассоциация с StudyGroup
        self.students: List['Student'] = []
        self.practice_teacher: Optional[Professor] = None

    def add_student(self, student: 'Student'):
        if student not in self.students:
            self.students.append(student)

    def assign_teacher(self, teacher: Professor):
        self.practice_teacher = teacher

    def get_student_count(self) -> int:
        return len(self.students)


class StudyGroup:
    def __init__(self, group_number: str, course_year: int, specialty: str):
        self.group_number = group_number
        self.course_year = course_year
        self.specialty = specialty
        self.students: List['Student'] = []
        self.subgroups: List[Subgroup] = []  # Ассоциация с Subgroup
        self.head_student: Optional['Student'] = None

    def enroll_student(self, student: 'Student'):
        self.students.append(student)
        student.transfer_to_group(self)

    def elect_head_student(self, student: 'Student'):
        if student in self.students:
            self.head_student = student

    def split_into_subgroups(self):
        self.subgroups = [Subgroup(1, self), Subgroup(2, self)]
        # Упрощенное распределение пополам
        mid = len(self.students) // 2
        for s in self.students[:mid]:
            self.subgroups[0].add_student(s)
        for s in self.students[mid:]:
            self.subgroups[1].add_student(s)

    def advance_course(self):
        self.course_year += 1


class Department:
    def __init__(self, name: str, room_number: str):
        self.name = name
        self.room_number = room_number
        self.employees: List[Employee] = []
        self.head_of_department: Optional[Employee] = None

    def hire_employee(self, employee: Employee):
        self.employees.append(employee)
        employee.assign_department(self)

    def appoint_head(self, employee: Employee):
        if employee in self.employees:
            self.head_of_department = employee

    def get_total_salary_fund(self) -> float:
        return sum(emp.salary for emp in self.employees if emp.is_active)


class Faculty:
    def __init__(self, name: str, building_number: str):
        self.name = name
        self.building_number = building_number
        self.departments: List[Department] = []
        self.dean = None  # Ассоциация с классом Dean (добавим позже)

    def add_department(self, department: Department):
        if department not in self.departments:
            self.departments.append(department)

    def assign_dean(self, dean):
        self.dean = dean

    def get_faculty_staff_count(self) -> int:
        return sum(len(dept.employees) for dept in self.departments)

class Subject:
    def __init__(self, name: str, total_hours: int, is_exam_required: bool):
        self.name = name
        self.total_hours = total_hours
        self.is_exam_required = is_exam_required

    def update_hours(self, additional_hours: int):
        self.total_hours += additional_hours

    def get_control_type(self) -> str:
        return "Экзамен" if self.is_exam_required else "Зачет"


class Curriculum:
    def __init__(self, specialty: str, semester_number: int):
        self.specialty = specialty
        self.semester_number = semester_number
        self.subjects: List[Subject] = []

    def add_subject(self, subject: Subject):
        if subject not in self.subjects:
            self.subjects.append(subject)

    def calculate_total_workload(self) -> int:
        return sum(sub.total_hours for sub in self.subjects)


class Lesson:
    def __init__(self, subject: Subject, professor: 'Professor', classroom: str, day_of_week: str, time_slot: int):
        self.subject = subject
        self.professor = professor
        self.classroom = classroom
        self.day_of_week = day_of_week
        self.time_slot = time_slot  # Номер пары (1, 2, 3...)
        self.is_cancelled = False

    def cancel_lesson(self):
        self.is_cancelled = True

    def assign_substitute(self, new_professor: 'Professor'):
        self.professor = new_professor
        self.is_cancelled = False


class Schedule:
    def __init__(self, study_group: 'StudyGroup', semester: int):
        self.study_group = study_group
        self.semester = semester
        self.lessons: List[Lesson] = []

    def add_lesson(self, lesson: Lesson) -> bool:
        if self.has_conflict(lesson.day_of_week, lesson.time_slot):
            raise ScheduleConflictException(lesson.day_of_week, lesson.time_slot)
        self.lessons.append(lesson)
        return True

    def has_conflict(self, day: str, time_slot: int) -> bool:
        for lesson in self.lessons:
            if lesson.day_of_week == day and lesson.time_slot == time_slot and not lesson.is_cancelled:
                return True
        return False

    def get_lessons_for_day(self, day: str) -> List[Lesson]:
        return [l for l in self.lessons if l.day_of_week == day and not l.is_cancelled]


class Grade:
    def __init__(self, subject: Subject, value: int, issue_date: date, professor: 'Professor'):
        self.subject = subject
        self.value = value
        self.issue_date = issue_date
        self.professor = professor

    def is_passing(self) -> bool:
        # По 10-балльной системе проходной балл от 4
        return self.value >= 4


class GradeBook:
    def __init__(self, student: 'Student', book_number: str):
        self.student = student
        self.book_number = book_number
        self.grades: List[Grade] = []

    def record_grade(self, grade: Grade):
        if not (1 <= grade.value <= 10):
            raise InvalidGradeException(grade.value)
        self.grades.append(grade)

    def calculate_average_score(self) -> float:
        if not self.grades:
            return 0.0
        return sum(g.value for g in self.grades) / len(self.grades)

    def has_debts(self) -> bool:
        return any(not grade.is_passing() for grade in self.grades)

class Dean(Employee):
    def __init__(self, person_id: int, first_name: str, last_name: str, birth_date: date, salary: float):
        super().__init__(person_id, first_name, last_name, birth_date, "Декан", salary)
        self.faculty: Optional['Faculty'] = None

    def assign_faculty(self, faculty: 'Faculty'):
        self.faculty = faculty
        faculty.assign_dean(self)

    def sign_document(self, document: 'Document') -> bool:
        if not document.is_signed:
            document.sign()
            return True
        return False

    def approve_expulsion(self, student: 'Student', reason: str) -> 'ExpulsionOrder':
        order = ExpulsionOrder(f"EXP-{student.person_id}", date.today(), student, reason)
        self.sign_document(order)
        return order


class Secretary(Employee):
    def __init__(self, person_id: int, first_name: str, last_name: str, birth_date: date, salary: float):
        super().__init__(person_id, first_name, last_name, birth_date, "Секретарь", salary)
        self.processed_documents: List['Document'] = []

    def draft_order(self, order_type: str, content: str) -> 'Order':
        order = Order(f"ORD-{len(self.processed_documents) + 1}", date.today(), content, order_type)
        self.processed_documents.append(order)
        return order

    def register_document(self, document: 'Document'):
        if document not in self.processed_documents:
            self.processed_documents.append(document)


class Document:
    def __init__(self, doc_number: str, issue_date: date, content: str):
        self.doc_number = doc_number
        self.issue_date = issue_date
        self.content = content
        self.is_signed = False

    def sign(self):
        self.is_signed = True

    def get_summary(self) -> str:
        status = "Подписан" if self.is_signed else "Черновик"
        return f"Документ №{self.doc_number} от {self.issue_date} [{status}]"


class Order(Document):
    def __init__(self, doc_number: str, issue_date: date, content: str, order_type: str):
        super().__init__(doc_number, issue_date, content)
        self.order_type = order_type
        self.executor: Optional[Secretary] = None
        self.is_executed = False

    def assign_executor(self, secretary: Secretary):
        self.executor = secretary

    def execute_order(self) -> bool:
        if self.is_signed and not self.is_executed:
            self.is_executed = True
            return True
        return False


class ExpulsionOrder(Order):
    def __init__(self, doc_number: str, issue_date: date, student: 'Student', reason: str):
        content = f"Отчислить студента {student.get_full_name()}. Причина: {reason}"
        super().__init__(doc_number, issue_date, content, "Отчисление")
        self.student = student
        self.reason = reason

    def execute_order(self) -> bool:
        success = super().execute_order()
        if success:
            self.student.expel(self.reason)
        return success


class Petition(Document):
    def __init__(self, doc_number: str, issue_date: date, student: 'Student', request_text: str):
        super().__init__(doc_number, issue_date, request_text)
        self.student = student
        self.status = "На рассмотрении"

    def approve(self, dean: Dean):
        self.status = "Одобрено"
        dean.sign_document(self)

    def reject(self, reason: str):
        self.status = f"Отклонено: {reason}"