from django.db import models
from django.contrib.auth.models import User

class Marker(models.Model):
    PROGRAM_TYPES = [
        ("BA", "Bachelor of Arts"),
        ("BS", "Bachelor of Science"),
        ("BBA", "Bachelor of Business Administration"),
        ("BEng", "Bachelor of Engineering"),
        ("BFA", "Bachelor of Fine Arts"),
        ("BEd", "Bachelor of Education"),
        ("BSN", "Bachelor of Nursing"),
        ("LLB", "Bachelor of Law"),
        ("BCom", "Bachelor of Commerce"),
        ("BSW", "Bachelor of Social Work"),
        ("NA", "Other"),
    ]
    
    name = models.CharField(max_length=100)
    map_url = models.CharField(max_length=1000)
    lat = models.FloatField()
    lng = models.FloatField()
    location = models.CharField(max_length=500)
    website = models.CharField(max_length=100)
    contact = models.CharField(max_length=200, blank=True, null=True)
    program = models.CharField(max_length=200, blank=True, null=True)
    program_type = models.CharField(max_length=5, choices=PROGRAM_TYPES, default='NA')
    scholarship = models.BooleanField(default=False)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
