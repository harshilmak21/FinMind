
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly"
]


def get_gmail_service():

    credentials = None

    # Check whether an authentication token already exists
    if os.path.exists("token.json"):

        credentials = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES
        )

    # Authenticate if necessary
    if not credentials or not credentials.valid:

        if credentials and credentials.expired and credentials.refresh_token:

            credentials.refresh(Request())

        else:

            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES
            )

            credentials = flow.run_local_server(port=0)

        # Save authentication token
        with open("token.json", "w") as token:
            token.write(credentials.to_json())

    # Create Gmail API service
    service = build(
        "gmail",
        "v1",
        credentials=credentials
    )

    print("Gmail authentication successful!")

    return service

