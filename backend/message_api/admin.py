from django.contrib import admin
from .models import TimelineEvent, CalendarEvent

@admin.register(TimelineEvent)
class TimelineEventAdmin(admin.ModelAdmin):
    list_display = ('date', 'title', 'created_at', 'updated_at')
    list_filter = ('date',)
    search_fields = ('title', 'details')
    ordering = ('-date',)

# Register your models here.
@admin.register(CalendarEvent)
class CalendarEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'end_time', 'event_type', 'is_all_day', 'updated_at')
    list_filter = ('event_type', 'is_all_day', 'start_time')
    search_fields = ('title', 'description')
    ordering = ('-start_time',)
