from typing import List, TYPE_CHECKING
if TYPE_CHECKING:
    from .book import Book
    from .student import Student

class Library:
    def __init__(self, name: str):
        self.name = name
        self.books: List['Book'] = []

    def add_book(self, book: 'Book'):
        self.books.append(book)

    def issue_book(self, book: 'Book', student: 'Student'):
        book.assign_to(student)