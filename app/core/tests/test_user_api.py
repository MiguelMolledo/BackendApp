from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublishUsersApiTest(TestCase):
    """
    Test the users Api (Public)
    """

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """
        Test creating user with valid payload is successful
        :return:
        """

        payload = {
            'email': "testemail@gmail.com",
            'password': 'testpass',
            'name': "Test Name"
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload.get("password")))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """
        Test to check if the user already exists
        :return:
        """

        payload = {
            'email': "testemail@gmail.com",
            'password': 'testpass',
            'name': "Test Name"
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """
        Test that the password must be more than 5 characters
        :return:
        """
        payload = {
            'email': "testemail@gmail.com",
            'password': '123',
            'name': "Test Name"
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload["email"]).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that a token is created for the User"""
        payload = {
            'email':'testemail@gmail.com',
            'password':"testpass"
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        payload = {'email':'testemail@gmail.com','password':'testpassword'}
        create_user(**payload)
        payload['password'] = 'wrongpassword'
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user doesnt exist"""
        payload = {'email':'testemail@gmail.com','password':'testpassword'}
        res = self.client.post(TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_create_token_missing_fields(self):
        """test that email and password are required"""
        payload = {'email': 'testemail@gmail.com', 'password': ' '}
        res = self.client.post(TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)


