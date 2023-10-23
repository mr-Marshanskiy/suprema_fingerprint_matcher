from django.core.management.base import BaseCommand

from users.models import AuthApiToken


class Command(BaseCommand):
    help = 'Generate API Token'

    def handle(self, *args, **options):
        AuthApiToken.objects.all().delete()
        print('Done')
