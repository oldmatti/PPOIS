class DeaneryException(Exception):
    """Базовый класс для всех исключений домена Деканат."""
    pass

class StudentNotFoundException(DeaneryException):
    def __init__(self, student_id: int):
        super().__init__(f"Студент с ID {student_id} не найден в системе.")
        self.student_id = student_id

class InvalidGradeException(DeaneryException):
    def __init__(self, grade: int):
        super().__init__(f"Недопустимое значение оценки: {grade}. Оценка должна быть от 1 до 10.")
        self.grade = grade

class ScheduleConflictException(DeaneryException):
    def __init__(self, day: str, time_slot: int):
        super().__init__(f"Конфликт расписания: на день '{day}', пара {time_slot} уже назначено занятие.")

class InsufficientCreditsException(DeaneryException):
    def __init__(self, student_name: str):
        super().__init__(f"Студенту {student_name} не хватает баллов или закрытых предметов для перевода.")

class InvalidGroupTransferException(DeaneryException):
    def __init__(self, student_name: str, target_group: str):
        super().__init__(f"Невозможно перевести студента {student_name} в группу {target_group}. Группа переполнена или не совпадает специальность.")

class DormitoryFullException(DeaneryException):
    def __init__(self, building_number: str):
        super().__init__(f"В общежитии №{building_number} нет свободных мест.")

class ScholarshipDeniedException(DeaneryException):
    def __init__(self, student_name: str, reason: str):
        super().__init__(f"Студенту {student_name} отказано в стипендии. Причина: {reason}.")

class ExpulsionRulesViolationException(DeaneryException):
    def __init__(self, student_name: str):
        super().__init__(f"Нарушение правил отчисления: нельзя отчислить студента {student_name} без веской причины или подписи декана.")

class InvalidDocumentFormatException(DeaneryException):
    def __init__(self, doc_number: str):
        super().__init__(f"Документ №{doc_number} имеет неверный формат или заполнен некорректно.")

class UnauthorizedAccessException(DeaneryException):
    def __init__(self, role: str, action: str):
        super().__init__(f"Отказано в доступе: роль '{role}' не имеет прав для выполнения действия '{action}'.")

class RetakeLimitExceededException(DeaneryException):
    def __init__(self, student_name: str, subject_name: str):
        super().__init__(f"Студент {student_name} исчерпал лимит пересдач (более 3 раз) по предмету '{subject_name}'.")