from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .subject import Subject

class Curriculum:
    """Class representing an academic curriculum or degree plan."""

    def __init__(self, curriculum_id: str, major: str):
        self.curriculum_id = curriculum_id
        self.major = major
        self.subjects: List['Subject'] = []

    def add_subject(self, subject: 'Subject'):
        """Adds a required subject to this curriculum."""
        self.subjects.append(subject)