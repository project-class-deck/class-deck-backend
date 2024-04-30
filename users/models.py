from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    nickname = models.CharField(
        max_length=50, blank=False, null=False, verbose_name=_("닉네임")
    )


class Guest(User):
    class Meta:
        proxy = True
