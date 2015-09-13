from django.contrib import admin
from soundtracker.models import Signal


class SignalAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'arduino_number', 'voltage']
    list_filter = ['arduino_number']

admin.site.register(Signal, SignalAdmin)