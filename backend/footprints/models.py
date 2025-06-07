from django.db import models

class Footprint(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    date = models.DateField()
    description = models.TextField()
    image = models.ImageField(upload_to='footprints/')

    def __str__(self):
        return self.name