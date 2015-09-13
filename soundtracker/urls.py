from soundtracker import views
from django.conf.urls import patterns, url


urlpatterns = patterns('',
    # Homepage
    url(r'^$', views.IndexView.as_view(), name='home'),
    # signal submit
    url(r'^signal-submit/$', views.signal_submit, name='submit'), 
)
