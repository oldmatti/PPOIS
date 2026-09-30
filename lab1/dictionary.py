#добавление нового английского слова и перевода для него (+=); в C++ предусмотреть перегрузку как для C-строк (char*), так и для std::string;
# удаление существующего английского слова из словаря (-=);
# поиск перевода английского слова ([]);
# замену перевода английского слова ([]);
# определение количества слов в словаре;
# загрузку словаря из файла.

class Dictionary:

    class _Node:
        def __init__(self, english, russian):
            self.english = english
            self.russian = russian
            self.left = None
            self.right = None

    def __init__(self):
        self.__root = None
        self.__count = 0

    def _insert(self, node, english, russian):
        # Базовый случай: дошли до края (пустоты)
        if node is None:
            self.__count += 1
            return self._Node(english, russian)

        # Сравниваем слова для выбора пути
        if english < node.english:
            node.left = self._insert(node.left, english, russian)
        elif english > node.english:
            node.right = self._insert(node.right, english, russian)
        else:
            # Слово уже существует (english == node.english).
            # По условиям словаря мы просто обновляем перевод на новый.
            node.russian = russian

        # Обязательно возвращаем текущий узел обратно родителю,
        # чтобы старые связи в дереве не оборвались
        return node

    def __iadd__(self, pair):#добавление нового английского слова и перевода для него (+=)
        """Добавление нового слова и перевода (оператор +=)."""
        english, russian = pair
        self.__root = self._insert(self.__root, english, russian)
        return self



    def _find_min(self, node):
        """Вспомогательный метод для поиска узла с минимальным ключом."""
        current = node
        while current.left is not None:
            current = current.left
        return current

    def _remove(self, node, english_word):
        # Базовый случай: дошли до пустоты, слова нет в дереве
        if node is None:
            raise KeyError(f"Слово '{english_word}' не найдено.")

        # Ищем нужное слово, спускаясь по дереву
        if english_word < node.english:
            node.left = self._remove(node.left, english_word)
        elif english_word > node.english:
            node.right = self._remove(node.right, english_word)
        else:
            # Слово найдено! Обрабатываем три случая удаления:

            # Случай 1 и 2: Узла нет левого или правого потомка.
            if node.left is None:
                self.__count -= 1
                return node.right
            elif node.right is None:
                self.__count -= 1
                return node.left

            # Случай 3: У узла есть оба потомка (и левый, и правый).
            min_node = self._find_min(node.right)

            # Копируем данные найденного узла в текущий (который хотим удалить)
            node.english = min_node.english
            node.russian = min_node.russian

            # Теперь рекурсивно удаляем тот самый минимальный узел-дубликат снизу
            node.right = self._remove(node.right, min_node.english)

        return node

    def __isub__(self, english_word): # удаление существующего английского слова из словаря (-=);
        """Удаление слова и перевода (оператор -=).
        Если слова в словаре нет, то операция игнорируется"""
        self.__root = self._remove(self.__root, english_word)
        return self


    def __getitem__(self, english_word):
        """Поиск перевода по английскому слову (оператор [])."""
        current = self.__root

        while current is not None:
            if english_word == current.english:
                return current.russian
            elif english_word < current.english:
                current = current.left
            else:
                current = current.right

        # Если цикл закончился, а мы так ничего и не вернули, значит слова нет
        raise KeyError(f"Слово '{english_word}' не найдено.")


    def __setitem__(self, english_word, new_russian):
        """Замена или добавление перевода через оператор []."""
        self.__root = self._insert(self.__root, english_word, new_russian)



    def __len__(self):
        """Возвращает количество слов в словаре."""
        return self.__count



    def _pre_order_save(self, node, file):
        """Скрытый рекурсивный метод для записи узлов (Корень -> Лево -> Право)."""
        if node is not None:
            # Сначала записываем текущий узел (Родитель)
            file.write(f"{node.english}-{node.russian}\n")

            # Затем рекурсивно обходим левое поддерево
            self._pre_order_save(node.left, file)

            # В конце рекурсивно обходим правое поддерево
            self._pre_order_save(node.right, file)

    def save_to_file(self, filename):
        """
        Сохраняет словарь в текстовый файл с использованием прямого обхода дерева.
        Это гарантирует, что при загрузке структура дерева будет восстановлена.
        """
        # Открываем файл на запись ('w' - write), указываем кодировку UTF-8 для русских букв
        with open(filename, 'w', encoding='utf-8') as file:
            # Запускаем рекурсивный обход, начиная с корня
            self._pre_order_save(self.__root, file)


    def load_from_file(self, filename):
        """
        Загружает словарь из текстового файла.
        Слова добавляются в текущее дерево."""

        # Открываем файл на чтение ('r' - read)
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                # Убираем пробелы и символы переноса строки по краям
                clean_line = line.strip()

                if not clean_line:
                    continue  # Пропускаем пустые строки, если они есть

                # Разбиваем строку по тире ровно один раз.
                # Если в английском слове есть дефис (t-shirt), он останется целым.
                parts = clean_line.split('-', 1)

                if len(parts) == 2:
                    english = parts[0].strip()
                    russian = parts[1].strip()

                    # Используем наш уже готовый оператор += (магический метод __iadd__)
                    self += (english, russian)
                else:
                    raise ValueError(f"Некорректный формат строки в файле: {clean_line}")



    def _compare_trees(self, node1, node2):
        """Скрытый метод для рекурсивного сравнения двух узлов и их потомков."""
        # Базовый случай 1: оба узла пустые (дошли до конца веток одновременно)
        if node1 is None and node2 is None:
            return True

        # Базовый случай 2: один узел есть, а другого нет (структура не совпадает)
        if node1 is None or node2 is None:
            return False

        # Сравниваем сами слова в текущих узлах
        if node1.english != node2.english or node1.russian != node2.russian:
            return False

        # Если текущие узлы равны, рекурсивно проверяем левые и правые ветки.
        # Деревья равны ТОЛЬКО если равны и левая, и правая части (оператор and)
        return (self._compare_trees(node1.left, node2.left) and
                self._compare_trees(node1.right, node2.right))

    def __eq__(self, other):
        """
        Проверяет два словаря на равенство (оператор ==)."""
        # 1. Проверяем, что сравниваем словарь со словарем, а не с числом или строкой
        if not isinstance(other, Dictionary):
            return False

        # 2. Оптимизация (быстрый отказ):
        # Если количество слов разное, деревья точно не равны.
        if len(self) != len(other): #переопределенный метод
            return False

        # 3. Если размеры равны, запускаем поузловое сравнение корней
        return self._compare_trees(self.__root, other._Dictionary__root)

    def __enter__(self):
        """
        Вход в контекстный менеджер.
        Вызывается при старте блока with.
        """
        # Мы просто возвращаем сам объект словаря,
        # чтобы он записался в переменную после слова 'as'
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Выход из контекстного менеджера.
        Вызывается АВТОМАТИЧЕСКИ при выходе из блока with
        или при возникновении ошибки внутри блока.
        """
        # Как только работа закончена, автоматически сохраняем всё в файл.
        # (Имя файла можно сделать переменной класса, но для простоты укажем здесь)
        self.save_to_file("dictionary_backup.txt")

        # Мы возвращаем False, чтобы сказать Питону:
        # "Если внутри блока with произошла ошибка, не прячь её, покажи пользователю!"
        return False