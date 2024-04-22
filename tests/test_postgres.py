import unittest
import psycopg2
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class TestUserManagement(unittest.TestCase):

    def setUp(self):
        # Set up database connection
        self.conn = psycopg2.connect(
            dbname="mydatabase",
            user="postgres",
            password="postgres",
            host="db",
            port=5432
        )
        self.cur = self.conn.cursor()

        # Set up Selenium WebDriver
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8097/login')

    def test_login_successful(self):
        ''' Tests successful login against database records '''
        username = "user1"
        password = "user1"  # Assume this is the correct password for the user

        # Navigate to the login page and wait for input fields to be available
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
        self.driver.find_element(By.ID, 'username').send_keys(username)
        self.driver.find_element(By.ID, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//*[@id="submit"]').click()

        # Wait for the "Welcome, Admin!" message to ensure login was successful
        welcome_message = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Welcome!')]"))
        )
        self.assertTrue(welcome_message.is_displayed(), "Welcome message is not displayed.")

        # Verify in the database
        self.cur.execute("SELECT username FROM usersdata WHERE username = %s", (username,))
        last_login = self.cur.fetchone()
        self.assertIsNotNone(last_login, "Database check for last login failed.")


    def test_create_new_user(self):
        ''' Tests creating a new user and checks the database for record creation '''
        self.driver.get('http://localhost:8097/manage_users')

        # Using time to generate a unique username
        username = "new_user_" + str(time.time())
        password = "new_password"
        
        # Click the manage users button
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'create-new-user'))
        )
        manage_users_button = self.driver.find_element(By.CLASS_NAME, 'create-new-user')
        manage_users_button.click()
        
        # Enter username in the username input field
        username_input = self.driver.find_element(By.ID, 'new-username')
        password_input = self.driver.find_element(By.ID, 'new-password')
        submit_button = self.driver.find_element(By.ID, 'new-submit')
        username_input.send_keys(username)
        # Enter password
        password_input.send_keys(password)
        
        # Submit the form
        submit_button.click()

        self.cur.execute("SELECT username FROM usersdata WHERE username = %s", (username,))
        db_username = self.cur.fetchone()
        self.assertIsNotNone(db_username)
        self.assertEqual(db_username[0], username)


    def test_update_user_role(self):
        ''' Tests updating an existing user's role and verifies it in the database '''
        username = "rishabh"
        self.driver.get('http://localhost:8097/manage_users')

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'update-user'))
        )
        manage_users_button = self.driver.find_element(By.CLASS_NAME, 'update-user')
        manage_users_button.click()

        # Wait for the dropdown to be visible and interactable
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'roleToUpdate'))
        )
        user_select_dropdown = self.driver.find_element(By.ID, 'roleToUpdate')
        user_select_dropdown.send_keys('user')
        
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="updateForm"]/button'))
        )
        select_role_button = self.driver.find_element(By.XPATH, '//*[@id="updateForm"]/button')
        select_role_button.click()
        
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'usernameToUpdate'))
        )
        user_select_dropdown = self.driver.find_element(By.ID, 'usernameToUpdate')
        user_select_dropdown.send_keys(username)
        time.sleep(5)
        
        element = self.driver.find_element(By.XPATH, '//*[@id="roleToUpdate"]')
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        user_select_dropdown = self.driver.find_element(By.XPATH, '//*[@id="roleToUpdate"]')
        user_select_dropdown.send_keys('admin')
        time.sleep(2)
        
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/form[3]/input[2]'))
        )
        select_role_button = self.driver.find_element(By.XPATH, '/html/body/form[3]/input[2]')
        select_role_button.click()
        

        # Verify in the database
        self.cur.execute("SELECT role FROM usersdata WHERE username = %s", (username,))
        updated_role = self.cur.fetchone()[0]
        self.assertEqual(updated_role, 'admin')

    def tearDown(self):
        self.driver.quit()
        self.cur.close()
        self.conn.close()

if __name__ == '__main__':
    unittest.main()
