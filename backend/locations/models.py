from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    image = models.ImageField(upload_to='location_images/', blank=True, null=True)
    visited_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name 