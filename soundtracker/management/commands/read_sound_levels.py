import twitter
from django.conf import settings
from soundtracker.models import Robot
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Load test data into the DB. Randomly assigns each voltage in the list to an Arduino."

    def handle(self, *args, **options):
        # Set up the Twitter API
        api = twitter.Api(
            consumer_key=settings.TWITTER_CONSUMER_KEY,
            consumer_secret=settings.TWITTER_CONSUMER_SECRET,
            access_token_key=settings.TWITTER_ACCESS_TOKEN_KEY,
            access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET
        )

        for robot in Robot.objects.all():
            peak_voltage = robot.has_sound_spike()

            if peak_voltage:
                # Tweet here
                name = robot.name or u'Bot with no name'
                location = robot.location or u'unplaced robot'

                tweet = "Things are really going off in " + location + "! " + name + " picked up a reading\
                 of " + str(peak_voltage)
                api.PostUpdate(tweet)
            else:
                print "No spike recorded for " + robot.id
