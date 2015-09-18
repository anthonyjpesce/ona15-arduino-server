import json
import datetime
import calculate
from django.utils import timezone
from django.http import HttpResponse
from soundtracker.models import Robot, Signal
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def signal_submit(request):
    """
    Takes a post request from an Arduino and adds the reading to
    our database.
    """
    # It must be a POST request
    if request.method != 'POST':
        return HttpResponse(status=405)

    # Grab the data we want from the request
    arduino_number = request.REQUEST.get('aid', None)
    robot, created = Robot.objects.get_or_create(id=arduino_number)
    voltage = request.REQUEST.get('volt', None)

    # Return a 400 response for a malformed request
    if not arduino_number or not voltage:
        return HttpResponse(status=400)

    # Add our reading to the database
    Signal.objects.create(
        robot=robot,
        voltage=voltage,
    )

    # We're good, return a 200 response
    return HttpResponse(status=200)


def get_signal_stats(robot_id=None):
    """
    Calculate various stats about the signals in the database.
    We'll want:
    1) number of signals sent
    2) Average volts
    """
    if robot_id:
        signals = Signal.objects.filter(robot__id=robot_id)
    else:
        signals = Signal.objects.all()

    voltages = list(signals.values_list('voltage').order_by('voltage'))
    mean_voltage = calculate.mean(voltages)
    std_dev = calculate.standard_deviation(voltages)

    return mean_voltage, std_dev


def get_signal_json(request, arduino_id=1):
    """
    Get all signals over the last 10 minutes
    """
    ten_minutes = timezone.localtime(timezone.now()) - datetime.timedelta(minutes=10)
    signals = Signal.objects.filter(robot__id=arduino_id,
                                    timestamp__lt=timezone.localtime(timezone.now()),
                                    timestamp__gte=ten_minutes)
    response = json.dumps([s.as_dict() for s in signals])

    return HttpResponse(response, content_type='text/json')


class IndexView(TemplateView):
    """
    The homepage and its many doodads.
    """
    template_name = 'soundtracker/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        context["voltages"] = Signal.objects.all().values_list('voltage')

        return context
