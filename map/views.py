from django.shortcuts import render, redirect, get_object_or_404
from .forms import MarkerForm
from django.http import JsonResponse
from django.core import serializers
from .models import Marker
from django.views.decorators.csrf import csrf_exempt
import json

def home(request):
    return render(request, 'home.html')

def add_marker(request):
    markers = Marker.objects.all()
    if request.method == 'POST':
        form = MarkerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_marker')  
    else:
        form = MarkerForm()
    return render(request, 'add_marker.html', {'form': form, 'markers': markers})
    
def get_markers(request):
    markers = Marker.objects.all()
    marker_list = serializers.serialize('json', markers)
    return JsonResponse(json.loads(marker_list), safe=False)

def delete_marker(request, pk):
    marker = get_object_or_404(Marker, pk=pk)
    marker.delete()
    return redirect('add_marker')

@csrf_exempt
def update_marker(request):
    data = json.loads(request.body)
    marker = Marker.objects.get(pk=data['id'])
    setattr(marker, data['column'], data['value'])
    marker.save()
    return JsonResponse({'status': 'success'})