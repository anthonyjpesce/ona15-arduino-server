from django.db import models
from django.utils import timezone


class Robot(models.Model):
    name = models.CharField(default="Unnamed robot", null=True, max_length=30)
    location = models.CharField(blank=True, null=True, max_length=30)

    def check_for_spikes(self):
        """
        Find the standard deviation of the past 10 minutes.
        Send out a tweet if there are any signals greater than two standard deviations 
        in the past 30 seconds. 
        """
        ten_minutes = timezone.localtime(timezone.now()) - datetime.timedelta(minutes=20)
        thirty_seconds = timezone.localtime(timezone.now()) - datetime.timedelta(seconds=30)
        signals_past_ten_min = Signal.objects.filter(robot__id=robot_id,
                timestamp__lt=timezone.localtime(timezone.now()),
                timestamp__gte=ten_minutes
            )
        std_dev = calculate.standard_deviation(voltages)
        twice_std_dev = std_dev * 2
        signals_past_30_secs = signals_past_ten_min.filter(timestamp__gte=thirty_seconds, voltage__gte=twice_std_dev)

        if signals_past_30_secs.count() > 0:
            # This is where we tweet?
            pass


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
    timestamp = models.DateTimeField(auto_now_add=True)
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
