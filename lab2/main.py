from datetime import date
from models import (
    Faculty, Department, Dean, Professor, Student, StudyGroup,
    Subject, Schedule, Lesson, GradeBook, Grade
)
from exceptions import DeaneryException, InvalidGradeException, ScheduleConflictException


def setup_test_data():
    """Создает базовые объекты для демонстрации работы системы."""
    faculty = Faculty("Факультет компьютерных систем", "Корпус 4")
    dean = Dean(1, "Иван", "Иванов", date(1975, 5, 20), 2500.0)
    dean.assign_faculty(faculty)

    cs_dept = Department("Кафедра информатики", "401a")
    faculty.add_department(cs_dept)

    prof = Professor(2, "Петр", "Петров", date(1980, 10, 15), "Доцент", 1800.0, "Кандидат наук")
    cs_dept.hire_employee(prof)

    group = StudyGroup("123456", 2, "Программная инженерия")
    student1 = Student(101, "Алексей", "Смирнов", date(2004, 3, 12), "RB-001")
    student2 = Student(102, "Мария", "Кузнецова", date(2005, 7, 21), "RB-002")

    group.enroll_student(student1)
    group.enroll_student(student2)
    student1.issue_grade_book(GradeBook(student1, "GB-001"))
    student2.issue_grade_book(GradeBook(student2, "GB-002"))

    subject = Subject("Основы алгоритмов", 120, True)
    prof.assign_subject(subject)

    schedule = Schedule(group, 3)

    return dean, group, prof, subject, schedule


def main():
    dean, group, prof, subject, schedule = setup_test_data()

    while True:
        print("\n=== Система управления Деканатом ===")
        print("1. Показать список студентов группы")
        print("2. Добавить занятие в расписание")
        print("3. Выставить оценку студенту")
        print("4. Инициировать отчисление студенту (Приказ декана)")
        print("0. Выход")

        choice = input("Выберите действие: ")

        try:
            if choice == "1":
                print(f"\nГруппа {group.group_number}:")
                for s in group.students:
                    print(f"- {s.get_full_name()} [{s.status}]")

            elif choice == "2":
                day = input("Введите день недели (например, Понедельник): ")
                slot = int(input("Введите номер пары (1-5): "))
                lesson = Lesson(subject, prof, "Ауд. 412", day, slot)
                # Если будет конфликт, вылетит ScheduleConflictException
                schedule.add_lesson(lesson)
                print("Занятие успешно добавлено в расписание!")

            elif choice == "3":
                student_id = int(input("Введите ID студента (например, 101): "))
                target_student = next((s for s in group.students if s.person_id == student_id), None)
                if not target_student:
                    print("Студент не найден.")
                    continue

                mark = int(input(f"Введите оценку по 10-балльной шкале для {target_student.get_full_name()}: "))
                grade = Grade(subject, mark, date.today(), prof)
                # Если оценка вне диапазона 1-10, вылетит InvalidGradeException
                target_student.grade_book.record_grade(grade)
                print(
                    f"Оценка выставлена. Средний балл студента: {target_student.grade_book.calculate_average_score():.2f}")

            elif choice == "4":
                student_id = int(input("Введите ID студента для отчисления (например, 101): "))
                target_student = next((s for s in group.students if s.person_id == student_id), None)
                if not target_student:
                    print("Студент не найден.")
                    continue

                reason = input("Укажите причину отчисления: ")
                order = dean.approve_expulsion(target_student, reason)
                order.execute_order()
                print(f"Приказ №{order.doc_number} подписан деканом. Студент отчислен.")

            elif choice == "0":
                print("Выход из системы.")
                break
            else:
                print("Неизвестная команда.")

        except ValueError:
            print("Ошибка: пожалуйста, вводите числовые значения там, где это требуется.")
        except DeaneryException as e:
            # Перехват наших кастомных доменных исключений
            print(f"\n[ДОМЕННАЯ ОШИБКА]: {e}")


if __name__ == "__main__":
    main()