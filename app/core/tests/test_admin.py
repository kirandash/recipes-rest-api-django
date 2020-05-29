# test client will allow us to make test requests to django admin
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
# reverse allows us to generate urls for our django admin page
from django.urls import reverse


class AdminSiteTests(TestCase):
    # set up fn: to run before running any other tests in the class
    def setUp(self):
        # setting up test client
        self.client = Client()
        # setting up admin
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@bgwebagency.com',
            password='password123'
        )
        # force login to test client with admin_user, to avoid manual login
        self.client.force_login(self.admin_user)
        # setting up a user
        self.user = get_user_model().objects.create_user(
            email='test@bgwebagency.com',
            password='password123',
            name='Test user full name'
        )

    def test_users_listed(self):
        """Test that users are listed on the user page"""
        # reverse will generate url for us
        url = reverse('admin:core_user_changelist')
        # http call from test client's helper method get
        res = self.client.get(url)

        # checks if response content contains user name and email + status 200
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Test that the user edit page works"""
        # generate url with reverse
        url = reverse('admin:core_user_change', args=[self.user.id])
        # /admin/core/user/1
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
