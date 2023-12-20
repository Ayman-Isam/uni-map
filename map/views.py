import json
import uuid
import random
import string
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib import messages
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView, PasswordResetCompleteView, PasswordResetConfirmView
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from .decorators import unauthenticated_user
from .models import Marker, Profile, Program, Code, AuditLog
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

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
    program_types = Program.PROGRAM_TYPES
    if request.method == 'POST':
        name = request.POST.get('name')
        map_url = request.POST.get('map_url')
        if map_url is None:
            messages.error(request, 'Map URL is required', extra_tags='toast-error')
            context = {'error': 'Map URL is required.', 'markers': markers, 'program_types': program_types, 'form_data': request.POST}
            return render(request, 'add_marker.html', context)
        location = request.POST.get('location')
        website = request.POST.get('website')
        scholarship = request.POST.get('scholarship') == 'on'
        logo = request.FILES.get('logo')

        lat, lng = get_lat_lng_from_gmaps_url(map_url)
        if lat is None or lng is None:
            messages.error(request, 'Invalid Google Maps URL', extra_tags='toast-error')
            context = {'error': 'Invalid Google Maps URL.', 'markers': markers, 'program_types': program_types, 'form_data': request.POST}
            return render(request, 'add_marker.html', context)

        marker = Marker(name=name, map_url=map_url, location=location, website=website, scholarship=scholarship, logo=logo, lat=lat, lng=lng)
        marker.save()
        AuditLog.objects.create(user=request.user, action='create', details=f'Added marker {marker.name}')
        
        program_index = 0
        while True:
            program_name = request.POST.get('program_' + str(program_index))
            program_type = request.POST.get('program_type_' + str(program_index))

            if program_name is None or program_type is None:
                if program_index == 0:
                    messages.error(request, 'At least one program must be added', extra_tags='toast-error')
                    context = {'error': 'At least one program must be added.', 'markers': markers, 'program_types': program_types, 'form_data': request.POST}
                    return render(request, 'add_marker.html', context)
                else:
                    break

            program = Program(name=program_name, program_type=program_type)
            program.save()
            marker.programs.add(program)

            program_index += 1
        
        messages.success(request, 'University added successfully', extra_tags='toast-success')
        return redirect('view_marker')  
    else:
        return render(request, 'add_marker.html', {'markers': markers, 'program_types': program_types})
    
def edit_marker(request, pk):
    marker = get_object_or_404(Marker, pk=pk)
    program_types = Program.PROGRAM_TYPES

    if request.method == 'POST':
        name = request.POST.get('name')
        map_url = request.POST.get('map_url')
        location = request.POST.get('location')
        website = request.POST.get('website')
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
        marker.scholarship = scholarship
        if logo:
            marker.logo.delete(save=False) 
            marker.logo = logo  
        marker.lat = lat
        marker.lng = lng

        new_programs = []
        program_index = 0
        while True:
            program_name = request.POST.get('program_' + str(program_index))
            program_type = request.POST.get('program_type_' + str(program_index))

            if program_name is None or program_type is None:
                if program_index == 0:
                    messages.error(request, 'At least one program must be added', extra_tags='toast-error')
                    context = {'error': 'At least one program must be added.', 'marker': marker, 'program_types': program_types, 'form_data': request.POST}
                    return render(request, 'edit_marker.html', context)
                else:
                    break

            program = Program(name=program_name, program_type=program_type)
            program.save()
            new_programs.append(program)

            program_index += 1

        if new_programs:
            marker.programs.clear()
            for program in new_programs:
                marker.programs.add(program)

        marker.save()
        AuditLog.objects.create(user=request.user, action='update', details=f'Updated marker {marker.name}')

        messages.success(request, 'Marker updated successfully', extra_tags='toast-success')
        return redirect('view_marker')
    else:
        return render(request, 'edit_marker.html', {'marker': marker, 'program_types': program_types})
    
def delete_marker(request, pk):
    marker = get_object_or_404(Marker, pk=pk)
    marker_name = marker.name
    marker.delete()
    AuditLog.objects.create(user=request.user, action='delete', details=f'Deleted marker {marker_name}')
    messages.success(request, 'Marker deleted successfully', extra_tags='toast-success')
    return redirect('view_marker')

