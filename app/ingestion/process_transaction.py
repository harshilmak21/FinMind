from app.ingestion.gmail_client import get_gmail_service
from app.ingestion.inspect_message_body import extract_text
from app.ingestion.transaction_parser import parse_transaction_email

def process_transactions():

    service = get_gmail_service()

    query = 'newer_than:90d from noreplyubi-txn@ubi.bank.in'

    response = service.users().messages().list(
        userId = "me",
        q = query,
        maxResults = 10
    ).execute()

    messages = response.get("messages",[])

    print("emails found ") , len(messages)

    transactions = []

    for item in messages:

        message_id = item["id"]

        message = service.users().messages().get(
            userId = "me",
            id = message_id,
            format = "full"
        ).execute()

        payload = message.get("payload" , {})
        email_parts = extract_text(service , message_id , payload)

        email_text = "\n".join(email_parts)

        try:
            transaction = parse_transaction_email(email_text)
            transactions.append(transaction)
            print("\nTransaction extracted:")
            print(transaction)

        except ValueError as error:
            print(f"Could not parse Email:",message_id)
            print(f"Reason : {error}")

        print(f"Total transcations extracted : {len(transactions)}")

        return transactions

if __name__ == "__main__":
    process_transactions()