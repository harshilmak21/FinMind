
from app.ingestion.gmail_client import get_gmail_service


def inspect_emails():

    service = get_gmail_service()

    # Search recent emails related to UPI or Google Pay
    query = 'newer_than:90d {"Google Pay" UPI}'

    response = service.users().messages().list(
        userId="me",
        q=query,
        maxResults=20
    ).execute()

    messages = response.get("messages", [])

    print(f"\nFound {len(messages)} candidate emails\n")

    for item in messages:

        message = service.users().messages().get(
            userId="me",
            id=item["id"],
            format="metadata",
            metadataHeaders=["From", "Subject", "Date"]
        ).execute()

        headers = message.get("payload", {}).get("headers", [])

        details = {
            h["name"]: h["value"]
            for h in headers
        }

        print("\n" + "=" * 60)
        print("EMAIL ID:", item["id"])
        print("FROM:", details.get("From"))
        print("SUBJECT:", details.get("Subject"))
        print("DATE:", details.get("Date"))
        print("SNIPPET:", message.get("snippet", ""))


if __name__ == "__main__":
    inspect_emails()
