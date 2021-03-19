from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string
from django.db import models


# Create your models here.


class UserManager(BaseUserManager):
    def _create_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError('Email is required!')
        if not username:
            raise ValueError('Name is required!')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.create_activation_code()
        user.save(using=self.db)
        return user

    def create_user(self, email, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, email, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        if extra_fields.get('is_superuser') is False:
            raise ValueError('Super users must have is_superuser=True')
        return self._create_user(email, username, password, **extra_fields)


class MyUser(AbstractUser):
    username = models.CharField(max_length=50)
    email = models.EmailField(primary_key=True)
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=50, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    def create_activation_code(self):
        activation_code = get_random_string(20)
        if MyUser.objects.filter(activation_code=activation_code).exists():
            self.create_activation_code()
        self.activation_code = activation_code

