from django.test import TestCase, Client
from django.contrib.auth import  get_user_model

from django.urls import reverse
class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="test@gmail.com",
            password= 'password1234'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email="testAdmin_@gmail.com",
            password='Admin_password1234',
            name = " Miguel Molledo"

        )

    def test_users_listed(self):
        """
        Test that users are listed on user Page
        :return:
        """

        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """
        Test that user edit page works
        :return:
        """
        #/admin/core/user/1
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)


    def test_create_user_page(self):
        """
        Test that the create user page works
        :return:
        """

        url = reverse('admin:core_user_add')
        rest = self.client.get(url)
        self.assertEqual(rest.status_code, 200)