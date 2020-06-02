from django.db import models
# imports required from django to customize use rmodel
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
# To retrieve AUTH settings
from django.conf import settings


# user manager class - provides helper fn for creating user / superuser
class UserManager(BaseUserManager):

    # extra_fields will contain all additional fields other than email & pwd
    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        # Create a new model
        if not email:
            raise ValueError('Users must have an email address')
        # normalize_email: helper fn that comes with BaseUserManager class
        user = self.model(email=self.normalize_email(email), **extra_fields)
        # set_password helper fn
        user.set_password(password)
        # the self._db option is helpful when we are using multiple DBs
        user.save(using=self._db)

        return user

    # will use create_superuser only from terminal so no need of extra_fields
    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        # call create_user fn which we created above
        user = self.create_user(email, password)
        # set is_staff and is_superuser to True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # creating an object using UserManager class instance
    objects = UserManager()

    # Set email as the USERNAME_FIELD
    USERNAME_FIELD = 'email'


class Tag(models.Model):
    """Tag to be used for a recipe"""
    name = models.CharField(max_length=255)
    # recommended way of fetching auth user: use settings from django.conf
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )  # CASCADE means on deleting user, delete the tag as well

    # string representation of Tag model on admin
    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredient to be used in a recipe"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    # string representation of Ingredient model on admin
    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Recipe object"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    # can also mention Ingredient as class instead of string,
    # but that way, will hv to make sure that Ingredient class is above Recipe
    ingredients = models.ManyToManyField('Ingredient')
    tags = models.ManyToManyField('Tag')

    # string representation of Recipe model on admin
    def __str__(self):
        return self.title
