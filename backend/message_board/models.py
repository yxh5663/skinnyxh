from django.db import models

# Create your models here.

class Message(models.Model):
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.text[:50]}... ({self.timestamp.strftime('%Y-%m-%d %H:%M')})"
