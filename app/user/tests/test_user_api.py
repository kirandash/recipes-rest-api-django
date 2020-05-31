from django.test import TestCase
# auth user model
from django.contrib.auth import get_user_model
# reverse: for generating api url
from django.urls import reverse

# rest framework helper tools
# mock REST API client
from rest_framework.test import APIClient
# module with status codes in human readable format for status codes
from rest_framework import status

# Generate user/create url and assign to variable
CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


# create a short hand fn for create_user from get_user_model
# ** stands for dynamic variable
def create_user(**params):
    return get_user_model().objects.create_user(**params)


# Unauthenticated User API endpoints test cases
class PublicUserApiTests(TestCase):
    """Test the users API (public)"""

    # set up tasks to run before each test in the class
    def setUp(self):
        # set up mock API client. So, no need to set up with each fn
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            'email': 'test@bgwebagency.com',
            'password': 'django1234',
            'name': 'Tester Dash'
        }
        # post call to user url
        res = self.client.post(CREATE_USER_URL, payload)

        # check status code for 201 created
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # check if user is created in model
        user = get_user_model().objects.get(**res.data)
        # check if password matches
        self.assertTrue(user.check_password(payload['password']))
        # check if password is not returned in the user response - security
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creating a user that already exists fails"""
        payload = {'email': 'test@bgwebagency.com', 'password': 'django1234'}
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        # check status code for 400 bad request
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be more than 5 characters"""
        payload = {'email': 'test@bgwebagency.com', 'password': 'kk'}

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        # will return True/False based on the filter and .exists check
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        payload = {'email': 'test@bgwebagency.com', 'password': 'django1234'}
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        # check if token exists in response
        self.assertIn('token', res.data)
        # No need to test if token works, since 3rd party, trust rest_framework
        # just check if status code is ok
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        create_user(email='test@bgwebagency.com', password='django1234')
        payload = {'email': 'test@bgwebagency.com', 'password': '1234django'}
        res = self.client.post(TOKEN_URL, payload)

        # Check that token is not returned in response
        self.assertNotIn('token', res.data)
        # check status code is 400
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user does not exist"""
        payload = {'email': 'test@bgwebagency.com', 'password': 'django1234'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test that authentication is required for users"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserAPITests(TestCase):
    """Test API requests that require Authentication"""

    # set up tasks to run before each test in the class
    def setUp(self):
        self.user = create_user(
            email='test@bgwebagency.com',
            password='django1234',
            name='Tester Dash'
        )
        # create a reusable client
        self.client = APIClient()
        # authenticate with mock api client using dummy user
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user"""
        res = self.client.get(ME_URL)

        # check if retrieve is success with status code 200
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # check if response data has same name and email & not password
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email
        })

    def test_post_not_allowed(self):
        """Test that post is not allowed on the me url"""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for authenticated user"""
        payload = {'name': 'new name', 'password': 'newdjango1234'}

        res = self.client.patch(ME_URL, payload)

        # refresh_from_db helper fn to update user with latest value from db
        self.user.refresh_from_db()

        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
