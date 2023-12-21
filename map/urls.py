from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .views import MarkerListView

urlpatterns = [
    path('', views.home, name='home'),
    path('add-marker/', views.add_marker, name='add_marker'),
    path('edit-marker/<int:pk>', views.edit_marker, name='edit_marker'),
    path('view-marker/', MarkerListView.as_view(), name='view_marker'),
    path('delete-marker/<int:pk>', views.delete_marker, name='delete_marker'),
    path('update-marker/', views.update_marker, name='update_marker'),
    path('code/', views.view_code, name='view_code'),
    path('create-code/', views.create_code, name='create_code'),
    path('api/markers', views.get_markers, name='get_markers'),
    path('search-markers/', views.search_markers, name='search_markers'),
    path('logs/', views.view_audit_logs, name='view_audit_logs'),
    path("login/", views.login_attempt, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_attempt, name="register"),
    path("success/", views.success, name="success"),
    path("verify/<auth_token>/", views.verify, name="verify"),
    path("error/", views.verify, name="error"),
    path('password-reset/', views.CustomPasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',views.CustomPasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'), 
    path('password-reset-complete/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)