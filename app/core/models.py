from django.db import models
# imports required from django to customize use rmodel
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin


# user manager class - provides helper fn for creating user / superuser
class UserManager(BaseUserManager):

    # extra_fields will contain all additional fields other than email & pwd
    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        # Create a new model
        # normalize_email: helper fn that comes with BaseUserManager class
        user = self.model(email=self.normalize_email(email), **extra_fields)
        # set_password helper fn
        user.set_password(password)
        # the self._db option is helpful when we are using multiple DBs
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
