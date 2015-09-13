from django.db import models


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
    timestamp = models.DateTimeField(auto_now_add=True)
    voltage = models.DecimalField(max_digits=4, decimal_places=2)

