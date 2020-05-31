from django.test import TestCase
# always use helper fn get_user_model fn instead of importing the entire model.
# So in future if model is changed, we don't need to change all the references
from django.contrib.auth import get_user_model
from core import models


# helper fn to create a sample user
def sample_user(email='test@bgwebagency.com', password='django1234'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    def test_create_user_with_email_successsful(self):
        """Test creating a new user with an email is successful"""
        email = "test@bgwebagency.com"
        password = "testpass@123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test@BGWEBAGENCY.com'
        user = get_user_model().objects.create_user(
            email,
            'test123'
        )

        # .lower() is a string fn that makes the input lowercase
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            # anything we run here should raise the ValueError
            get_user_model().objects.create_user(
                None,
                'test123'
            )

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@bgwebagency.com',
            'test123'
        )

        # check if user is a superuser
        # check if user is a super user and user is a staff
        # is_superuser is included in user model as part of permissions mixin
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test the tag string representation"""
        # create a tag
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        # check if string representation of tag matches the above name
        self.assertEqual(str(tag), tag.name)
