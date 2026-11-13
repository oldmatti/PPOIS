from typing import List, TYPE_CHECKING
if TYPE_CHECKING:
    from .dormitory_room import DormitoryRoom

class Dormitory:
    def __init__(self, building_number: str, address: str):
        self.building_number = building_number
        self.address = address
        self.rooms: List['DormitoryRoom'] = []

    def add_room(self, room: 'DormitoryRoom'):
        self.rooms.append(room)