import uuid

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group as BaseGroup

from django.db import models


class Group(BaseGroup):
    code = models.CharField('Code', max_length=32, null=True, unique=True)


class User(AbstractUser):
    groups = models.ManyToManyField(
        Group, related_name='groups', verbose_name='Groups', blank=True
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.full_name} ({self.pk})'


class AuthApiToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        verbose_name = 'Auth API Token'
        verbose_name_plural = 'Auth API Tokens'
        indexes = (
            models.Index(fields=['id',]),
        )

    def __str__(self):
        return self.pk

