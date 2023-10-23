from django.contrib import admin

from common.models.mixins import DateModelAdminMixin
from persons import models


@admin.register(models.Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')


@admin.register(models.Person)
class PersonAdmin(DateModelAdminMixin):
    list_display = ('id', 'first_name', 'last_name', 'board_id',)
    search_fields = ('first_name', 'last_name', 'board_id')