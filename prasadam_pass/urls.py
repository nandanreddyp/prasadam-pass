"""
URL configuration for prasadam_pass project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from .views import home, event_registration, show_qr, scan_qr, process_qr_checkin, download_qr

urlpatterns = [
    path('admin', admin.site.urls),
    path('login', auth_views.LoginView.as_view(template_name='volunteer/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('', home, name='home'),
    path('event/<int:event_id>', event_registration, name='event_registration'),
    path('qr/<str:token>', show_qr, name='show_qr'),
    path('qr/download/<str:token>', download_qr, name='download_qr'),
    path('scan', scan_qr, name='scan_qr'),
    path('checkin/<str:token>', process_qr_checkin, name='process_qr_checkin')
]
