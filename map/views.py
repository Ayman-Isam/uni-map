from django.shortcuts import render, redirect
from .forms import MarkerForm
from django.http import JsonResponse
from django.core import serializers
from .models import Marker
import json

def home(request):
    return render(request, 'home.html')

def add_marker(request):
    if request.method == 'POST':
        form = MarkerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return render(request, 'add_marker.html', {'form': form})
    else:
        form = MarkerForm()
        return render(request, 'add_marker.html', {'form': form})
    
def get_markers(request):
    markers = Marker.objects.all()
    marker_list = serializers.serialize('json', markers)
    return JsonResponse(json.loads(marker_list), safe=False)