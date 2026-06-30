import os
import time
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


EMAIL = os.getenv("NAUKRI_EMAIL")
PASSWORD = os.getenv("NAUKRI_PASSWORD")


def human_delay(a=2, b=5):
    time.sleep(random.uniform(a, b))


def update_resume(resume_path):
    print("Opening Naukri login page...")

    options = uc.ChromeOptions()

    # Railway chromium path
    options.binary_location = "/usr/bin/chromium"

    # headless mode
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")

    # IMPORTANT FIX → force driver version same as browser
    driver = uc.Chrome(
        options=options,
        version_main=149,
        use_subprocess=True
    )

    wait = WebDriverWait(driver, 30)

    try:
        # Open login page
        driver.get("https://www.naukri.com/nlogin/login")
        print("Current URL:", driver.current_url)
        print("Page title:", driver.title)

        human_delay(3, 5)

        # Email field
        email_field = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//input[contains(@placeholder,"Enter your active Email ID")]')
            )
        )

        for char in EMAIL:
            email_field.send_keys(char)
            time.sleep(random.uniform(0.05, 0.15))

        human_delay(1, 2)

        # Password field
        password_field = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//input[contains(@placeholder,"Enter your password")]')
            )
        )

        for char in PASSWORD:
            password_field.send_keys(char)
            time.sleep(random.uniform(0.05, 0.15))

        human_delay(1, 2)

        # Login button
        login_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//button[contains(text(),"Login")]')
            )
        )

        login_button.click()
        print("Logged in successfully")

        human_delay(5, 8)

        # Go to profile page
        driver.get("https://www.naukri.com/mnjuser/profile")
        print("Navigated to profile page")

        human_delay(5, 8)

        # Upload input
        upload_input = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//input[@type="file"]')
            )
        )

        upload_input.send_keys(os.path.abspath(resume_path))

        print("Resume uploaded successfully")

        human_delay(5, 8)

    except Exception as e:
        print("Error occurred:", e)
        driver.save_screenshot("error.png")
        print("Screenshot saved: error.png")
        raise

    finally:
        driver.quit()