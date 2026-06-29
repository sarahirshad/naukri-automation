from drive_fetch import fetch_latest_resume
from naukri_update import update_resume


def main():
    print("Starting automation...")

    # Step 1: Fetch latest resume from Google Drive
    resume_path = fetch_latest_resume()
    print(f"Downloaded: {resume_path}")

    # Step 2: Upload to Naukri
    update_resume(resume_path)

    print("Resume updated successfully!")


if __name__ == "__main__":
    main() 