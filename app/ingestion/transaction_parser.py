import re
from datetime import datetime
from decimal import Decimal


def extract_field(pattern , text , field_name):

    match = re.search(pattern , text , re.IGNORECASE)
    if not match:
        raise ValueError(f"Could not extract {field_name}")

    return match.group(1).strip()

def parse_transaction_email(email_text):

    text = re.sub(r"\s+", " ", email_text).strip()

    # Extract individual transaction fields
    payee = extract_field(
        r"Payee Name\s*:\s*(.*?)\s+(?=\d+\.\s*Amount\s*:)",
        text,
        "Payee Name"
    )

    amount = extract_field(
        r"Amount\s*:\s*Rs\.?\s*([\d,]+(?:\.\d{1,2})?)",
        text,
        "Amount"
    )

    channel = extract_field(
        r"Channel\s*:\s*([A-Za-z]+)",
        text,
        "Channel"
    )

    transaction_id = extract_field(
        r"Transaction ID/RRN\s*:\s*(\d+)",
        text,
        "Transaction ID"
    )

    status = extract_field(
        r"Transaction Status\s*:\s*([A-Za-z]+)",
        text,
        "Transaction Status"
    )

    transaction_date = extract_field(
        r"Transaction Date and Time\s*:\s*(\d{2}-\d{2}-\d{4}\s+\d{2}:\d{2}:\d{2})",
        text,
        "Transaction Date"
    )

    # Convert extracted values into proper Python types
    amount = Decimal(amount.replace(",", ""))

    transaction_date = datetime.strptime(
        transaction_date,
        "%d-%m-%Y %H:%M:%S"
    )

    transaction = {
        "payee": payee,
        "amount": amount,
        "currency": "INR",
        "channel": channel,
        "transaction_id": transaction_id,
        "status": status,
        "transaction_datetime": transaction_date
    }

    return transaction
