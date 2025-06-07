from django.db import models

# Create your models here.
class Message(models.Model):
    content = models.TextField()
    author = models.CharField(max_length=100, blank=True, default='Anonymous')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author}: {self.content[:50]}"

class TimelineEvent(models.Model):
    date = models.DateField()
    title = models.CharField(max_length=200)
    details = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.date} - {self.title}"

class CalendarEvent(models.Model):
    EVENT_TYPE_CHOICES = [
        ('holiday', 'Holiday'),
        ('memo', 'Memo'),
        ('log', 'Log'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True) # Optional for single-point events or if duration is implicit
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES, default='memo')
    is_all_day = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    
    # If you want to associate events with users in the future
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['start_time']

    def __str__(self):
        return f"{self.title} ({self.get_event_type_display()}) - {self.start_time.strftime('%Y-%m-%d %H:%M')}"
