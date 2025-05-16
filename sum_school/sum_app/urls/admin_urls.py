from django.urls import path
from sum_app.views import admin_views

app_name = 'sum_admin'

urlpatterns = [
    path('login/', admin_views.show_admin_login, name='show_admin_login'),
    path('login/authenticate/', admin_views.admin_login, name='admin_login'),
    path('logout/', admin_views.admin_logout, name='logout'),

    path('dashboard/', admin_views.admin_dashboard, name='admin_dashboard'),
    path('my-profile/', admin_views.show_admin_profile, name='show_admin_profile'),
    path('my-profile/edit/', admin_views.show_edit_admin_profile, name='show_edit_admin_profile'),
    path('my-profile/update/', admin_views.update_admin_profile, name='update_admin_profile'),
    path('my-profile/email/edit/', admin_views.show_edit_admin_email, name='show_edit_admin_email'),
    path('my-profile/email/update/', admin_views.update_admin_email, name='update_admin_email'),
    path('my-profile/password/edit/', admin_views.show_edit_admin_password, name='show_edit_admin_password'),
    path('my-profile/password/update/', admin_views.update_admin_password, name='update_admin_password'),
]