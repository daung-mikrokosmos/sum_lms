"""
URL configuration for sum_school project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from sum_app.views import main_views, admin_views
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/welcome', permanent=False)),
    path('welcome', main_views.welcome, name='welcome'),
    path('admin/', include('sum_app.urls.admin_urls', namespace='sum_admin')),
    path('student/', include('sum_app.urls.student_urls', namespace='sum_student')),
    path('django-admin/', admin.site.urls),  # Django's built-in admin
]
