class CustomSet:
    """Класс, реализующий неориентированное множество."""

    def __init__(self, elements=None):
        """Конструктор множества. Инициализирует пустой список элементов."""
        self.elements = []
        if elements is not None:
            for elem in elements:
                self.add(elem)

    def add(self, item):
        """Добавление элемента. Дубликаты игнорируются."""
        # Благодаря переопределенному __eq__, оператор 'in' сам поймет,
        # как сравнивать даже вложенные множества
        if item not in self.elements:
            self.elements.append(item)

    def is_empty(self):
        """Проверка на пустое множество."""
        return len(self.elements) == 0

    def __len__(self):
        """Определение мощности множества (количества элементов)."""
        return len(self.elements)

    def __eq__(self, other):
        """
        Проверка множеств на равенство (==).
        Множества равны, если состоят из одних и тех же элементов, независимо от порядка.
        """
        if not isinstance(other, CustomSet):
            return False
        if len(self) != len(other):
            return False

        # Проверяем, что каждый наш элемент есть в другом множестве
        for item in self.elements:
            if item not in other.elements:
                return False
        return True

    def __str__(self):
        """Красивый вывод множества в виде {a, b, {c}}."""
        # Преобразуем все элементы в строки и склеиваем через запятую
        items_str = ", ".join(str(item) for item in self.elements)
        return f"{{{items_str}}}"

    def __repr__(self):
        """Технический вывод (для отладки совпадает с обычным)."""
        return self.__str__()

    def powerset(self):
        """
        Построение булеана (множества всех подмножеств) данного множества.
        Например, для {a, b} вернет {{}, {a}, {b}, {a, b}}.
        """
        result = CustomSet()

        # Начинаем с базового случая: список, содержащий только пустое подмножество
        subsets = [[]]

        for elem in self.elements:
            # Для каждого элемента множества удваиваем список подмножеств,
            # добавляя этот элемент к каждому уже существующему подмножеству
            new_subsets = []
            for sub in subsets:
                new_subsets.append(sub + [elem])
            subsets.extend(new_subsets)

        # Теперь превращаем каждый список обратно в CustomSet и кладем в результат
        for sub_list in subsets:
            result.add(CustomSet(sub_list))

        return result

    @staticmethod
    def from_string(s: str):
        """
        Формирование множества из строки.
        Пример: CustomSet.from_string("{a, b, {c}, {}}")
        """
        # Убираем все пробелы для удобства парсинга
        s = s.replace(" ", "")
        if not s or s[0] != '{' or s[-1] != '}':
            raise ValueError("Строка должна начинаться с '{' и заканчиваться '}'.")

        stack = []
        current_word = ""
        root = None

        # Идем по каждому символу строки
        for char in s:
            if char == '{':
                # Начинается новое (возможно, вложенное) множество
                new_set = CustomSet()
                if stack:
                    # Кладем его внутрь родительского множества
                    stack[-1].add(new_set)
                else:
                    root = new_set
                stack.append(new_set)

            elif char == '}':
                # Множество закрывается
                if current_word:
                    stack[-1].add(current_word)
                    current_word = ""

                if not stack:
                    raise ValueError("Ошибка: лишняя закрывающая скобка '}'.")
                stack.pop()

            elif char == ',':
                # Элемент закончился
                if current_word:
                    stack[-1].add(current_word)
                    current_word = ""
            else:
                # Накапливаем буквы элемента (например, 'a', 'b', 'c')
                current_word += char

        if stack:
            raise ValueError("Ошибка: не хватает закрывающей скобки '}'.")

        return root
