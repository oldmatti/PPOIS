from datetime import date
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .contract import Contract

class Invoice:
    def __init__(self, invoice_id: str, contract: 'Contract', due_date: date):
        self.invoice_id = invoice_id
        self.contract = contract
        self.due_date = due_date
        self.is_paid = False

    def pay_invoice(self):
        self.is_paid = True