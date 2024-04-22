import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import psycopg2
import random

class TestLogin(unittest.TestCase):

    def setUp(self):
        # Replace 'chromedriver' with the path to your WebDriver executable
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8097/admin_manage')

        username_input_login = self.driver.find_element(By.ID, 'username')
        password_input_login = self.driver.find_element(By.ID, 'password')
        submit_button_login = self.driver.find_element(By.ID, 'submit')

        username_input_login.send_keys('admin')
        password_input_login.send_keys('admin')
        submit_button_login.click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'dashboard'))
        )

        manage_users_link = self.driver.find_element(By.CLASS_NAME, 'manage-users')

        manage_users_link.click()

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'page-title'))
        )

    def test_create_new_user_without_username(self):
        # Click the button to show the create new user form
        new_user_button = self.driver.find_element(By.CLASS_NAME, 'create-new-user')
        new_user_button.click()

        # Wait for the form elements to become visible
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'new-username'))
        )

        # Find the username and password input fields, and submit button
        password_input = self.driver.find_element(By.ID, 'new-password')
        submit_button = self.driver.find_element(By.ID, 'new-submit')

        # Enter a password without a username
        password_input.send_keys('password')
        submit_button.click()

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'newusernameError'))
        )

        # Check if the username error message is displayed
        error_message = self.driver.find_element(By.ID, 'newusernameError')
        self.assertTrue('Please enter a username.' in error_message.text)

    def test_create_new_user_without_password(self):
    # Click the button to show the create new user form
        new_user_button = self.driver.find_element(By.CLASS_NAME, 'create-new-user')
        new_user_button.click()

        # Wait for the form elements to become visible
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'new-username'))
        )

        # Find the username and password input fields, and submit button
        username_input = self.driver.find_element(By.ID, 'new-username')
        password_input = self.driver.find_element(By.ID, 'new-password')
        submit_button = self.driver.find_element(By.ID, 'new-submit')

        # Clear the password field first (in case it contains any default value)
        password_input.clear()

        # Enter a username without a password
        username_input.send_keys('vasu')
        submit_button.click()

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'newpasswordError'))
        )

        # Check if the password error message is displayed
        error_message = self.driver.find_element(By.ID, 'newpasswordError')
        self.assertTrue('Please enter a password.' in error_message.text)

    def test_update_new_user_without_type(self):
        update_user_button = self.driver.find_element(By.CLASS_NAME, 'update-user')
        update_user_button.click()

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'update-role-selection'))
        )

        update_role_selection_button = self.driver.find_element(By.ID, 'update-role-selection')
        update_role_selection_button.click()

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'roleToUpdateError'))
        )

        error_message = self.driver.find_element(By.ID, 'roleToUpdateError')
        self.assertTrue('Please select a role to update.' in error_message.text)

    def test_update_new_user_without_username(self):
        update_user_button = self.driver.find_element(By.CLASS_NAME, 'update-user')
        update_user_button.click()

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'update-role-selection'))
        )

        selection_list_id = "roleToUpdate"
        # Select role as "developer" from the dropdown
        role_to_update = Select(self.driver.find_element(By.ID, selection_list_id))
        role_to_update.select_by_value('developer')

        update_role_selection_button = self.driver.find_element(By.ID, 'update-role-selection')
        update_role_selection_button.click()

        user_to_update = Select(self.driver.find_element(By.ID, 'usernameToUpdate'))
        user_to_update.select_by_visible_text('Select User')  # Assuming the first user in the list

        new_role_selection = Select(self.driver.find_element(By.ID, 'update_new_role'))
        new_role_selection.select_by_visible_text('user')

        update_submit_button = self.driver.find_element(By.ID, 'update-submit')
        update_submit_button.click()

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'usernameToUpdateError'))
        )

        error_message = self.driver.find_element(By.ID, 'usernameToUpdateError')
        self.assertTrue('Please select a user to update.' in error_message.text)

    def test_update_new_user_without_new_role(self):
        update_user_button = self.driver.find_element(By.CLASS_NAME, 'update-user')
        update_user_button.click()

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'update-role-selection'))
        )

        selection_list_id = "roleToUpdate"
        role_to_update = Select(self.driver.find_element(By.ID, selection_list_id))
        role_to_update.select_by_value('developer')

        # Click the update role selection button
        update_role_selection_button = self.driver.find_element(By.ID, 'update-role-selection')
        update_role_selection_button.click()

        # Select the user to update
        user_to_update = Select(self.driver.find_element(By.ID, 'usernameToUpdate'))
        user_to_update.select_by_index(1)  # Assuming the first user in the list

        # Clear the new role selection (if any)
        new_role_selection = Select(self.driver.find_element(By.ID, 'update_new_role'))
        new_role_selection.select_by_visible_text('Select Role')
        time.sleep(2)

        # Click the update submit button
        update_submit_button = self.driver.find_element(By.ID, 'update-submit')
        update_submit_button.click()
        time.sleep(2)

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'newRoleError'))
        )

        # Check if the new role error message is displayed
        error_message = self.driver.find_element(By.ID, 'newRoleError')
        self.assertTrue('Please select a new role.' in error_message.text)

    def test_delete_user_without_selecting_user(self):
        delete_user_button = self.driver.find_element(By.CLASS_NAME, 'delete-user')
        delete_user_button.click()

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'submit-delete'))
        )

        delete_role_selection_button = self.driver.find_element(By.ID, "submit-delete")
        delete_role_selection_button.click()

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'delete-user-error'))
        )

        error_message = self.driver.find_element(By.ID, 'delete-user-error')
        self.assertTrue('Please select at least one user to delete.' in error_message.text)


    def tearDown(self):
        self.driver.quit()
    