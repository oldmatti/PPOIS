from datetime import date
from .document import Document

class Order(Document):
    """Base class representing a formal university order. Inherits from Document."""

    def __init__(self, document_id: str, creation_date: date, title: str, order_type: str):
        super().__init__(document_id, creation_date, title)
        self.order_type = order_type