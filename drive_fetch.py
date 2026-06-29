import os
import json
import io
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload


load_dotenv()


def fetch_latest_resume():
    print("Downloading latest resume from Google Drive...")

    # Read token from token.json (NOT env variable)
    with open("token.json", "r") as f:
        token_data = json.load(f)

    creds = Credentials.from_authorized_user_info(token_data)

    service = build("drive", "v3", credentials=creds)

    folder_id = os.getenv("GOOGLE_FOLDER_ID")

    query = f"'{folder_id}' in parents and trashed=false"

    results = service.files().list(
        q=query,
        orderBy="modifiedTime desc",
        pageSize=1,
        fields="files(id, name)"
    ).execute()

    files = results.get("files", [])

    if not files:
        raise Exception("No files found in Google Drive folder")

    latest_file = files[0]
    file_id = latest_file["id"]
    file_name = latest_file["name"]

    print(f"Latest file found: {file_name}")

    os.makedirs("resumes", exist_ok=True)

    request = service.files().get_media(fileId=file_id)

    file_path = os.path.join("resumes", file_name)

    with io.FileIO(file_path, "wb") as fh:
        downloader = MediaIoBaseDownload(fh, request)

        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"Download progress: {int(status.progress() * 100)}%")

    print(f"Downloaded successfully: {file_path}")

    return os.path.abspath(file_path)