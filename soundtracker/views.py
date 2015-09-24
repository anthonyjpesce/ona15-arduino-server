import json
import logging
import datetime
from django.utils import timezone
from django.http import HttpResponse
from soundtracker.models import Robot, Signal
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import get_object_or_404

logger = logging.getLogger(__name__)


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
    robot_id = request.REQUEST.get('robot_id', None)
    voltage = request.REQUEST.get('volt', None)
    logger.debug("Signal recieved: robot_id:%s\tvoltage: %s" % (robot_id, voltage))

    # Return a 400 response for a malformed request
    if not robot_id or not voltage:
        return HttpResponse(status=400)

    robot = get_object_or_404(Robot, id=robot_id)

    logger.debug("Adding signal to %s" % robot)

    # Add our reading to the database
    Signal.objects.create(
        robot=robot,
        voltage=round(voltage, 2),
    )

    # We're good, return a 200 response
    return HttpResponse(status=200)


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
        context['robots'] = Robot.objects.all()

        return context
