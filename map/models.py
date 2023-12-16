from django.db import models
from django.contrib.auth.models import User

class Marker(models.Model):
    name = models.CharField(max_length=100)
    map_url = models.CharField(max_length=1000)
    lat = models.FloatField()
    lng = models.FloatField()
    location = models.CharField(max_length=500)
    website = models.CharField(max_length=100)
    contact = models.CharField(max_length=200, blank=True, null=True)
    program = models.CharField(max_length=200, blank=True, null=True)
    scholarship = models.BooleanField(default=False)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
