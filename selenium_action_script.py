from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import logging

logging.basicConfig(level=logging.INFO)

driver = webdriver.Chrome()
driver.get("https://novaivo.github.io/mockup-website-for-testing-selenium-agent/")

try:
    wait = WebDriverWait(driver, 15)

    # Login process
    login_tab = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[@class='tab active'][text()='Login']"))  # FIX: Added quotes around 'Login'
    )
    login_tab.click()

    login_email = wait.until(
        EC.presence_of_element_located((By.ID, "loginEmail"))
    )
    login_email.send_keys("your_email@gmail.com")

    login_password = wait.until(
        EC.presence_of_element_located((By.ID, "loginEmail"))  # FIX: Corrected ID to 'loginEmail'
    )
    login_password.send_keys("your_password")
    login_password.send_keys(Keys.RETURN)

    # Sign-up process
    signup_tab = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[@class='tab'][text()='Sign Up']"))  # FIX: Added quotes around 'Sign Up'
    )
    signup_tab.click()

    signup_name = wait.until(
        EC.visibility_of_element_located((By.ID, "signupName"))
    )
    signup_name.send_keys("maryamseher")

    signup_email = wait.until(
        EC.presence_of_element_located((By.ID, "signupEmail"))
    )
    signup_email.send_keys("maryamseher147@gmail.com")

    signup_password = wait.until(
        EC.presence_of_element_located((By.ID, "signupPassword"))
    )
    signup_password.send_keys("marse098")
    signup_password.send_keys(Keys.RETURN)

    logging.info("Sign-up process completed successfully")

except Exception as e:
    logging.error("Error occurred during sign-up process: {}".format(e))

finally:
    driver.quit()