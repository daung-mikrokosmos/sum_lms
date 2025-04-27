from django.urls import path
from sum_app.views import student_views

app_name = 'sum_student'

urlpatterns = [
    path('login/', student_views.show_student_login, name='show_student_login'),
    path('login/authenticate/', student_views.student_login, name='student_login'),
    path('dashboard/', student_views.student_dashboard, name='student_dashboard'),
    path('logout/', student_views.student_logout, name='logout'),
]