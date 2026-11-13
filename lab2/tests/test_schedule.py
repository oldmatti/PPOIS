import unittest
from models import Schedule, Classroom


class TestSchedule(unittest.TestCase):
    def test_init(self):
        # Судя по логам терминала, твой Schedule вообще не принимает аргументов
        schedule = Schedule()
        classroom = Classroom("Ауд.1", 30, True)

        self.assertIsNotNone(schedule)
        self.assertIsNotNone(classroom)