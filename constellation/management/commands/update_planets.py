from django.core.management.base import NoArgsCommand

from django.contrib.auth.models import User
from django.db import transaction

from constellation.models import Stream

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        return update_planets()

def update_planets():
    for stream in Stream.objects.all():
        stream.update_planet()
