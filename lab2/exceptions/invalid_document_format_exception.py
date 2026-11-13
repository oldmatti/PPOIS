from .deanery_exception import DeaneryException

class InvalidDocumentFormatException(DeaneryException):
    def __init__(self, doc_number: str):
        super().__init__(f"Document No. {doc_number} has an invalid format or is filled incorrectly.")