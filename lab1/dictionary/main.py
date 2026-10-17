from lab1.dictionary.dictionary import Dictionary


def print_menu():
    """Выводит меню на экран."""
    print("\n" + "=" * 30)
    print(" АНГЛО-РУССКИЙ СЛОВАРЬ (BST) ")
    print("=" * 30)
    print("1. Добавить или обновить слово")
    print("2. Найти перевод")
    print("3. Удалить слово")
    print("4. Показать количество слов")
    print("0. Выйти и сохранить")
    print("=" * 30)


def main():
    filename = "my_dictionary.txt"

    with Dictionary() as my_dict:

        try:
            my_dict.load_from_file(filename)
            print(f"[*] Словарь успешно загружен. Слов внутри: {len(my_dict)}")
        except FileNotFoundError:
            print("[*] Файл словаря не найден. Создан новый пустой словарь.")
        except ValueError as e:
            print(f"[!] Ошибка чтения файла: {e}")

        while True:
            print_menu()
            choice = input("Выберите пункт меню (0-4): ").strip()

            if choice == "1":
                eng = input("Введите английское слово: ").strip()
                rus = input("Введите перевод: ").strip()
                try:
                    my_dict += (eng, rus)
                    print(f"[+] Слово '{eng}' успешно сохранено!")
                except ValueError as e:
                    print(f"[!] Ошибка ввода: {e}")

            elif choice == "2":
                eng = input("Какое слово найти? ").strip()
                try:
                    translation = my_dict[eng]
                    print(f"[>] Перевод: {translation}")
                except KeyError:
                    print(f"[!] Слово '{eng}' не найдено в словаре.")

            elif choice == "3":
                eng = input("Какое слово удалить? ").strip()
                try:
                    my_dict -= eng
                    print(f"[-] Слово '{eng}' удалено из словаря.")
                except KeyError:
                    print(f"[!] Ошибка: Слова '{eng}' и так нет в словаре.")

            elif choice == "4":
                print(f"[i] Сейчас в словаре слов: {len(my_dict)}")

            elif choice == "0":
                print("Сохранение данных...")
                my_dict.save_to_file(filename)
                print("До свидания!")
                break

            else:
                print("[!] Неизвестная команда. Пожалуйста, введите цифру от 0 до 4.")


if __name__ == "__main__":
    main()
