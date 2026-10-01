# python -m unittest test_dictionary.py
# Чтобы доказать преподавателю, что у вас высокое покрытие (или настроить это в CI/CD на GitHub, как просят в ТЗ), используется стандартная утилита coverage
# Запуск тестов с покрытием: python3 -m coverage run -m unittest test_dictionary.py
# Вывод отчета: python3 -m coverage report -m
import unittest
import os
from dictionary import Dictionary


class TestDictionary(unittest.TestCase):
    # Константы, чтобы избежать "магических строк" (требование ТЗ)
    TEST_FILE = "test_data.txt"
    BACKUP_FILE = "dictionary_backup.txt"

    def setUp(self):
        """Вызывается перед каждым тестом. Подготавливает чистый словарь."""
        self.dict = Dictionary()

    def tearDown(self):
        """Вызывается после каждого теста. Убирает за собой тестовые файлы."""
        for filename in (self.TEST_FILE, self.BACKUP_FILE):
            if os.path.exists(filename):
                os.remove(filename)

    def test_initialization_and_len(self):
        """Проверка создания словаря и начального счетчика."""
        self.assertEqual(len(self.dict), 0)

    def test_add_and_get_word(self):
        """Проверка добавления (+=) и поиска ([])."""
        self.dict += ("apple", "яблоко")
        self.assertEqual(len(self.dict), 1)
        self.assertEqual(self.dict["apple"], "яблоко")

    def test_update_existing_word(self):
        """При обновлении перевода счетчик не должен расти."""
        self.dict += ("apple", "яблоко")
        self.dict += ("apple", "яблочко")
        self.assertEqual(len(self.dict), 1)
        self.assertEqual(self.dict["apple"], "яблочко")

    def test_add_invalid_format(self):
        """Защита от дурака: добавление неверного формата должно вызывать ValueError."""
        with self.assertRaises(ValueError):
            self.dict += "просто строка"

    def test_get_nonexistent_word(self):
        """Поиск несуществующего слова должен вызывать KeyError."""
        with self.assertRaises(KeyError):
            _ = self.dict["ghost"]

    def test_remove_word(self):
        """Удаление слова (-=) и пересчет количества."""
        self.dict += ("apple", "яблоко")
        self.dict += ("banana", "банан")
        self.dict -= "apple"

        self.assertEqual(len(self.dict), 1)
        with self.assertRaises(KeyError):
            _ = self.dict["apple"]

    def test_remove_nonexistent_word(self):
        """Удаление несуществующего слова вызывает KeyError."""
        with self.assertRaises(KeyError):
            self.dict -= "ghost"

    def test_equality_operator(self):
        """Проверка оператора == для двух словарей."""
        dict2 = Dictionary()

        # Заполняем одинаково
        self.dict += ("apple", "яблоко")
        dict2 += ("apple", "яблоко")
        self.assertTrue(self.dict == dict2)

        # Меняем второй словарь
        dict2 += ("cat", "кот")
        self.assertFalse(self.dict == dict2)

        # Сравнение с другим типом данных
        self.assertFalse(self.dict == "какая-то строка")

    def test_file_io(self):
        """Проверка сохранения в файл и загрузки из него."""
        self.dict += ("mouse", "мышь")
        self.dict += ("cat", "кот")

        self.dict.save_to_file(self.TEST_FILE)

        new_dict = Dictionary()
        new_dict.load_from_file(self.TEST_FILE)

        self.assertEqual(len(new_dict), 2)
        self.assertTrue(self.dict == new_dict)

    def test_load_corrupted_file(self):
        """Проверка загрузки сломанного файла."""
        with open(self.TEST_FILE, 'w', encoding='utf-8') as f:
            f.write("сломанная_строка_без_тире\n")

        with self.assertRaises(ValueError):
            self.dict.load_from_file(self.TEST_FILE)

    def test_context_manager(self):
        """Проверка работы with (автосохранение при выходе)."""
        with Dictionary() as ctx_dict:
            ctx_dict += ("dog", "собака")

        # После выхода из with должен появиться файл бэкапа
        self.assertTrue(os.path.exists(self.BACKUP_FILE))

    def test_remove_complex_cases(self):
        """Проверка сложных случаев удаления: узел-лист и узел с двумя потомками."""
        # Строим ветвистое дерево
        self.dict += ("m", "м")  # корень
        self.dict += ("b", "б")  # левый потомок
        self.dict += ("z", "з")  # правый потомок
        self.dict += ("a", "а")  # левый-левый (лист)
        self.dict += ("c", "ц")  # левый-правый (теперь у 'b' два потомка)

        # 1. Удаляем лист (нет потомков)
        self.dict -= "a"

        # 2. Удаляем узел с двумя потомками (у 'b' есть 'a' и 'c')
        # Это заставит сработать метод _find_min
        self.dict -= "b"

        self.assertEqual(len(self.dict), 3)
        with self.assertRaises(KeyError):
            _ = self.dict["b"]

    def test_eq_different_structure(self):
        """Проверка деревьев одинакового размера, но разной структуры и содержания."""
        dict2 = Dictionary()
        # Дерево 1: корень 'a', потомок 'b'
        self.dict += ("a", "1")
        self.dict += ("b", "2")

        # Дерево 2: корень 'b', потомок 'a'
        dict2 += ("b", "2")
        dict2 += ("a", "1")

        # Длина одинаковая (2), но структура разная
        self.assertFalse(self.dict == dict2)

    def test_load_empty_file(self):
        """Проверка загрузки из абсолютно пустого файла."""
        with open(self.TEST_FILE, 'w', encoding='utf-8'):
            pass  # Создаем пустой файл

        self.dict.load_from_file(self.TEST_FILE)
        self.assertEqual(len(self.dict), 0)

    def test_remove_node_with_only_left_child(self):
        """Покрытие красных строк 121-123: узел только с левым потомком."""
        self.dict += ("c", "ц")
        self.dict += ("a", "а")  # 'a' уходит влево от 'c'
        self.dict -= "c"  # Удаляем корень, остается только левая ветка
        self.assertEqual(len(self.dict), 1)

    def test_remove_node_with_two_children_explicit(self):
        """Покрытие _find_min и строк 126-133: узел с двумя потомками."""
        self.dict += ("m", "м")  # Корень
        self.dict += ("a", "а")  # Левый потомок
        self.dict += ("z", "з")  # Правый потомок
        self.dict -= "m"  # Удаляем корень, у которого ровно 2 ветки
        self.assertEqual(len(self.dict), 2)
        with self.assertRaises(KeyError):
            _ = self.dict["m"]

    def test_setitem_operator(self):
        """Покрытие красной строки 162: использование dict[key] = value."""
        self.dict["new_word"] = "новое_слово"
        self.assertEqual(self.dict["new_word"], "новое_слово")

    def test_load_with_empty_lines(self):
        """Покрытие красной строки 207: пропуск пустых строк при чтении файла."""
        with open(self.TEST_FILE, 'w', encoding='utf-8') as f:
            f.write("\napple-яблоко\n   \n\n")
        self.dict.load_from_file(self.TEST_FILE)
        self.assertEqual(len(self.dict), 1)

    def test_compare_different_shapes(self):
        """Покрытие красной строки 232: деревья разной формы."""
        dict2 = Dictionary()
        self.dict += ("a", "а")
        self.dict += ("b", "б")  # Ветка вправо

        dict2 += ("a", "а")  # У dict2 нет правого потомка, структура не совпадает
        self.assertFalse(self.dict == dict2)

    def test_getitem_missing_explicit(self):
        """Покрытие красной строки 157: ошибка при поиске."""
        self.dict += ("a", "а")
        with self.assertRaises(KeyError):
            _ = self.dict["ghost"]


if __name__ == '__main__':
    unittest.main()
