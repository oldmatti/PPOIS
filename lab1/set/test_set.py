import unittest
from set.set import CustomSet


class TestCustomSet(unittest.TestCase):
    def setUp(self):
        """Создаем базовые множества перед каждым тестом."""
        self.set_a = CustomSet(['a', 'b', 'c'])
        self.set_b = CustomSet(['b', 'c', 'd'])
        self.empty_set = CustomSet()

    def test_init_and_add(self):
        """Тест инициализации и добавления (без дубликатов)."""
        s = CustomSet(['a', 'a', 'b'])
        self.assertEqual(len(s), 2)
        s.add('c')
        self.assertEqual(len(s), 3)
        s.add('c')  # Дубликат не должен добавиться
        self.assertEqual(len(s), 3)

    def test_remove(self):
        """Тест удаления элементов."""
        self.set_a.remove('a')
        self.assertEqual(len(self.set_a), 2)
        self.assertFalse(self.set_a['a'])
        with self.assertRaises(KeyError):
            self.set_a.remove('z')

    def test_is_empty_and_len(self):
        """Тест проверки на пустоту и длины."""
        self.assertTrue(self.empty_set.is_empty())
        self.assertFalse(self.set_a.is_empty())
        self.assertEqual(len(self.empty_set), 0)
        self.assertEqual(len(self.set_a), 3)

    def test_eq(self):
        """Тест проверки на равенство."""
        s1 = CustomSet(['a', 'b'])
        s2 = CustomSet(['b', 'a'])
        self.assertEqual(s1, s2)
        self.assertNotEqual(s1, self.set_a)
        self.assertNotEqual(s1, "не множество")

    def test_str(self):
        """Тест строкового представления."""
        s = CustomSet(['a', 'b'])
        self.assertIn("a", str(s))
        self.assertIn("b", str(s))
        self.assertTrue(str(s).startswith("{") and str(s).endswith("}"))

    def test_getitem(self):
        """Тест проверки принадлежности ([])."""
        self.assertTrue(self.set_a['a'])
        self.assertFalse(self.set_a['z'])

    def test_add_operators(self):
        """Тест объединения (+ и +=)."""
        result = self.set_a + self.set_b
        self.assertEqual(len(result), 4)  # a, b, c, d

        s = CustomSet(['a'])
        s += CustomSet(['b'])
        self.assertEqual(len(s), 2)

        with self.assertRaises(TypeError):
            _ = self.set_a + "строка"
        with self.assertRaises(TypeError):
            self.set_a += "строка"

    def test_mul_operators(self):
        """Тест пересечения (* и *=)."""
        result = self.set_a * self.set_b
        self.assertEqual(len(result), 2)  # b, c
        self.assertTrue(result['b'] and result['c'])

        s = CustomSet(['a', 'b'])
        s *= CustomSet(['b', 'c'])
        self.assertEqual(len(s), 1)  # только b

        with self.assertRaises(TypeError):
            _ = self.set_a * "строка"
        with self.assertRaises(TypeError):
            self.set_a *= "строка"

    def test_sub_operators(self):
        """Тест разности (- и -=)."""
        result = self.set_a - self.set_b
        self.assertEqual(len(result), 1)  # только a
        self.assertTrue(result['a'])

        s = CustomSet(['a', 'b'])
        s -= CustomSet(['b', 'c'])
        self.assertEqual(len(s), 1)  # только a

        with self.assertRaises(TypeError):
            _ = self.set_a - "строка"
        with self.assertRaises(TypeError):
            self.set_a -= "строка"

    def test_powerset(self):
        """Тест построения булеана."""
        s = CustomSet(['a', 'b'])
        ps = s.powerset()
        # Для 2 элементов должно быть 2^2 = 4 подмножества: {}, {a}, {b}, {a, b}
        self.assertEqual(len(ps), 4)

    def test_from_string(self):
        """Тест парсинга множества из строки."""
        # Базовый случай
        s1 = CustomSet.from_string("{a,b,c}")
        self.assertEqual(len(s1), 3)
        self.assertTrue(s1['a'] and s1['b'] and s1['c'])

        # Случай с вложенностью
        s2 = CustomSet.from_string("{a,{b}}")
        self.assertEqual(len(s2), 2)

        # Ошибки парсинга
        with self.assertRaises(ValueError):
            CustomSet.from_string("a,b,c}")  # Нет начальной скобки
        with self.assertRaises(ValueError):
            CustomSet.from_string("{a,b")  # Нет конечной скобки


if __name__ == '__main__':
    unittest.main()
