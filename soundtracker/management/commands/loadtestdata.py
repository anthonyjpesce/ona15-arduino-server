import os
import csv
import random
import datetime
from django.conf import settings
from django.utils import timezone
from soundtracker.models import Robot, Signal
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Load test data into the DB. Randomly assigns each voltage in the list to an Arduino."

    def handle(self, *args, **options):
        # Delete current data
        Signal.objects.all().delete()

        filename = 'test_data.txt'
        data_dir = os.path.join(settings.BASE_DIR, 'soundtracker', 'data')
        signals_list = []

        # Setting start time to fifteen minutes ago
        dummy_starttime = timezone.localtime(timezone.now()) - datetime.timedelta(minutes=15)
        time = dummy_starttime

        with open(os.path.join(data_dir, filename)) as infile:
            reader = csv.reader(infile)
            for row in reader:

                # Assign each signal to a random Arduino robot
                arduino = random.randrange(1, 6)
                # if that robot doesn't exist, create it
                robot, created = Robot.objects.get_or_create(id=arduino)

                s = Signal(
                        robot=robot,
                        timestamp=time,
                        voltage=row[0]
                    )
                time = time + datetime.timedelta(seconds=1)
                signals_list.append(s)

            Signal.objects.bulk_create(signals_list, batch_size=500)
