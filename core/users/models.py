from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from core.common.models import TimeStampedModel
from core.users.managers import UserManager


class User(AbstractUser, TimeStampedModel):
    """Custom User model."""

    email = models.EmailField(_("email address"), unique=True)
    name = models.CharField(_("full name"), max_length=150, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self) -> str:
        return self.email
