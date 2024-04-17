import unittest
import psycopg2
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import random

class TestLogin(unittest.TestCase):

    def setUp(self):
        dbname="mydatabase"  
        user="postgres"   
        password="admin"     
        host="localhost"     

        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host
        )

        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8097/login')


    def test_postgres_connection(self):
        '''Check if the connection to the PostgreSQL server is successful.'''
        
        self.assertIsNotNone(self.conn)

    def test_login_with_invalid_credentials(self):
        # Fill in the login form with valid credentials
        username_input = self.driver.find_element(By.ID, 'username')
        password_input = self.driver.find_element(By.ID, 'password')
        submit_button = self.driver.find_element(By.ID, 'submit')

        random_password = str(random.randint(1000, 9999))

        username_input.send_keys('user1')
        password_input.send_keys(random_password)
        submit_button.click()
        time.sleep(2)

        # Wait until the success message is displayed
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'AuthenticationError'))
        )

        # Check if the success message is displayed
        error_message = self.driver.find_element(By.CLASS_NAME, 'AuthenticationError')
        self.assertTrue('Combination of username and password do not match.' in error_message.text)

    def tearDown(self):
        self.driver.quit()
