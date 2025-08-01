import os
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains  # Optional, but useful
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from browserstack.local import Local

# Env creds
USERNAME = os.getenv("BROWSERSTACK_USERNAME")
ACCESS_KEY = os.getenv("BROWSERSTACK_ACCESS_KEY")

if not USERNAME or not ACCESS_KEY:
    raise Exception("BROWSERSTACK_USERNAME or BROWSERSTACK_ACCESS_KEY not set in environment.")

# Enable BS Local
BROWSERSTACK_LOCAL = True

# Browser config list
browsers = [
    {
        "browserName": "chrome",
        "bstack:options": {
            "os": "Windows",
            "osVersion": "11",
            "sessionName": "Local Web Test - Chrome",
            "buildName": os.getenv("BROWSERSTACK_BUILD_NAME", "Automate Build"),
            "projectName": os.getenv("BROWSERSTACK_PROJECT_NAME", "bs-demo-cert"),
            "local": "true"
        }
    },
    {
        "browserName": "safari",
        "bstack:options": {
            "os": "OS X",
            "osVersion": "Monterey",
            "sessionName": "Local Web Test - Safari",
            "buildName": os.getenv("BROWSERSTACK_BUILD_NAME", "Automate Build"),
            "projectName": os.getenv("BROWSERSTACK_PROJECT_NAME", "bs-demo-cert"),
            "local": "true"
        }
    }
]

def start_local():
    bs_local = Local()
    bs_local_args = { "key": ACCESS_KEY }
    bs_local.start(**bs_local_args)
    print("[INFO] BrowserStackLocal is running.")
    return bs_local

def stop_local(bs_local):
    if bs_local and bs_local.isRunning():
        bs_local.stop()
        print("[INFO] BrowserStackLocal stopped.")

def mark_test_status(driver, status, reason):
    script = (
        'browserstack_executor: ' +
        json.dumps({
            'action': 'setSessionStatus',
            'arguments': {
                'status': status,
                'reason': reason
            }
        })
    )
    driver.execute_script(script)

def run_test(capabilities_dict):
    options = webdriver.ChromeOptions()
    for key in capabilities_dict:
        options.set_capability(key, capabilities_dict[key])

    executor_url = f"https://{USERNAME}:{ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"
    driver = webdriver.Remote(command_executor=executor_url, options=options)

    try:
        print("[INFO] Opening app...")
        driver.get("http://localhost:3000")
        time.sleep(2)

        # Step 1: Click "Sign In"
        driver.find_element(By.ID, "signin").click()
        time.sleep(1)

        # Wait helper
        wait = WebDriverWait(driver, 10)

        # --- Select Username ---
        username_field = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Select Username')]"))
        )
        username_field.click()
        time.sleep(1)

        # Select first option
        first_username_option = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "css-1n7v3ny-option"))
        )
        first_username_option.click()
        time.sleep(1)

        # --- Select Password ---
        password_field = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Select Password')]"))
        )
        password_field.click()
        time.sleep(1)

        # Select first option
        first_password_option = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "css-1n7v3ny-option"))
        )
        first_password_option.click()
        time.sleep(1)

        # Step 4: Click "Log In"
        driver.find_element(By.ID, "login-btn").click()
        time.sleep(2)

        # Step 5: Find "iPhone 12" and click "Add to cart"
        iphone_titles = driver.find_elements(By.CLASS_NAME, "shelf-item__title")
        for idx, title in enumerate(iphone_titles):
            if "iPhone 12" in title.text:
                driver.find_elements(By.CLASS_NAME, "shelf-item__buy-btn")[idx].click()
                break
        time.sleep(1)

        # Step 6: Click "Checkout"
        driver.find_element(By.CLASS_NAME, "buy-btn").click()
        time.sleep(2)

        mark_test_status(driver, "passed", "Cart flow completed successfully.")
    except Exception as e:
        print(f"[ERROR] Test failed: {e}")
        mark_test_status(driver, "failed", str(e))
        raise
    finally:
        driver.quit()

# MAIN
if __name__ == "__main__":
    bs_local = start_local() if BROWSERSTACK_LOCAL else None
    time.sleep(2)  # Optional buffer for local tunnel
    try:
        for caps in browsers:
            run_test(caps)
    finally:
        stop_local(bs_local)
