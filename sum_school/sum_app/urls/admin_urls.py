from django.urls import path
from sum_app.views import admin_views

app_name = 'sum_admin'

urlpatterns = [
    path('login/', admin_views.show_admin_login, name='show_admin_login'),
    path('dashboard/', admin_views.admin_dashboard, name='admin_dashboard'),
    path('login/authenticate/', admin_views.admin_login, name='admin_login'),
    path('logout/', admin_views.admin_logout, name='logout'),
]
