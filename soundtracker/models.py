from django.db import models
from django.utils import timezone


class Robot(models.Model):
    name = models.CharField(default="Unnamed robot", null=True, max_length=30)
    location = models.CharField(blank=True, null=True, max_length=30)

    class Meta:
        ordering = ('-name',)

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
    timestamp = models.DateTimeField(default=timezone.now())
    voltage = models.DecimalField(max_digits=4, decimal_places=2)

    def as_dict(self):
        return {
            "ts": timezone.localtime(self.timestamp).strftime("%Y-%m-%d %H:%M:%S"),
            "v": str(self.voltage)
        }

    class Meta:
        ordering = ('-timestamp', 'pk',)

    def __unicode__(self):
        return "Robot %s: %s" % (self.arduino_number, str(self.timestamp))
