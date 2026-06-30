import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


EMAIL = os.getenv("NAUKRI_EMAIL")
PASSWORD = os.getenv("NAUKRI_PASSWORD")


def update_resume(resume_path):
    print("Opening Naukri login page...")

    options = Options()
    options.binary_location = "/usr/bin/google-chrome"

    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    wait = WebDriverWait(driver, 30)

    try:
        driver.get("https://www.naukri.com/nlogin/login")
        print("Current URL:", driver.current_url)
        print("Page title:", driver.title)

        # Email field
        email_field = wait.until(
            EC.presence_of_element_located((By.XPATH, '//input[contains(@placeholder,"Enter your active Email ID")]'))
        )
        email_field.send_keys(EMAIL)

        # Password field
        password_field = wait.until(
            EC.presence_of_element_located((By.XPATH, '//input[contains(@placeholder,"Enter your password")]'))
        )
        password_field.send_keys(PASSWORD)

        # Login button
        login_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(),"Login")]'))
        )
        login_button.click()

        print("Logged in successfully")
        time.sleep(5)

        # Profile page
        driver.get("https://www.naukri.com/mnjuser/profile")
        time.sleep(5)

        # Upload button
        upload_input = wait.until(
            EC.presence_of_element_located((By.XPATH, '//input[@type="file"]'))
        )

        upload_input.send_keys(os.path.abspath(resume_path))

        print("Resume uploaded successfully")
        time.sleep(5)

    except Exception as e:
        print("Error occurred:", e)
        driver.save_screenshot("error.png")
        print("Screenshot saved: error.png")
        raise

    finally:
        driver.quit()