from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add-marker/', views.add_marker, name='add_marker'),
    path('add-marker/delete/<int:pk>', views.delete_marker, name='delete_marker'),
    path('update-marker/', views.update_marker, name='update_marker'),
    path('api/markers', views.get_markers, name='get_markers'),
]