from typing import List, TYPE_CHECKING
if TYPE_CHECKING:
    from .student import Student
from exceptions.dormitory_full_exception import DormitoryFullException

class DormitoryRoom:
    def __init__(self, room_number: str, capacity: int):
        self.room_number = room_number
        self.capacity = capacity
        self.students: List['Student'] = []

    def assign_student(self, student: 'Student'):
        if len(self.students) >= self.capacity:
            raise DormitoryFullException(self.room_number)
        self.students.append(student)