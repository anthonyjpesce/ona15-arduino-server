import os
import csv
import random
import datetime
from django.conf import settings
from soundtracker.models import Signal
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Load test data into the DB. Randomly assigns each voltage in the list to an Arduino."

    def handle(self, *args, **options):
        filename = 'test_data.txt'
        data_dir = os.path.join(settings.BASE_DIR, 'soundtracker', 'data')
        signals_list = []

        # Setting start time to an arbitraty time in the past
        dummy_starttime = datetime.datetime(2015, 9, 12, 22, 16, 8)
        time = dummy_starttime

        with open(os.path.join(data_dir, filename)) as infile:
            reader = csv.reader(infile)
            for row in reader:
                arduino = random.randrange(1,6)
                s = Signal(
                        arduino_number=arduino,
                        timestamp=time,
                        voltage=row[0]
                    )
                time = time + datetime.timedelta(seconds=1)
                signals_list.append(s)

            Signal.objects.bulk_create(signals_list, batch_size=500)
