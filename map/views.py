import json
import uuid
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView, PasswordResetCompleteView
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from .decorators import unauthenticated_user
from .models import Marker, Profile
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

def home(request):
    return render(request, 'home.html')

def get_lat_lng_from_gmaps_url(url):
   at_index = url.find('@')
   comma_index = url.find(',', at_index)
   if at_index != -1 and comma_index != -1:
       lat = url[at_index + 1:comma_index]
       lon_start = url.find(',', comma_index + 1)
       if lon_start != -1:
           lon = url[comma_index + 1:lon_start]
           return float(lat), float(lon)
   return None, None

@login_required(login_url='login')
def add_marker(request):
    markers = Marker.objects.all()
    program_types = Marker.PROGRAM_TYPES
    if request.method == 'POST':
        name = request.POST.get('name')
        map_url = request.POST.get('map_url')
        location = request.POST.get('location')
        website = request.POST.get('website')
        program = request.POST.get('program')
        program_type = request.POST.get('program_type')
        scholarship = request.POST.get('scholarship') == 'on'
        logo = request.FILES.get('logo')

        lat, lng = get_lat_lng_from_gmaps_url(map_url)
        if lat is None or lng is None:
            messages.error(request, 'Invalid Google Maps URL', extra_tags='toast-error')
            return render(request, 'add_marker.html', {'error': 'Invalid Google Maps URL.', 'markers': markers, 'program_types': program_types})

        # Save the data to the database
        marker = Marker(name=name, map_url=map_url, location=location, website=website, program=program, program_type=program_type, scholarship=scholarship, logo=logo, lat=lat, lng=lng)
        marker.save()

        messages.success(request, 'Marker added successfully', extra_tags='toast-success')
        return redirect('add_marker')  
    else:
        return render(request, 'add_marker.html', {'markers': markers, 'program_types': program_types})
    
def edit_marker(request, pk):
    marker = get_object_or_404(Marker, pk=pk)
    program_types = Marker.PROGRAM_TYPES

    if request.method == 'POST':
        name = request.POST.get('name')
        map_url = request.POST.get('map_url')
        location = request.POST.get('location')
        website = request.POST.get('website')
        program = request.POST.get('program')
        program_type = request.POST.get('program_type')
        scholarship = request.POST.get('scholarship') == 'on'
        logo = request.FILES.get('logo')

        lat, lng = get_lat_lng_from_gmaps_url(map_url)
        if lat is None or lng is None:
            messages.error(request, 'Invalid Google Maps URL', extra_tags='toast-error')
            return render(request, 'edit_marker.html', {'error': 'Invalid Google Maps URL.', 'marker': marker, 'program_types': program_types})

        marker.name = name
        marker.map_url = map_url
        marker.location = location
        marker.website = website
        marker.program = program
        marker.program_type = program_type
        marker.scholarship = scholarship
        if logo:
            marker.logo.delete(save=False) 
            marker.logo = logo  
        marker.lat = lat
        marker.lng = lng
        marker.save()

        messages.success(request, 'Marker updated successfully', extra_tags='toast-success')
        return redirect('view_marker')
    else:
        return render(request, 'edit_marker.html', {'marker': marker, 'program_types': program_types})

def view_marker(request):
    markers = Marker.objects.all()
    return render(request, 'view_marker.html', {'markers': markers})
    
def get_markers(request):
    markers = Marker.objects.all()
    marker_list = serializers.serialize('json', markers)
    return JsonResponse(json.loads(marker_list), safe=False)

def delete_marker(request, pk):
    marker = get_object_or_404(Marker, pk=pk)
    marker.delete()
    messages.success(request, 'Marker deleted successfully', extra_tags='toast-success')
    return redirect('view_marker')

@csrf_exempt
def update_marker(request):
    data = json.loads(request.body)
    marker = Marker.objects.get(pk=data['id'])
    setattr(marker, data['column'], data['value'])
    marker.save()
    return JsonResponse({'status': 'success'})

class CustomPasswordResetView(PasswordResetView):
    success_url = reverse_lazy('password_reset')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            response = super().form_valid(form)
            messages.success(self.request, 'Password reset link has been sent', extra_tags='toast-success')
        else:
            messages.error(self.request, 'An account associated with this email does not exist', extra_tags='toast-error')
        return HttpResponseRedirect(self.get_success_url())

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    def get(self, request, *args, **kwargs):
        messages.success(request, 'Your password has been reset', extra_tags='toast-success')
        return redirect('login') 

#Decorator to prevent logged in user from viewing login page 
@unauthenticated_user
def login_attempt(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = username).first()
        if user_obj is None:
            messages.error(request, 'User not found', extra_tags='toast-error')
            return redirect('/login/')

        profile_obj = Profile.objects.filter(user = user_obj).first()

        if not profile_obj.is_verified:
            messages.error(request, 'Profile is not verified, check your email', extra_tags='toast-error')
            return redirect('/login/')

        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, 'Wrong Password', extra_tags='toast-error')
            return redirect('/login/')

        login(request, user)
        return redirect('/')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))

#Decorator to prevent logged in user from viewing register page  
@unauthenticated_user
def register_attempt(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            if User.objects.filter(username=username).first():
                messages.error(request, 'Username is taken.', extra_tags='toast-error')
                return redirect('/register/')
            if User.objects.filter(email=email).first():
                messages.error(request, 'Email is taken.', extra_tags='toast-error')
                return redirect('/register/')
            user_obj = User(username=username, email=email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user=user_obj, auth_token=auth_token)
            profile_obj.save()
            send_mail_after_register(email, auth_token)
            messages.success(request, 'An email has been sent for account verification', extra_tags='toast-success')
            return redirect('/login/')
        except Exception as e:
            print(e)
    return render(request, 'register.html')

def success(request):
    return render(request,'success.html')  


def verify (request, auth_token):
    try: 
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified', extra_tags='toast-error')
                return redirect('/')

            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified', extra_tags='toast-success')
            return redirect('/login/')
        else:
            return redirect('/error/')
    except Exception as e:
        print(e)


def error_page(request):
    return render(request, 'error.html')

def send_mail_after_register(email, token):
    subject = "Your account needs to be verified"
    message = f"Hi, paste the link to verify your account https://unimap.pythonanywhere.com/verify/{token}/"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)