def view_marker(request):
    markers = Marker.objects.all()
    return render(request, 'view_marker.html', {'markers': markers})

def get_markers(request):
    markers = Marker.objects.all()
    marker_list = []
    for marker in markers:
        marker_dict = serializers.serialize('json', [marker])
        marker_dict = json.loads(marker_dict)[0]  # Convert the serialized string back to a dictionary
        programs = marker.programs.all()
        program_list = [{'name': program.name, 'program_type_display': program.get_program_type_display()} for program in programs]
        marker_dict['fields']['programs'] = program_list  # Add the programs to the marker dictionary
        marker_list.append(marker_dict)
    return JsonResponse(marker_list, safe=False)

@csrf_exempt
def update_marker(request):
    data = json.loads(request.body)
    marker = Marker.objects.get(pk=data['id'])
    setattr(marker, data['column'], data['value'])
    marker.save()
    return JsonResponse({'status': 'success'})

def generate_code(length=15):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join((random.choice(letters_and_digits) for _ in range(length)))

@user_passes_test(lambda u: u.is_superuser)
def create_code(request):
    code = generate_code()
    email = request.POST.get('email')
    new_code = Code(code=code, email=email, is_valid=True, expires_at=timezone.now() + timezone.timedelta(days=3))
    new_code.save()
    
    send_mail(
        'Your registration code',
        '',
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
        html_message=f'''
            <h1>Your registration code</h1>
            <p>Your registration code is: <strong>{code}</strong></p>
            <p>Make sure you use this email to register at <a href="https://unimap.pythonanywhere.com/verify/">https://unimap.pythonanywhere.com/verify/</a>.</p>
            <p>Please note that this code will expire in 3 days.</p>
        ''',
    )
    
    messages.success(request, 'Code sent successfully.', extra_tags='toast-success')
    return redirect('view_code')

@user_passes_test(lambda u: u.is_superuser)
def view_code(request):
    codes = Code.objects.all()
    return render(request, 'code.html', {'codes': codes})

def view_audit_logs(request):
    logs = AuditLog.objects.all()
    return render(request, 'audit_logs.html', {'logs': logs})

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


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Your password has been reset.', extra_tags='toast-success')
        return redirect('login')

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f" {error}", extra_tags='toast-error')
        return self.render_to_response(self.get_context_data(form=form))

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
            return render(request, 'login.html', {'username': username})

        profile_obj = Profile.objects.filter(user = user_obj).first()

        if not profile_obj.is_verified:
            messages.error(request, 'Profile is not verified, check your email', extra_tags='toast-error')
            return render(request, 'login.html', {'username': username})

        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, 'Wrong Password', extra_tags='toast-error')
            return render(request, 'login.html', {'username': username})

        login(request, user)
        return redirect('/')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))

@unauthenticated_user
def register_attempt(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        code = request.POST.get('code')
        
        code_obj = Code.objects.filter(code=code).first()
    
        if code_obj and code_obj.expires_at < timezone.now():
            code_obj.is_valid = False
            code_obj.save()
        
        if not code_obj or not code_obj.is_valid:
            messages.error(request, 'Invalid or expired code.', extra_tags='toast-error')
            return render(request, 'register.html', {'username': username, 'email': email})
        
        if not code_obj.email == email:
            messages.error(request, 'Email does not match email attached to code.', extra_tags='toast-error')
            return render(request, 'register.html', {'username': username, 'email': email})
        
        code_obj.is_valid = False
        code_obj.save()
           
        try:
            validate_password(password)
        except ValidationError as e:
            for error in e.messages:
                messages.error(request, error, extra_tags='toast-error')
            return render(request, 'register.html', {'username': username, 'email': email})

        try:
            if User.objects.filter(username=username).first():
                messages.error(request, 'Username is taken.', extra_tags='toast-error')
                return render(request, 'register.html', {'username': username, 'email': email})
            if User.objects.filter(email=email).first():
                messages.error(request, 'Email is taken.', extra_tags='toast-error')
                return render(request, 'register.html', {'username': username, 'email': email})
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