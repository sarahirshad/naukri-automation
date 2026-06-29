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
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    wait = WebDriverWait(driver, 30)

    try:
        # Open login page
        print("Opening Naukri login page...")
        driver.get("https://www.naukri.com/nlogin/login")

        # Wait for email field
        email_field = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[contains(@placeholder,'Enter your active Email ID')]")
            )
        )

        # Wait for password field
        password_field = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[contains(@placeholder,'Enter your password')]")
            )
        )

        print("Entering credentials...")
        email_field.send_keys(EMAIL)
        password_field.send_keys(PASSWORD)

        # Click login
        login_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(),'Login')]")
            )
        )

        print("Logging in...")
        login_btn.click()

        # Wait for profile page load
        time.sleep(5)

        print("Opening profile page...")
        driver.get("https://www.naukri.com/mnjuser/profile")

        # Wait for update button
        update_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//input[@value='Update resume']")
            )
        )

        print("Uploading resume...")
        update_btn.send_keys(os.path.abspath(resume_path))

        time.sleep(5)

        print("Resume updated successfully!")

    except Exception as e:
        print("Error occurred:", str(e))
        raise

    finally:
        driver.quit()