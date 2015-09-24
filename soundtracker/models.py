import calculate
import datetime
import logging
from django.db import models
from django.utils import timezone

logger = logging.getLogger(__name__)


class Robot(models.Model):
    name = models.CharField(default="Unnamed robot", null=True, max_length=30)
    location = models.CharField(blank=True, null=True, max_length=30)
    description = models.TextField(blank=True, null=True)

    def has_sound_spike(self):
        """
        Find the standard deviation of the past 10 minutes.
        Send out a tweet if there are any signals greater than two standard deviations
        in the past 10 seconds.
        """
        ten_minutes = timezone.localtime(timezone.now()) - datetime.timedelta(minutes=10)
        ten_seconds = timezone.localtime(timezone.now()) - datetime.timedelta(seconds=10)
        signals_past_ten_min = self.signal_set.filter(
                timestamp__lt=timezone.localtime(timezone.now()),
                timestamp__gte=ten_minutes
            )
        if signals_past_ten_min.count > 0:
            voltages = list(signals_past_ten_min.values_list('voltage', flat=True).order_by('voltage'))
            avg = calculate.mean(voltages)
            std_dev = calculate.standard_deviation(voltages)
            twice_std_dev = (std_dev * 2) + avg
            signals_past_10_secs = signals_past_ten_min.filter(timestamp__gte=ten_seconds, voltage__gte=twice_std_dev)

            # return the voltage of the highest signal if there has been a spike
            # Or return False
            if signals_past_10_secs.count() > 0:
                signals_past_10_secs = list(signals_past_10_secs.values_list('voltage', flat=True).order_by('-voltage'))
                return signals_past_10_secs[0]
            else:
                return False
        else:
            return False

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        if self.name:
            return "Robot: %s" % self.name
        else:
            return "Robot: %d" % self.id


class Signal(models.Model):
    """
    A transmission from our robot
    """
    robot = models.ForeignKey('Robot', null=True)
    timestamp = models.DateTimeField()
    voltage = models.DecimalField(max_digits=4, decimal_places=2)

    def as_dict(self):
        return {
            "ts": timezone.localtime(self.timestamp).strftime("%Y-%m-%d %H:%M:%S"),
            "v": str(self.voltage)
        }

    class Meta:
        ordering = ('-timestamp', 'pk',)

    def __unicode__(self):
        return "Robot %s: %s" % (self.robot.id, str(self.timestamp))

    def save(self, *args, **kwargs):
        if not self.timestamp:
            self.timestamp = timezone.localtime(timezone.now())
        logger.debug("Saving signal %s %s volts" % (self.robot, self.voltage))
        super(Signal, self).save(*args, **kwargs)
