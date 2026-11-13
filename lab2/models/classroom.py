class Classroom:
    """Class representing a physical university classroom or lecture hall."""

    def __init__(self, room_number: str, capacity: int, has_projector: bool):
        self.room_number = room_number
        self.capacity = capacity
        self.has_projector = has_projector