from django.contrib import admin

from .models import Marker, Profile, Program, Code

admin.site.register(Marker)
admin.site.register(Profile)
admin.site.register(Program)
admin.site.register(Code)
