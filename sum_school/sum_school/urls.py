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
from sum_app.views import main_views
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/welcome', permanent=False)),
    path('welcome', main_views.welcome, name='welcome'),
    path('register', main_views.show_register, name='show_register'),
    path('admin/', include('sum_app.urls.admin_urls', namespace='sum_admin')),
    path('student/', include('sum_app.urls.student_urls', namespace='sum_student')),
    path('teacher/', include('sum_app.urls.teacher_urls', namespace='sum_teacher')),
    path('django-admin/', admin.site.urls),  # Django's built-in admin
    
    # UI
    path('dashboard/' , main_views.dashboard , name='dashboard'),
    path('dashboard/<str:course_id>/' , main_views.programDetails , name='program'),
    path('dashboard/<str:course_id>/activity/' , main_views.activity , name='activity'),
    path('dashboard/<str:course_id>/activity/create' , main_views.activityCreate , name='activity_create'),
    path('dashboard/<str:course_id>/module/' , main_views.moduleRedirect , name='moduleRedirect' ),
    path('dashboard/<str:course_id>/module/<int:m>/' , main_views.module, name='module' ),
    path('dashboard/<str:course_id>/module/upload' , main_views.moduleUploadLesson , name='upload_lesson' ),
    path('dashboard/<str:course_id>/assignment/' , main_views.assignmentRedirect),
    path('dashboard/<str:course_id>/assignment/<int:m>' , main_views.assignment , name='assignment'),
    path('dashboard/<str:course_id>/assignment/<int:m>/<str:assignment_id>' , main_views.assignmentDetails , name='assignment_details'),
    path('dashboard/<str:course_id>/people' , main_views.people , name='people'),
    path('dashboard/<str:course_id>/classes' , main_views.classes , name='classes'),
]
