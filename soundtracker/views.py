from django.http import HttpResponse
from soundtracker.models import Signal
from django.views.generic import TemplateView


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
    voltage = request.REQUEST.get('volt', None)

    # Return a 400 response for a malformed request
    if not arduino_number or not voltage:
        return HttpResponse(status=400)

    # Add our reading to the database
    Signal.objects.create(
        arduino_number=arduino_number,
        voltage=voltage,
    )

    # We're good, return a 200 response
    return HttpResponse(status=200)


class IndexView(TemplateView):
    """
    The homepage and its many doodads.
    """
    template_name = 'soundtracker/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        return context