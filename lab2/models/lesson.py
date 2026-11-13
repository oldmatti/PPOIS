from datetime import datetime
from typing import TYPE_CHECKING
from .classroom import Classroom

if TYPE_CHECKING:
    from .subject import Subject
    from .professor import Professor
    from .study_group import StudyGroup


class Lesson:
    """Class representing a scheduled class session (lecture or practice)."""

    def __init__(self, lesson_id: str, start_time: datetime, end_time: datetime,
                 subject: 'Subject', professor: 'Professor',
                 group: 'StudyGroup', classroom: Classroom):
        self.lesson_id = lesson_id
        self.start_time = start_time
        self.end_time = end_time

        # сохраняем ссылки на другие объекты
        self.subject = subject
        self.professor = professor
        self.group = group
        self.classroom = classroom