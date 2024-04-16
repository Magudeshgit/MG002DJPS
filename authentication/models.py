from django.db import models
from django.contrib.auth.models import AbstractUser
from .modelmanagers import User_Manager


class Users(AbstractUser):
    username=None
    first_name=None
    last_name=None

    business_name = models.CharField(max_length=50)
    Owner = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)

    objects = User_Manager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def has_perm(self, perm, obj=None):
        return True
    def has_module_perm(self, app_label):
        return True


    def __str__(self):
        return self.email