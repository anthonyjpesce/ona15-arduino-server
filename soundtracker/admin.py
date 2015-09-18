from django.contrib import admin
from soundtracker.models import Robot, Signal


class RobotAdmin(admin.ModelAdmin):
    list_display = ['name', 'location']


class SignalAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'arduino_number', 'voltage']
    list_filter = ['arduino_number']


admin.site.register(Signal, SignalAdmin)
admin.site.register(Robot, RobotAdmin)
