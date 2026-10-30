from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.functions import Lower


class User(AbstractUser):
    """Custom user (SEB-F-001). Email is unique so duplicate identifiers are rejected."""

    email = models.EmailField("email address", unique=True)
    REQUIRED_FIELDS = ["email"]

    class Meta:
        constraints = [models.UniqueConstraint(Lower("email"), name="user_email_case_unique")]
