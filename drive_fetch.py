from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from dotenv import load_dotenv
import os
import io

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID")


def authenticate_google():
    creds = None

    # Load existing token if available
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file(
            "token.json", SCOPES
        )

    # If no valid token, create new one
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save token for future runs
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return creds


def get_latest_resume():
    creds = authenticate_google()

    service = build("drive", "v3", credentials=creds)

    results = service.files().list(
        q=f"'{FOLDER_ID}' in parents",
        orderBy="modifiedTime desc",
        pageSize=1,
        fields="files(id, name)"
    ).execute()

    files = results.get("files", [])

    if not files:
        print("No files found in Google Drive folder.")
        return None

    file_id = files[0]["id"]
    file_name = files[0]["name"]

    request = service.files().get_media(fileId=file_id)

    os.makedirs("resumes", exist_ok=True)

    file_path = os.path.join("resumes", file_name)

    with io.FileIO(file_path, "wb") as fh:
        downloader = MediaIoBaseDownload(fh, request)

        done = False
        while not done:
            status, done = downloader.next_chunk()

    print(f"Downloaded: {file_name}")
    return file_path


if __name__ == "__main__":
    get_latest_resume()