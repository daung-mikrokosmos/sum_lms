from django.urls import path
from sum_app.views import student_views

app_name = 'sum_student'

urlpatterns = [
    path('login/', student_views.show_login, name='show_login'),
    path('dashboard/', student_views.student_dashboard, name='student_dashboard'),
    path('login/authenticate/', student_views.user_login, name='user_login'),
    path('logout/', student_views.user_logout, name='logout'),
]
