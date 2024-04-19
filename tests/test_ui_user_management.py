'''
def test_create_new_user_with_username_and_password(self):
    # Click the button to show the create new user form
    new_user_button = self.driver.find_element(By.ID, 'create-new-user')
    new_user_button.click()

    # Wait for the form elements to become visible
    WebDriverWait(self.driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'new-username'))
    )

    # Find the username and password input fields, and submit button
    username_input = self.driver.find_element(By.ID, 'new-username')
    password_input = self.driver.find_element(By.ID, 'new-password')
    submit_button = self.driver.find_element(By.ID, 'new-submit')

    # Generate a random username and password
    random_username = 'user' + str(random.randint(1000, 9999))
    random_password = 'password' + str(random.randint(1000, 9999))

    # Enter the random username and password
    username_input.send_keys(random_username)
    password_input.send_keys(random_password)
    submit_button.click()

    WebDriverWait(self.driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'create-success'))
    )

    # Check if the success message is displayed
    success_message = self.driver.find_element(By.CLASS_NAME, 'create-success')
    self.assertTrue('New user is created!' in success_message.text)
'''