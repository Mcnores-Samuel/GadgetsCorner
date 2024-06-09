#!usr/bin/env python3
# -*- coding: utf-8 -*-
"""The UserProfile model represents the users of the application. It includes
fields to store relevant information about each user, such as their name and
email address

Classes:
    - UserProfileManager
    - UserProfile
"""
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
from django.utils import timezone


class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""
    def create_user(self, email, password=None, **extra_fields):
        """Create a new user profile

        Args:
            email (str): User email
            password (str, optional): User password. Defaults to None.
            **extra_fields: Extra fields to be added to the user profile

        Raises:
            ValueError: If email is not provided

        Returns:
            UserProfile: New user profile
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create a superuser"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class UserProfile(AbstractUser):
    """The UserProfile model represents the users of the application. It includes
    fields to store relevant information about each user, such as their name and
    email address

    Fields:
    - email: The email address of the user, which serves as the primary key.
    - phone_number: The phone number of the user.
    - is_staff: A boolean field indicating whether the user is a staff member.
    - is_active: A boolean field indicating whether the user is active.
    - date_joined: The date on which the user joined the application.
    - last_login: The date on which the user last logged in to the application.
    - is_agent: A boolean field indicating whether the user is an agent.
    - is_superuser: A boolean field indicating whether the user is a superuser.
    - groups: A many-to-many field linking the user to the groups to which they belong.
    - user_permissions: A many-to-many field linking the user to the permissions they have.

    Usage:
    The UserProfile model is used to manage user accounts and permissions within
    the application. It allows for the creation of new users, as well as the
    assignment of permissions and roles.

    Note:
    - The UserProfile model is a subclass of the AbstractUser model, which provides
        default implementations for the fields listed above.
    - The is_agent field is used to distinguish between agents and other users.
    - The is_superuser field is used to distinguish between superusers and other users.
    - The is_staff field is used to distinguish between staff members and other users.
    - The is_active field is used to distinguish between active and inactive users.
    - The date_joined field is used to track when users joined the application.
    - The last_login field is used to track when users last logged in to the application.
    """
    email = models.EmailField(max_length=100, unique=True)
    objects = UserProfileManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        app_label = 'gadgetsCorner'

    def __str__(self):
        return self.username
 

class UserAvatar(models.Model):
    """The UserAvatar model represents the avatars of the users of the application."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True)
    image = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        app_label = 'gadgetsCorner'
        verbose_name = 'User Avatar'
        verbose_name_plural = 'User Avatars'
