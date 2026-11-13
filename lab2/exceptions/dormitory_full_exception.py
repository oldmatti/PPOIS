from .deanery_exception import DeaneryException

class DormitoryFullException(DeaneryException):
    def __init__(self, building_number: str):
        super().__init__(f"Dormitory No. {building_number} has no available rooms.")