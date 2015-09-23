import logging
import random
import twitter
from django.conf import settings
from soundtracker.models import Robot
from django.core.management.base import BaseCommand, CommandError

logger = logging.getLogger(__name__)


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
            name = robot.name or u'Bot with no name'
            location = robot.location or u'unplaced robot'

            if peak_voltage:
                # Tweet here
                tweets = [
                    "Things are really going off in the " + location + "! " + name + " picked up a reading of " + str(peak_voltage) + " volts. #ONA15Bot",
                    location + " must be turned up to 11. " + name + " just recorded " + str(peak_voltage) + " volts. #ONA15Bot",
                    location + " just hit " + str(peak_voltage) + " on the #ONA15Bot voltage meter. Turn down for what!",
                    "I went to #ONA15 and all I got was this splitting headache. Audio sensor reads " + str(peak_voltage) + " in the " + location + " #ONA15Bot"
                ]
                tweet = tweets[random.randrange(0, len(tweets))]

                logger.debug(tweet)
                api.PostUpdate(tweet)
            else:
                logger.debug("No spike recorded for " + name)
