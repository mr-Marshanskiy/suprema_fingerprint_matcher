from django.contrib import admin
from django.utils import timezone

from django.db import models


class DateMixin(models.Model):
    created_at = models.DateTimeField(
        verbose_name='Created at', null=True, blank=False
    )
    updated_at = models.DateTimeField(verbose_name='Updated at', null=True, blank=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not getattr(self, self.__class__._meta.pk.name) and not self.created_at:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(DateMixin, self).save(*args, **kwargs)


class DictBaseCodeMixin(models.Model):
    code = models.CharField('Code', max_length=15, primary_key=True, unique=True)
    name = models.CharField('Name', max_length=63)

    def __str__(self):
        return f'{self.name} (code: {self.code})'

    class Meta:
        abstract = True
        ordering = ('name',)


class DateModelAdminMixin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at',)