from django.db import models
from django.utils import timezone

class Signal(models.Model):
    """
    A transmission from our robot
    """
    ARDUINO_NUMBER_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5')
    )
    arduino_number = models.CharField(
        blank=True, null=True, choices=ARDUINO_NUMBER_CHOICES, max_length=2,
    )
    timestamp = models.DateTimeField(default=timezone.now())
    voltage = models.DecimalField(max_digits=4, decimal_places=2)

    def as_dict(self):
        return {
            "no": self.arduino_number,
            "ts": self.timestamp.isoformat(),
            "v": str(self.voltage)
        }

    class Meta:
        ordering = ('-timestamp', 'pk')

    def __unicode__(self):
        "Robot %s: %s" % (self.arduino_number, str(self.timestamp))
