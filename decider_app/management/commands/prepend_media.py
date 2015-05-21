import os
from django.core.management import BaseCommand
from decider_app.models import Picture


class Command(BaseCommand):

    def handle(self, *args, **options):

        pics = Picture.objects.all()

        for pic in pics:
            if pic.preview_url and pic.url and not pic.url.startswith('media'):
                pic.url = os.path.join('media', pic.url)
                pic.preview_url = os.path.join('media', pic.preview_url)
                pic.save()
