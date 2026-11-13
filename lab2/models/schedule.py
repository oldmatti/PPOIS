from typing import List
from .lesson import Lesson


class Schedule:
    """Class representing the university timetable and managing lesson conflicts."""

    def __init__(self):
        self.lessons: List[Lesson] = []

    def add_lesson(self, new_lesson: Lesson):
        """
        Adds a lesson to the schedule.
        Raises ValueError if there is a time and room conflict.
        """
        for existing_lesson in self.lessons:
            # проверка, пытаются ли занять ту же самую аудиторию
            if existing_lesson.classroom.room_number == new_lesson.classroom.room_number:

                if (existing_lesson.start_time < new_lesson.end_time and
                        new_lesson.start_time < existing_lesson.end_time):
                    raise ValueError(f"Conflict! Room {new_lesson.classroom.room_number} is already booked.")

        self.lessons.append(new_lesson)