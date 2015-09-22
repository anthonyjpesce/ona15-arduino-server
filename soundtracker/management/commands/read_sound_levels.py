import twitter
from settings_private import *
from django.conf import settings
from soundtracker.models import Robot
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Load test data into the DB. Randomly assigns each voltage in the list to an Arduino."

    def handle(self, *args, **options):
        # Set up the Twitter API
        api = twitter.Api(
            consumer_key=TWITTER_CONSUMER_KEY,
            consumer_secret=TWITTER_CONSUMER_SECRET,
            access_token_key=TWITTER_ACCESS_TOKEN_KEY,
            access_token_secret=TWITTER_ACCESS_TOKEN_SECRET
        )

        for robot in Robot.objects.all():
            peak_voltage = robot.has_sound_spike()

            if peak_voltage:
                # Tweet here
                tweet = "Things are really going off in " + robot.location + "! " + robot.name + " picked up a reading\
                 of " + peak_voltage
                api.PostUpdate(tweet)
