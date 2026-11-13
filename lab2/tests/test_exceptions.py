import unittest
from exceptions import (
    StudentNotFoundException, InsufficientCreditsException,
    InvalidGroupTransferException, DormitoryFullException,
    ScholarshipDeniedException, ExpulsionRulesViolationException,
    InvalidDocumentFormatException, UnauthorizedAccessException,
    RetakeLimitExceededException
)

class TestExceptionsInitialization(unittest.TestCase):
    def test_all_custom_exceptions(self):
        exceptions = [
            StudentNotFoundException(1),
            InsufficientCreditsException("Иван"),
            InvalidGroupTransferException("Иван", "102"),
            DormitoryFullException("4"),
            ScholarshipDeniedException("Иван", "Долги"),
            ExpulsionRulesViolationException("Иван"),
            InvalidDocumentFormatException("DOC-1"),
            UnauthorizedAccessException("Студент", "Удаление"),
            RetakeLimitExceededException("Иван", "Математика")
        ]
        for exc in exceptions:
            self.assertTrue(isinstance(exc, Exception))