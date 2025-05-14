from django.urls import path
from sum_app.views import admin_views

app_name = 'sum_admin'

urlpatterns = [
    path('login/', admin_views.show_admin_login, name='show_admin_login'),
    path('login/authenticate/', admin_views.admin_login, name='admin_login'),
    path('logout/', admin_views.admin_logout, name='logout'),

    path('dashboard/', admin_views.admin_dashboard, name='admin_dashboard'),
    path('my-profile/', admin_views.show_admin_profile, name='show_admin_profile'),
]