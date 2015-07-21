import random
import string
from django.core.management import BaseCommand
from decider_app.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        for user in User.objects.filter(username=''):
            username = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))
            while User.objects.filter(username=username).count() > 0:
                username = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))
            user.username = username
            print(str(user.id) + ": " + username)
            user.save()