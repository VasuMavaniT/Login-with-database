import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import psycopg2
import random

class TestLogin(unittest.TestCase):

    def setUp(self):
        # Replace 'chromedriver' with the path to your WebDriver executable
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8097/login')

        username_input = self.driver.find_element(By.ID, 'username')
        password_input = self.driver.find_element(By.ID, 'password')
        submit_button = self.driver.find_element(By.ID, 'submit')

        username_input.send_keys('admin')
        password_input.send_keys('admin')
        submit_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'dashboard'))
        )

        manage_users_link = self.driver.find_element(By.CLASS_NAME, 'manage-users')

        manage_users_link.click()

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'page-title'))
        )

    def tearDown(self):
        self.driver.quit()
    