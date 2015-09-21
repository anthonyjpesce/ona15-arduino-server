from django.conf import settings
from django.utils import timezone
from soundtracker.models import Robot
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Load test data into the DB. Randomly assigns each voltage in the list to an Arduino."

    def handle(self, *args, **options):
        for robot in Robot.objects.all():
            if robot.has_sound_spike():
                # Tweet here
                pass
