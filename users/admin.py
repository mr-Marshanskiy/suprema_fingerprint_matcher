from django.contrib import admin

from users.models import AuthApiToken


@admin.register(AuthApiToken)
class AuthApiTokenAdmin(admin.ModelAdmin):
    pass
