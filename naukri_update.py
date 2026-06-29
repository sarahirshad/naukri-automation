from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import os
import time

load_dotenv()

EMAIL = os.getenv("NAUKRI_EMAIL")
PASSWORD = os.getenv("NAUKRI_PASSWORD")


def update_resume():
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install())
    )

    driver.maximize_window()

    driver.get("https://www.naukri.com/nlogin/login")

    time.sleep(3)

    driver.find_element(By.ID, "usernameField").send_keys(EMAIL)
    driver.find_element(By.ID, "passwordField").send_keys(PASSWORD)

    driver.find_element(
        By.XPATH,
        "//button[text()='Login']"
    ).click()

    time.sleep(5)

    driver.get("https://www.naukri.com/mnjuser/profile")

    time.sleep(5)

    upload_btn = driver.find_element(
        By.XPATH,
        "//input[@type='file']"
    )

    resume_folder = "resumes"
    files = os.listdir(resume_folder)

    if not files:
        print("No resume found")
        driver.quit()
        return

    latest_resume = files[0]

    resume_path = os.path.abspath(
        os.path.join(resume_folder, latest_resume)
    )

    print("Uploading:", resume_path)

    upload_btn.send_keys(resume_path)

    time.sleep(5)

    print("Resume updated successfully!")

    driver.quit()


if __name__ == "__main__":
    update_resume()