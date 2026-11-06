
import base64
from html.parser import HTMLParser

from app.ingestion.gmail_client import get_gmail_service


# 1. Convert HTML into readable text
class HTMLTextExtractor(HTMLParser):

    def __init__(self):
        super().__init__()
        self.text = []

    def handle_data(self, data):
        self.text.append(data)

    def get_text(self):
        return " ".join(self.text)


# 2. Debug MIME structure
def debug_mime_structure(payload, level=0):

    indent = "    " * level

    print(indent + "MIME:", payload.get("mimeType"))

    body = payload.get("body", {})

    print(indent + "Body keys:", list(body.keys()))
    print(indent + "Body size:", body.get("size"))
    print(indent + "Attachment ID:", body.get("attachmentId"))

    for part in payload.get("parts", []):
        debug_mime_structure(part, level + 1)


# 3. Extract email content
def extract_text(service, message_id, payload):

    text_parts = []

    mime_type = payload.get("mimeType", "")
    body = payload.get("body", {})

    data = body.get("data")

    # Check whether content is stored as an attachment
    if not data and body.get("attachmentId"):

        attachment_id = body["attachmentId"]

        attachment = service.users().messages().attachments().get(
            userId="me",
            messageId=message_id,
            id=attachment_id
        ).execute()

        data = attachment.get("data")

    # Decode content if available
    if data and mime_type in ["text/plain", "text/html"]:

        decoded = base64.urlsafe_b64decode(data)
        content = decoded.decode("utf-8", errors="replace")

        if mime_type == "text/html":

            parser = HTMLTextExtractor()
            parser.feed(content)

            content = parser.get_text()

        text_parts.append(content)

    # Recursively inspect nested MIME parts
    for part in payload.get("parts", []):

        text_parts.extend(
            extract_text(service, message_id, part)
        )

    return text_parts


# 4. Fetch and inspect one email
def inspect_message(service, message_id):

    message = service.users().messages().get(
        userId="me",
        id=message_id,
        format="full"
    ).execute()

    payload = message.get("payload", {})

    print("\nEMAIL ID:", message_id)
    print("=" * 60)

    print("\nDEBUGGING MIME STRUCTURE:")
    debug_mime_structure(payload)

    text_parts = extract_text(service, message_id, payload)

    print("\nEXTRACTED EMAIL CONTENT:")
    print("=" * 60)

    if text_parts:

        for part in text_parts:
            print(part)

    else:
        print("No readable email body found.")


# 5. Search and inspect transaction emails
def inspect_emails():

    service = get_gmail_service()

    query = 'newer_than:90d from:noreplyubi-txn@ubi.bank.in'

    response = service.users().messages().list(
        userId="me",
        q=query,
        maxResults=10
    ).execute()

    messages = response.get("messages", [])

    print("Emails found:", len(messages))

    if not messages:
        print("No matching emails found.")
        return

    for item in messages:

        inspect_message(service, item["id"])


# 6. Program entry point
if __name__ == "__main__":

    inspect_emails()
