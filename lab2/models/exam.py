from datetime import datetime
from typing import TYPE_CHECKING
from .lesson import Lesson
if TYPE_CHECKING:
    from .subject import Subject
    from .professor import Professor
    from .study_group import StudyGroup
    from .classroom import Classroom

class Exam(Lesson):
    def __init__(self, lesson_id: str, start_time: datetime, end_time: datetime,
                 subject: 'Subject', professor: 'Professor', group: 'StudyGroup',
                 classroom: 'Classroom', min_pass_score: int):
        super().__init__(lesson_id, start_time, end_time, subject, professor, group, classroom)
        self.min_pass_score = min_pass_score