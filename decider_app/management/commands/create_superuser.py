import string
import uuid
from django.core.management import BaseCommand
from decider_app.models import User


class Command(BaseCommand):

    args = 'email=... password=...'

    def handle(self, *args, **options):

        arguments = {}
        for arg in args:
            try:
                key, value = string.split(arg, '=')
            except ValueError:
                continue
            arguments[key] = value

        email = arguments.get('email') if arguments.get('email') else 'admin@admin.com'
        password = arguments.get('password') if arguments.get('password') else 'admin'

        try:
            User.objects.get(email=email)
            print('user already exists')
            return
        except User.DoesNotExist:
            user = User(email=email, uid=uuid.uuid4().hex, is_superuser=True, is_staff=True)
            user.set_password(password)
            user.save()
            print('user created')
            return
