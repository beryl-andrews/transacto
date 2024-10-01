from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password

# Custom user manager to handle user creation
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, user_type='user', **extra_fields):
        """Creates and saves a regular user."""
        if not email:
            raise ValueError('The Email field must be set')
        if not username:
            raise ValueError('The Username field must be set')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, user_type=user_type, **extra_fields)
        user.set_password(password)  # Hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """Creates and saves a superuser."""
        return self.create_user(username, email, password, user_type='admin', **extra_fields)

# Custom user model
class User(AbstractBaseUser):
    USER_TYPES = [
        ('user', 'User'),
        ('admin', 'Admin'),
    ]

    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    user_type = models.CharField(max_length=50, choices=USER_TYPES, default='user')

    # Define the username field and required fields
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']  # Fields required for createsuperuser

    objects = UserManager()  # Custom manager

    def save(self, *args, **kwargs):
        if not self.pk:  # If it's a new user, hash the password
            self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.username

