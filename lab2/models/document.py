from datetime import date

class Document:
    """Base class for all official university documents."""

    def __init__(self, document_id: str, creation_date: date, title: str):
        self.document_id = document_id
        self.creation_date = creation_date
        self.title = title
        self.is_signed = False  # по умолчанию документ не подписан

    def sign_document(self):
        """Changes the document status to signed."""
        self.is_signed = True