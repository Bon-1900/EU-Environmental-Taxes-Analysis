"""Contributers: Yuansheng zhang"""

from my_app.models import User
import time

class TestMyApp:
    def test_index_page_valid( self, client ):
        """
        GIVEN a Flask application is running
        WHEN the '/' home page is requested (GET)
        THEN check the response is valid
        """
        response = client.get( '/' )
        assert response.status_code == 200

    def test_profile_not_allowed_when_user_not_logged_in( self, client ):
        """
        GIVEN A user is not logged
        WHEN When they access the profile menu option
        THEN they should be redirected to the login page
        """
        response = client.get( '/community/profile', follow_redirects=True )
        assert response.status_code == 200
        assert b'Password' in response.data

    def test_signup_succeeds( self, client ):
        """
            GIVEN A user is not registered
            WHEN they submit a valid registration form
            THEN the should be redirected to a page with a custom welcome message and there should be an
            additional
            record in the user table in the database
            """
        count = User.query.count()
        response = client.post( '/signup/signup', data=dict(
            title = 'Mr',
            first_name='Person',
            last_name='Two',
            email='person_2@people.com',
            password='password2',
            password_repeat='password2',
            security_question='What was the name of your first pet?',
            security_answer='test_answer2'
        ), follow_redirects=True )
        count2 = User.query.count()
        assert count2 - count == 1
        assert response.status_code == 200
        assert b'Person' in response.data

    def test_log_in_with_security_question( self, client ):
        """
        GIVEN a User without profile has been created
        WHEN the user logs in with security questions
        THEN he/she is redirected to the index page
        """
        response = client.post( '/signup/forgot_password',
                     data=dict(
                         email='person1@people.com',
                         security_question='What\'s your mother\'s maiden name?',
                         security_answer= 'test_answer1'
                     ), follow_redirects=True )
        assert response.status_code == 200
        assert b'EU environmental taxes analysis' in response.data

    def test_log_in_for_user_with_profile( self, client ):
        """
        GIVEN a User without profile has been created
        WHEN the user logs in with security questions
        THEN he/she is redirected to the index page
        """
        response = client.post( '/signup/login',
                     data=dict(
                         email='person3@people.com',
                         password='password3',
                         remember=False
                     ), follow_redirects=True )
        assert response.status_code == 200
        assert b'SELECT CHART' in response.data

    def test_log_in_with_wrong_email( self, client ):
        """
        GIVEN a User has been created
        WHEN the user logs in with the wrong email address
        THEN an error message should be displayed on the login form ('No account found with that email address.')
        """
        response = client.post( '/signup/login',
                                data=dict(
                                    email='non_existing_password@test.com',
                                    password='non_existing_password',
                                    remember=False
                                ), follow_redirects=True )
        assert b'The email address indicated is not registered' in response.data

    def test_log_in_with_wrong_password( self, client ):
        '''
        GIVEN a User has been created
        WHEN the user logs in with the wrong password
        THEN then an error message should be displayed on the login form
        '''
        response = client.post( '/signup/login',
                                data=dict(
                                    email='person1@people.com',
                                    password='non_existing_password',
                                    remember=False
                                ), follow_redirects=True )
        assert b'The password is not valid' in response.data

    def test_option_to_log_in( self, client ):
        '''
        GIVEN a User logged out
        WHEN they access the navigation bar
        THEN there should be an option to login in
        '''
        response = client.get( '/signup/logout', follow_redirects=True )
        assert b'Login' in response.data

    def test_remember_me_within_60_sec( self, client, app ):
        '''
        GIVEN a User is logged in and selected Remember Me
        WHEN they close the browser and re-open it within 60 seconds
        THEN they should remain logged in
        '''
        client.post( '/signup/login',
                                data=dict(
                                    email='person1@people.com',
                                    password='password1',
                                    remember=True
                                ), follow_redirects=True )
        app.reset()
        time.sleep(30)
        response = client.get( '/' )
        assert b'Logout' in response.data

    def test_remember_me_after_60_sec( self, client, app ):
        '''
        GIVEN a User is logged in and selected Remember Me
        WHEN they close the browser and re-open after 60 seconds
        THEN they should be required to login again to access any protected pages (such as community home)
        '''
        client.post( '/signup/login',
                                data=dict(
                                    email='person1@people.com',
                                    password='password1',
                                    remember=True
                                ), follow_redirects=True )
        app.reset()
        time.sleep(70)
        response = client.get( '/' )
        assert b'Login' in response.data
