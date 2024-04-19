import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class TestAdminDashboard(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:8097/login")  

        username_input = self.driver.find_element(By.ID, 'username')
        password_input = self.driver.find_element(By.ID, 'password')
        submit_button = self.driver.find_element(By.ID, 'submit')

        username_input.send_keys('admin')
        password_input.send_keys('admin')
        submit_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'dashboard'))
        )

    def test_admin_dashboard_visibility(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'welcome-message'))
        )
        success_message = self.driver.find_element(By.CLASS_NAME, 'welcome-message')
        self.assertTrue('Welcome, Admin!' in success_message.text)

    def test_click_profile_management_link(self):
        # Find the link for 'Profile Management' by its class name
        profile_management_link = self.driver.find_element(By.CLASS_NAME, 'profile-management')

        # Click on the 'Profile Management' link
        profile_management_link.click()

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'page-title'))
        )
        success_message = self.driver.find_element(By.CLASS_NAME, 'page-title')
        self.assertTrue('Profile Management Page' in success_message.text)

    def test_click_view_notifications_link(self):
        # Find the link for 'View Notifications' by its class name
        view_notifications_link = self.driver.find_element(By.CLASS_NAME, 'view-notifications')

        # Click on the 'View Notifications' link
        view_notifications_link.click()

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'page-title'))
        )
        success_message = self.driver.find_element(By.CLASS_NAME, 'page-title')
        self.assertTrue('View Notifications' in success_message.text)  

    def test_debug_logs_link(self):
        # Find the link for 'Debug Logs' by its class name
        debug_logs_link = self.driver.find_element(By.CLASS_NAME, 'debug-logs')

        # Click on the 'Debug Logs' link
        debug_logs_link.click()

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'page-title'))
        )
        success_message = self.driver.find_element(By.CLASS_NAME, 'page-title')
        self.assertTrue('Debug Logs' in success_message.text)

    def test_manage_users_link(self):
        # Find the link for 'Manage Users' by its class name
        manage_users_link = self.driver.find_element(By.CLASS_NAME, 'manage-users')

        # Click on the 'Manage Users' link
        manage_users_link.click()

        self.assertIn('Assign Roles', self.driver.title)
        

    def test_click_system_settings_link(self):
        # Find the link for 'System Settings' by its class name
        system_settings_link = self.driver.find_element(By.CLASS_NAME, 'system-settings')

        # Click on the 'System Settings' link
        system_settings_link.click()

        # Wait for the page title to be visible
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'page-title')))

        # Assert that the page title contains 'System Settings'
        success_message = self.driver.find_element(By.CLASS_NAME, 'page-title')
        self.assertIn('System Settings', success_message.text)


    def test_view_reports_link(self):
        # Find the link for 'View Reports' by its class name
        view_reports_link = self.driver.find_element(By.CLASS_NAME, 'view-reports')

        # Click on the 'View Reports' link
        view_reports_link.click()

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'page-title'))
        )
        success_message = self.driver.find_element(By.CLASS_NAME, 'page-title')
        self.assertTrue('View Reports' in success_message.text)
        

    def tearDown(self):
        self.driver.quit()
