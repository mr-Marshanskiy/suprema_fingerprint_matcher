from rest_framework.permissions import BasePermission

from users.models import AuthApiToken


class AuthTokenPermission(BasePermission):
    group_code = None
    groups_codes = None

    def has_permission(self, request, view):
        return AuthApiToken.objects.filter(
            id=request.headers.get('AuthToken')
        ).exists()

    def has_object_permission(self, request, view, obj):
        return AuthApiToken.objects.filter(
            id=request.headers.get('AuthToken')
        ).exists()
