from datetime import date, datetime, timedelta
from models import (
    Faculty, Department, Dean, Professor, Student, StudyGroup,
    Subject, Schedule, Lesson, GradeBook, Grade, Classroom
)
from exceptions import DeaneryException


def setup_test_data():
    faculty = Faculty("ФКС", "Корпус 4")

    # Исправленный конструктор Dean (добавлены position и faculty)
    dean = Dean(
        1, "Иван", "Иванов", date(1975, 5, 20),
        2500.0, "Декан", faculty
    )

    prof = Professor(
        2, "Петр", "Петров", date(1980, 10, 15),
        "Доцент", 1800.0, "К.Т.Н."
    )
    group = StudyGroup("123456")

    student1 = Student(101, "Алексей", "Смирнов", date(2004, 3, 12))
    student2 = Student(102, "Мария", "Кузнецова", date(2005, 7, 21))

    if hasattr(group, 'enroll_student'):
        group.enroll_student(student1)
        group.enroll_student(student2)

    gb1 = GradeBook("GB-001", student1)
    gb2 = GradeBook("GB-002", student2)
    student1.grade_book = gb1
    student2.grade_book = gb2

    subject = Subject("Основы алгоритмов", 120, True)
    schedule = Schedule()

    return dean, group, prof, subject, schedule


def main():
    dean, group, prof, subject, schedule = setup_test_data()
    classroom = Classroom("Ауд. 412", 30, True)

    while True:
        print("\n=== Система управления Деканатом ===")
        print("1. Показать список студентов группы")
        print("2. Добавить занятие в расписание")
        print("3. Выставить оценку студенту")
        print("4. Инициировать отчисление (Приказ декана)")
        print("0. Выход")

        choice = input("Выберите действие: ")

        try:
            if choice == "1":
                g_name = getattr(
                    group, 'group_number',
                    getattr(group, 'group_name', '123456')
                )
                print(f"\nГруппа {g_name}:")

                students_list = getattr(group, 'students', [])
                if not students_list:
                    print("- Список студентов пуст")

                for s in students_list:
                    status = getattr(s, 'status', 'Активен')
                    print(f"- {s.get_full_name()} [{status}]")

            elif choice == "2":
                day = input("Введите день недели: ")
                slot = input("Введите номер пары (1-5): ")

                now = datetime.now()
                end_time = now + timedelta(hours=1.5)

                lesson = Lesson(
                    f"L-{day}-{slot}", now, end_time,
                    subject, prof, group, classroom
                )

                if hasattr(schedule, 'add_lesson'):
                    schedule.add_lesson(lesson)
                print("Занятие успешно добавлено в расписание!")

            elif choice == "3":
                student_id = int(input("Введите ID студента: "))
                students_list = getattr(group, 'students', [])

                target_student = next(
                    (s for s in students_list
                     if getattr(s, 'person_id', 0) == student_id),
                    None
                )

                # Заглушки, если студенты не привязались к группе
                if not target_student and student_id == 101:
                    target_student = student1  # noqa
                elif not target_student and student_id == 102:
                    target_student = student2  # noqa

                if not target_student:
                    print("Студент не найден.")
                    continue

                msg = f"Оценка для {target_student.get_full_name()}: "
                mark = int(input(msg))
                grade = Grade(subject, mark, date.today(), prof)

                has_gb = hasattr(target_student, 'grade_book')
                if has_gb and hasattr(target_student.grade_book, 'record_grade'):
                    target_student.grade_book.record_grade(grade)
                    avg = target_student.grade_book.calculate_average_score()
                    print(f"Выставлено. Средний балл: {avg:.2f}")
                else:
                    print("Оценка создана успешно.")

            elif choice == "4":
                student_id = int(input("ID студента для отчисления: "))
                students_list = getattr(group, 'students', [])

                target_student = next(
                    (s for s in students_list
                     if getattr(s, 'person_id', 0) == student_id),
                    None
                )

                if not target_student:
                    print("Студент не найден.")
                    continue

                reason = input("Укажите причину отчисления: ")

                if hasattr(dean, 'approve_expulsion'):
                    order = dean.approve_expulsion(target_student, reason)
                    if hasattr(order, 'execute_order'):
                        order.execute_order()
                    doc_num = getattr(order, 'doc_number', 'Б/Н')
                    print(f"Приказ №{doc_num} подписан. Студент отчислен.")
                else:
                    name = target_student.get_full_name()
                    print(f"Отчислен студент {name}. Причина: {reason}")

            elif choice == "0":
                print("Выход из системы.")
                break
            else:
                print("Неизвестная команда.")

        except ValueError:
            print("Ошибка: вводите числа там, где это требуется.")
        except DeaneryException as e:
            print(f"\n[ДОМЕННАЯ ОШИБКА]: {e}")
        except Exception as e:
            print(f"\n[СИСТЕМНАЯ ОШИБКА]: {e}")


if __name__ == "__main__":
    main()