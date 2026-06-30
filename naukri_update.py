import os
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


EMAIL = os.getenv("NAUKRI_EMAIL")
PASSWORD = os.getenv("NAUKRI_PASSWORD")


def update_resume(resume_path):
    print("Opening Naukri login page...")

    options = uc.ChromeOptions()

    options.binary_location = "/usr/bin/chromium"

    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver = uc.Chrome(
        options=options,
        version_main=None
    )

    wait = WebDriverWait(driver, 40)

    try:
        # Open login page
        driver.get("https://www.naukri.com/nlogin/login")

        print("Current URL:", driver.current_url)
        print("Page title:", driver.title)

        time.sleep(5)

        # Email field
        email_field = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//input[@type="text"]')
            )
        )
        email_field.clear()
        email_field.send_keys(EMAIL)

        print("Email entered")

        # Password field
        password_field = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//input[@type="password"]')
            )
        )
        password_field.clear()
        password_field.send_keys(PASSWORD)

        print("Password entered")

        # Login button
        login_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//button[@type="submit"]')
            )
        )
        login_button.click()

        print("Login clicked")

        time.sleep(8)

        print("After login URL:", driver.current_url)

        # Open profile page
        driver.get("https://www.naukri.com/mnjuser/profile")

        time.sleep(8)

        print("Profile page opened")

        # Upload input
        upload_input = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//input[@type="file"]')
            )
        )

        upload_input.send_keys(os.path.abspath(resume_path))

        print("Resume uploaded successfully")

        time.sleep(5)

    except Exception as e:
        print("Error occurred:", str(e))
        driver.save_screenshot("error.png")
        print("Screenshot saved: error.png")
        raise

    finally:
        driver.quit()