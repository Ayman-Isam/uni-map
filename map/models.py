from django.db import models
from django.contrib.auth.models import User

class Program(models.Model):
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

    name = models.CharField(max_length=200)
    program_type = models.CharField(max_length=5, choices=PROGRAM_TYPES, default='NA')
    
    def to_dict(self):
        return {
            'name': self.name,
            'program_type': self.program_type,
        }

class Marker(models.Model):
    name = models.CharField(max_length=100)
    map_url = models.CharField(max_length=1000)
    lat = models.FloatField()  
    lng = models.FloatField()
    location = models.CharField(max_length=500)
    website = models.CharField(max_length=100)
    contact = models.CharField(max_length=200, blank=True, null=True)
    programs = models.ManyToManyField('Program', blank=True)
    scholarship = models.BooleanField(default=False)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if self.pk:
            existing = Marker.objects.get(pk=self.pk)
            if existing.logo and self.logo and existing.logo != self.logo:
                existing.logo.delete(save=False)
        super().save(*args, **kwargs)
        
    def to_representation(self):
        representation = super().to_representation()
        representation['programs'] = [program.to_dict() for program in self.programs.all()]
        return representation
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
class Code(models.Model):
    code = models.CharField(max_length=15)
    email = models.EmailField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=True)
    expires_at = models.DateTimeField()

class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=6, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField()

    class Meta:
        ordering = ['-timestamp']
