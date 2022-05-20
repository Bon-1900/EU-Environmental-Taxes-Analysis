"""Contributers: Yuansheng zhang"""

import pytest


@pytest.mark.usefixtures('chrome_driver', 'run_app')
class TestMyAppBrowser:
    def test_app_is_running(self, app):
        self.driver.implicitly_wait(10)
        self.driver.get("http://127.0.0.1:5000/")
        assert self.driver.title == 'Home page'

    def test_signup_succeeds(self):
        """
        Test that a user can create an account using the signup form if all fields are filled out correctly,
        and that they are redirected to the index page.
        """

        # Click signup menu link
        self.driver.find_element_by_id("signup-nav").click()
        self.driver.implicitly_wait(10)

        # Test person data
        first_name = "Person"
        last_name = "One"
        email = "person1@people.com"
        password = "password1"
        password_repeat = "password1"
        security_answer = 'test_answer1'

        # Fill in registration form
        self.driver.find_element_by_id("first_name").send_keys(first_name)
        self.driver.find_element_by_id("last_name").send_keys(last_name)
        self.driver.find_element_by_id("email").send_keys(email)
        self.driver.find_element_by_id("password").send_keys(password)
        self.driver.find_element_by_id("password_repeat").send_keys(password_repeat)
        self.driver.find_element_by_id("security_answer").send_keys(security_answer)
        self.driver.find_element_by_id("submit").click()
        self.driver.implicitly_wait(10)

        # Assert that browser redirects to index page
        assert self.driver.current_url == 'http://127.0.0.1:5000/'

        # Assert success message is flashed on the index page
        message = self.driver.find_element_by_class_name("list-unstyled").find_element_by_tag_name("li").text
        assert f"Hello, {first_name} {last_name}. You are signed up." in message

    def test_login_succeeds( self ):
        """
        Test that the user can log in
        """
        self.driver.find_element_by_id("login-nav").click()
        self.driver.implicitly_wait(10)

        email = "person1@people.com"
        password = "password1"

        self.driver.find_element_by_id( "email" ).send_keys( email )
        self.driver.find_element_by_id( "password" ).send_keys( password )
        self.driver.find_element_by_id( "submit" ).click()
        self.driver.implicitly_wait( 10 )

        assert self.driver.current_url == 'http://127.0.0.1:5000/Person'
        message = self.driver.find_element_by_class_name( "navbar-nav" ).find_element_by_tag_name( "a" ).text
        assert f"Logout" in message

    def test_logout( self ):
        """
        Test that the user can log out when logged in
        """
        self.driver.find_element_by_id( "logout-nav" ).click()
        assert self.driver.current_url == 'http://127.0.0.1:5000'
        message = self.driver.find_element_by_class_name( "navbar-nav" ).find_element_by_tag_name( "a" ).text
        assert f"Login" in message

    def test_redirecting_after_logging_in_from_community_page( self, client ):
        """
        GIVEN A user is not logged in
        WHEN When they click community and log in
        THEN they should be redirected to the community page
        """
        self.driver.find_element_by_id( "blog-nav" ).click()

        email = "person1@people.com"
        password = "password1"

        self.driver.find_element_by_id( "email" ).send_keys( email )
        self.driver.find_element_by_id( "password" ).send_keys( password )
        self.driver.find_element_by_id( "submit" ).click()
        self.driver.implicitly_wait( 10 )

        assert self.driver.current_url == 'http://127.0.0.1:5000/community/blog'
        message = self.driver.find_element_by_class_name( "blog-title" ).find_element_by_tag_name( "h1" ).text
        assert f"Welcome to the blog!" in message

