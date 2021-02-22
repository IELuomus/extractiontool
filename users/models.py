from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_editor = models.BooleanField(default=False)
    is_data_admin = models.BooleanField(default=False)
