import os
import time
import random
import undetected_chromedriver as uc
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


EMAIL = os.getenv("NAUKRI_EMAIL")
PASSWORD = os.getenv("NAUKRI_PASSWORD")


def human_type(element, text):
    for ch in text:
        element.send_keys(ch)
        time.sleep(random.uniform(0.1, 0.3))


def random_wait(a=2, b=5):
    time.sleep(random.uniform(a, b))


def update_resume(resume_path):
    print("Opening Naukri login page...")

    ua = UserAgent()

    options = uc.ChromeOptions()
    options.binary_location = "/usr/bin/chromium"

    options.add_argument(f"--user-agent={ua.random}")
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver = uc.Chrome(
        options=options,
        driver_executable_path="/usr/bin/chromedriver",
        use_subprocess=False
    )

    wait = WebDriverWait(driver, 30)

    try:
        driver.get("https://www.naukri.com/nlogin/login")

        print("Current URL:", driver.current_url)
        print("Page title:", driver.title)

        random_wait(3, 6)

        # Random scroll like human
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3)")
        random_wait(1, 3)

        # Email field
        email_field = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//input[contains(@placeholder,"Enter your active Email ID")]')
            )
        )
        human_type(email_field, EMAIL)

        random_wait(1, 2)

        # Password field
        password_field = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//input[contains(@placeholder,"Enter your password")]')
            )
        )
        human_type(password_field, PASSWORD)

        random_wait(1, 3)

        # Login button
        login_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//button[contains(text(),"Login")]')
            )
        )
        login_button.click()

        print("Logged in successfully")
        random_wait(5, 8)

        # Profile page
        driver.get("https://www.naukri.com/mnjuser/profile")
        random_wait(5, 8)

        # Upload resume
        upload_input = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//input[@type="file"]')
            )
        )

        upload_input.send_keys(os.path.abspath(resume_path))

        print("Resume uploaded successfully")
        random_wait(5, 8)

    except Exception as e:
        print("Error occurred:", e)
        driver.save_screenshot("error.png")
        print("Screenshot saved: error.png")
        raise

    finally:
        driver.quit()