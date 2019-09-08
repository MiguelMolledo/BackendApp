from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """
        Test creating new user with an email is successful
        :return: 
        """
        email = 'testApp@gmail.com'
        password = "Testpass123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))



    def test_new_user_email_normalized(self):
        """
        Test the email for a new user is normalized
        :return: 
        """
        email = 'testapp@gMail.com'
        user = get_user_model().objects.create_user(email=email,
                                                    password='test123')
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """
        Test creating user with no email raises error
        :return: 
        """
        with self.assertRaises(ValueError):
            user = get_user_model().objects.create_user(email=None,
                                                        password='12345')


    def test_create_new_superuser(self):
        """
        Test creating new Superuser
        :return: 
        """
        user = get_user_model().objects.create_superuser(
            email="test@gmail.com",
            password='1234'
        )
        self.assertTrue(user.is_staff, True)
        self.assertTrue(user.is_superuser, True)