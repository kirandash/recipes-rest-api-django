# built in python fn to mock uuid fn
from unittest.mock import patch

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
    def test_create_user_with_email_successful(self):
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
        # Check Tag model exists, verify create and retrieve
        # create a tag
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        # check if string representation of tag matches the above name
        self.assertEqual(str(tag), tag.name)

    def test_ingredients_str(self):
        """Test the ingredient string representation"""
        # Check Ingredient model exists, verify create and retrieve
        # create an ingredient
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Cucumber'
        )

        # check if string representation of ingredient matches the above name
        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """Test the recipe string representation"""
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='Steak and mushroom sauce',
            time_minutes=5,
            price=5.00
        )

        self.assertEqual(str(recipe), recipe.title)

    # module uuid, uuid4 is a fn that will generate version: uuid4
    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test that image is saved in the correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        # create a file path
        file_path = models.recipe_image_file_path(None, 'myimage.jpg')
        # expected path, string interpolation(Python3 feature)
        exp_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)
