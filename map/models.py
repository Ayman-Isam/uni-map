from django.db import models

class Marker(models.Model):
    name = models.CharField(max_length=100)
    map_url = models.CharField(max_length=1000)
    lat = models.FloatField()
    lng = models.FloatField()
    location = models.CharField(max_length=500)
    website = models.CharField(max_length=100)
