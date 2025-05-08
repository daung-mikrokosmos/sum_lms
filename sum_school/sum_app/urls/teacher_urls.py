from django.urls import path
from sum_app.views import teacher_views

app_name = 'sum_teacher'

urlpatterns = [
    path('login/', teacher_views.show_teacher_login, name='show_teacher_login'),
    path('dashboard/', teacher_views.teacher_dashboard, name='teacher_dashboard'),
    path('login/authenticate/', teacher_views.teacher_login, name='teacher_login'),
    path('logout/', teacher_views.teacher_logout, name='logout'),
]