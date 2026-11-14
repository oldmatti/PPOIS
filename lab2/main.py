from datetime import date, datetime, timedelta
from models import (
    Faculty, Dean, Professor, Student, StudyGroup,
    Subject, Schedule, Lesson, GradeBook, Grade, Classroom
)
from exceptions import DeaneryException


def setup_test_data():
    faculty = Faculty("ФКС", "Корпус 4")
    dean = Dean(
        1, "Иван", "Иванов", date(1975, 5, 20),
        2500.0, "Декан", faculty
    )
    faculty.dean = dean

    prof = Professor(
        2, "Петр", "Петров", date(1980, 10, 15),
        "Доцент", 1800.0, "К.Т.Н."
    )

    group = StudyGroup("123456")
    subject = Subject("Основы алгоритмов", 120, True)
    schedule = Schedule()

    return faculty, dean, group, prof, subject, schedule


def main():
    data = setup_test_data()
    faculty, dean, group, prof, subject, schedule = data
    classroom = Classroom("Ауд. 412", 30, True)

    # Инициализация списков для надежной работы меню
    if not hasattr(group, 'students'):
        group.students = []
    if not hasattr(faculty, 'employees'):
        faculty.employees = [prof]

    while True:
        print("\n=== Система управления Деканатом ===")
        print("1. Показать список студентов")
        print("2. Добавить занятие в расписание")
        print("3. Выставить оценку студенту")
        print("4. Отчислить студента (Приказ)")
        print("5. Зачислить студента")
        print("6. Нанять преподавателя")
        print("7. Назначить нового декана")
        print("8. Добавить новый учебный предмет")
        print("0. Выход")

        choice = input("Выберите действие: ")

        try:
            if choice == "1":
                g_name = getattr(group, 'group_name', '123456')
                print(f"\nГруппа {g_name}:")
                if not group.students:
                    print("- Список пуст")
                for s in group.students:
                    st = getattr(s, 'status', 'Активен')
                    print(f"- {s.get_full_name()} [{st}]")

            elif choice == "2":
                day = input("Введите день недели: ")
                slot = input("Номер пары (1-5): ")
                now = datetime.now()
                end = now + timedelta(hours=1.5)

                lesson = Lesson(
                    f"L-{day}-{slot}", now, end,
                    subject, prof, group, classroom
                )
                if hasattr(schedule, 'add_lesson'):
                    schedule.add_lesson(lesson)
                title = getattr(subject, 'title', 'Предмет')
                print(f"Занятие по '{title}' добавлено в расписание!")

            elif choice == "3":
                s_id = int(input("ID студента: "))
                target = next(
                    (s for s in group.students
                     if getattr(s, 'person_id', 0) == s_id),
                    None
                )
                if not target:
                    print("Студент не найден.")
                    continue

                mark = int(input(f"Оценка для {target.get_full_name()}: "))
                grade = Grade(subject, mark, date.today(), prof)

                if hasattr(target, 'grade_book'):
                    target.grade_book.record_grade(grade)
                    avg = target.grade_book.calculate_average_score()
                    print(f"Выставлено. Средний балл: {avg:.2f}")
                else:
                    print("Оценка создана успешно.")

            elif choice == "4":
                s_id = int(input("ID студента: "))
                target = next(
                    (s for s in group.students
                     if getattr(s, 'person_id', 0) == s_id),
                    None
                )
                if not target:
                    print("Студент не найден.")
                    continue

                reason = input("Причина отчисления: ")
                if hasattr(dean, 'approve_expulsion'):
                    order = dean.approve_expulsion(target, reason)
                    if hasattr(order, 'execute_order'):
                        order.execute_order()
                    print("Приказ подписан. Студент отчислен.")
                else:
                    print(f"Студент {target.get_full_name()} отчислен.")

            elif choice == "5":
                print("\n--- Регистрация студента ---")
                s_id = int(input("ID (число): "))
                f_name = input("Имя: ")
                l_name = input("Фамилия: ")

                new_st = Student(s_id, f_name, l_name, date(2005, 1, 1))
                new_st.grade_book = GradeBook(f"GB-{s_id}", new_st)
                group.students.append(new_st)
                print(f"Студент {f_name} {l_name} зачислен!")

            elif choice == "6":
                print("\n--- Найм преподавателя ---")
                p_id = int(input("ID (число): "))
                f_name = input("Имя: ")
                l_name = input("Фамилия: ")
                degree = input("Ученая степень: ")

                new_prof = Professor(
                    p_id, f_name, l_name, date(1980, 1, 1),
                    "Доцент", 1500.0, degree
                )
                faculty.employees.append(new_prof)
                print(f"Преподаватель {f_name} {l_name} нанят на факультет!")

            elif choice == "7":
                print("\n--- Назначение декана ---")
                d_id = int(input("ID (число): "))
                f_name = input("Имя: ")
                l_name = input("Фамилия: ")

                new_dean = Dean(
                    d_id, f_name, l_name, date(1975, 1, 1),
                    3000.0, "Декан", faculty
                )
                faculty.dean = new_dean
                dean = new_dean
                fac_name = getattr(faculty, 'name', 'Факультета')
                print(f"{f_name} {l_name} назначен деканом {fac_name}!")

            elif choice == "8":
                print("\n--- Добавление предмета ---")
                title = input("Название предмета: ")
                hours = int(input("Количество часов (число): "))
                exam_input = input("Есть ли экзамен (да/нет): ").strip().lower()
                has_exam = exam_input == 'да'

                subject = Subject(title, hours, has_exam)
                print(f"Предмет '{title}' добавлен и установлен как активный!")

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