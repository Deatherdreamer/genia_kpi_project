from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Description of my command'

    def handle(self, *args, **options):
        # Your command logic goes here
        self.stdout.write('Hello, world!')