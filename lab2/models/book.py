from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from .student import Student

class Book:
    def __init__(self, title: str, author: str, isbn: str):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.borrowed_by: Optional['Student'] = None

    def assign_to(self, student: 'Student'):
        self.borrowed_by = student