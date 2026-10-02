from set import CustomSet


def print_menu():
    print("\n--- Меню работы с Канторовским Множеством ---")
    print("1. Создать множество из строки (например, {a, b, {c}})")
    print("2. Добавить элемент")
    print("3. Удалить элемент")
    print("4. Вывести текущее множество и его мощность")
    print("5. Проверить принадлежность элемента ([])")
    print("6. Построить булеан (множество всех подмножеств)")
    print("7. Объединить с другим множеством (+)")
    print("8. Найти пересечение с другим множеством (*)")
    print("9. Найти разность с другим множеством (-)")
    print("0. Выход")


def main():
    my_set = CustomSet()
    print("Программа запущена. Создано пустое множество.")

    while True:
        print_menu()
        choice = input("Выберите действие (0-9): ")

        try:
            if choice == '1':
                s = input("Введите строку множества (обязательно с фигурными скобками): ")
                my_set = CustomSet.from_string(s)
                print(f"Множество успешно создано: {my_set}")

            elif choice == '2':
                elem = input("Введите элемент для добавления: ")
                my_set.add(elem)
                print(f"Элемент добавлен. Текущее множество: {my_set}")

            elif choice == '3':
                elem = input("Введите элемент для удаления: ")
                my_set.remove(elem)
                print(f"Элемент удален. Текущее множество: {my_set}")

            elif choice == '4':
                print(f"Текущее множество: {my_set}")
                print(f"Мощность (количество элементов): {len(my_set)}")
                print(f"Пустое ли? {'Да' if my_set.is_empty() else 'Нет'}")

            elif choice == '5':
                elem = input("Введите элемент для проверки: ")
                # Используем перегруженный оператор []
                if my_set[elem]:
                    print(f"Элемент '{elem}' принадлежит множеству.")
                else:
                    print(f"Элемент '{elem}' НЕ принадлежит множеству.")

            elif choice == '6':
                powerset = my_set.powerset()
                print(f"Булеан текущего множества: {powerset}")

            elif choice == '7':
                s = input("Введите второе множество строкой для объединения: ")
                other_set = CustomSet.from_string(s)
                result = my_set + other_set
                print(f"Результат объединения: {result}")

            elif choice == '8':
                s = input("Введите второе множество строкой для пересечения: ")
                other_set = CustomSet.from_string(s)
                result = my_set * other_set
                print(f"Результат пересечения: {result}")

            elif choice == '9':
                s = input("Введите второе множество строкой для разности: ")
                other_set = CustomSet.from_string(s)
                result = my_set - other_set
                print(f"Результат разности: {result}")

            elif choice == '0':
                print("Выход из программы. До свидания!")
                break
            else:
                print("Неверный ввод. Попробуйте еще раз.")
        except Exception as e:
            # Отлавливаем любые ошибки (например, если нет закрывающей скобки) и не даем программе упасть
            print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
