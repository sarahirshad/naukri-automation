import os
import time
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


load_dotenv()

EMAIL = os.getenv("NAUKRI_EMAIL")
PASSWORD = os.getenv("NAUKRI_PASSWORD")


def update_resume(resume_path):
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    try:
        print("Opening Naukri login page...")

        driver.get("https://www.naukri.com/nlogin/login")

        time.sleep(3)

        driver.find_element(By.ID, "usernameField").send_keys(EMAIL)
        driver.find_element(By.ID, "passwordField").send_keys(PASSWORD)

        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        print("Logged in...")

        time.sleep(5)

        driver.get("https://www.naukri.com/mnjuser/profile")

        time.sleep(5)

        upload_btn = driver.find_element(
            By.XPATH,
            "//input[@type='file']"
        )

        print(f"Uploading: {resume_path}")

        upload_btn.send_keys(os.path.abspath(resume_path))

        time.sleep(10)

        print("Upload completed.")

    finally:
        driver.quit()   