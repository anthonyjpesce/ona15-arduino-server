import calculate
import datetime
from django.conf import settings
from django.utils import timezone
from soundtracker.models import Robot, Signal
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Load test data into the DB. Randomly assigns each voltage in the list to an Arduino."

    def handle(self, *args, **options):
        pass