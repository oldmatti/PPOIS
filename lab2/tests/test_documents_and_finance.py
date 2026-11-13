import unittest
from datetime import date
from models import (
    Contract, Invoice, Student, WarningOrder,
    TransferOrder, GraduationOrder, StudyGroup
)


class TestDocsAndFinance(unittest.TestCase):
    def setUp(self):
        self.student = Student(1, "Иван", "Иванов", date(2005, 1, 1))

    def test_finance(self):
        contract = Contract("C-1", self.student, 1500.0)
        contract.sign_contract()
        self.assertTrue(contract.is_active)

        invoice = Invoice("INV-1", contract, date.today())
        invoice.pay_invoice()
        self.assertTrue(invoice.is_paid)

    def test_orders(self):
        warning = WarningOrder(
            "W-1", date.today(), self.student, "Прогулы"
        )
        self.assertEqual(warning.reason, "Прогулы")

        group = StudyGroup("102")
        transfer = TransferOrder(
            "T-1", date.today(), self.student, group
        )
        self.assertEqual(transfer.new_group, group)

        grad = GraduationOrder(
            "G-1", date.today(), self.student, "Бакалавр"
        )
        self.assertEqual(grad.degree, "Бакалавр")