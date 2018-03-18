"""
    User test Class
"""
import unittest
import uuid
# from api import APP
from flask import json
from api.models.user import User
from api.models.business import Business
from api.helpers import get_token
from tests.api_tests import MainTests


class UserTests(MainTests):

    def test_registration(self):
        '''
            Testing registration
        '''
        response = self.app.post(self.url_prefix + 'auth/register', data=json.dumps({
            'username': self.exist_user['username'],
            'email': self.exist_user['email'],
            'password': self.exist_user['password'],
            'confirm_password': self.exist_user['confirm_password']
        }), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'have been successfully registered', response.data)

    def test_exist_email(self):
        '''
            Testing registration with exist email
        '''
        response = self.app.post(self.url_prefix + 'auth/register', data=json.dumps({
            'username': self.exist_user['username'],
            'email': self.sample_user['email'],
            'password': self.exist_user['password'],
            'confirm_password': self.exist_user['confirm_password']
        }), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Sorry the email address has been taken', response.data)

    def test_wrong_registration(self):
        """
            Test registration with incomplete data
        """
        response = self.app.post(self.url_prefix + 'auth/register', data=json.dumps({
            'username': 'dummy name',
            'confirm_password': self.exist_user['confirm_password']
        }), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Please provide', response.data)

    def test_login(self):
        """
            Testing login
        """
        response = self.app.post(self.url_prefix + 'auth/login', data=json.dumps({
            'email': self.sample_user['email'],
            'password': self.sample_user['password']
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'successfully logged', response.data)

    def test_invalid_password(self):
        """
            Testing for invalid password
        """
        response = self.app.post(self.url_prefix + 'auth/login', data=json.dumps({
            'email': self.sample_user['email'],
            'password': 'anyinvalidpassword'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertIn(b'Invalid password', response.data)

    def test_invalid_credentials(self):
        """
            Testing for invalid credentials
        """
        response = self.app.post(self.url_prefix + 'auth/login', data=json.dumps({
            'email': 'anyemail',
            'password': 'anyinvalidpassword'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertIn(b'Invalid email or password', response.data)

    def test_incomplete_creds(self):
        """
            Test registration with incomplete data
        """
        response = self.app.post(self.url_prefix + 'auth/login', data=json.dumps({
            'email': 'dummy@dummy.com',
        }), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Please provide', response.data)

    def test_logout(self):
        """
            Test Logout
        """
        response = self.app.post(self.url_prefix + 'auth/logout',
                                 data={}, headers={'Authorization': self.test_token})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You have successfully logged out', response.data)

    def test_password_reset(self):
        """
            Testing password Reset
        """
        response = self.app.post(self.url_prefix + 'auth/reset-password', data=json.dumps({
            'old_password': self.sample_user['password'],  # Old password
            'new_password': '123456',
        }), content_type='application/json',
            headers={'Authorization': self.test_token})
        self.assertEqual(response.status_code, 201)
        self.assertIn(
            b'You have successfully changed your password', response.data)

    def test_valid_token(self):
        """
            Testing valid token
        """
        # Test invalid token by accessing protected endpoint with invalid
        # authorization token
        response = self.app.post(self.url_prefix + 'auth/reset-password', data={
            'old_password': self.sample_user['password'],  # Old password
            'new_password': '123456',
        },
            headers={'Authorization': 'eyJhbGciOQxYI-vmeqW6s1hqaC3OrXuii_D8mK2lpEcDn7g'})
        self.assertEqual(response.status_code, 401)
        self.assertIn(
            b'Unauthorized', response.data)

    def test_expired_token(self):
        """
            Testing Expired token
        """
        # Test expired token by accessing protected endpoint with expired token
        response = self.app.post(self.url_prefix + 'auth/reset-password', data={
            'old_password': self.sample_user['password'],  # Old password
            'new_password': '123456',
        },
            headers={'Authorization': self.expired_test_token})
        self.assertEqual(response.status_code, 401)
        self.assertIn(
            b'Unauthorized', response.data)