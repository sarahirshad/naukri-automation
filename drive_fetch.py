import os
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io


FOLDER_ID = "1mX8crYRfjGr-zV5zzM36IRPsMLXJGyKW"


def fetch_latest_resume():
    creds_data = json.loads(os.environ["GOOGLE_TOKEN"])
    creds = Credentials.from_authorized_user_info(creds_data)

    service = build("drive", "v3", credentials=creds)

    results = service.files().list(
        q=f"'{FOLDER_ID}' in parents",
        orderBy="modifiedTime desc",
        pageSize=1,
        fields="files(id, name)"
    ).execute()

    files = results.get("files", [])

    if not files:
        raise Exception("No files found in Google Drive folder")

    file = files[0]
    file_id = file["id"]
    file_name = file["name"]

    os.makedirs("resumes", exist_ok=True)

    file_path = os.path.join("resumes", file_name)

    request = service.files().get_media(fileId=file_id)

    with io.FileIO(file_path, "wb") as fh:
        downloader = MediaIoBaseDownload(fh, request)
        done = False

        while not done:
            status, done = downloader.next_chunk()

    return file_path