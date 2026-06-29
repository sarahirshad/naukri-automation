import os
import time
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()

EMAIL = os.getenv("NAUKRI_EMAIL")
PASSWORD = os.getenv("NAUKRI_PASSWORD")


def update_resume(resume_path):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    wait = WebDriverWait(driver, 30)

    try:
        print("Opening Naukri login page...")
        driver.get("https://www.naukri.com/nlogin/login")

        time.sleep(10)

        print("Current URL:", driver.current_url)
        print("Page title:", driver.title)

        # Save screenshot for debugging
        driver.save_screenshot("debug.png")
        print("Screenshot saved")

        email_field = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@type='text']")
            )
        )

        password_field = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@type='password']")
            )
        )

        email_field.send_keys(EMAIL)
        password_field.send_keys(PASSWORD)

        login_btn = driver.find_element(
            By.XPATH, "//button[contains(text(),'Login')]"
        )
        login_btn.click()

        time.sleep(5)

        driver.get("https://www.naukri.com/mnjuser/profile")

        upload_btn = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@type='file']")
            )
        )

        upload_btn.send_keys(os.path.abspath(resume_path))

        time.sleep(5)

        print("Resume updated successfully!")

    finally:
        driver.quit()