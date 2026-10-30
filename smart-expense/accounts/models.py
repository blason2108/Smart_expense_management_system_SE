from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user (SEB-F-001). Email is unique so duplicate identifiers are rejected."""
    email = models.EmailField("email address", unique=True)
    REQUIRED_FIELDS = ["email"]
