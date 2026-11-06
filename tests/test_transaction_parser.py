import unittest
from datetime import datetime
from decimal import Decimal

from app.ingestion.transaction_parser import parse_transaction_email

class TestTransactionParser(unittest.TestCase):

    def setUp(self):

        self.email_text = """
        Your fund transfer request through UPI
        has been processed successfully.

        Transaction Details

        1. Payee Name : Coffee Shop
        2. Amount : Rs. 100.00
        3. Channel : UPI
        4. Transaction ID/RRN : 667533697212
        5. Transaction Status : Success
        6. Transaction Date and Time : 05-11-2026 18:12:34
        7. Debit Account Number : *4933
        """

    def test_payee_extraction(self):

        result = parse_transaction_email(self.email_text)

    def test_amount_extraction(self):
        result = parse_transaction_email(self.email_text)
        self.assertEqual(result["amount"] , Decimal("100.00"))

    def test_transaction_id(self):

        result = parse_transaction_email(self.email_text)

        self.assertEqual(
            result["transaction_id"],
            "667533697212"
        )

    def test_date_extraction(self):

        result = parse_transaction_email(self.email_text)

        expected_date = datetime(2026, 11, 5, 18, 12, 34)

        self.assertEqual(
            result["transaction_datetime"],
            expected_date
        )

    def test_transaction_status(self):

        result = parse_transaction_email(self.email_text)

        self.assertEqual(result["status"], "Success")

    def test_missing_amount(self):

        invalid_email = self.email_text.replace(
            "2. Amount : Rs. 100.00",
            ""
        )

        with self.assertRaises(ValueError):

            parse_transaction_email(invalid_email)


if __name__ == "__main__":
    unittest.main()

