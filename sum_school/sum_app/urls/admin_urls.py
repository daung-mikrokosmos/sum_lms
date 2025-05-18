from django.urls import path, include
from sum_app.views import admin_views

app_name = 'sum_admin'

# Profile subpatterns
urlpatterns = [
    # Auth routes
    path('login/', admin_views.show_admin_login, name='show_admin_login'),
    path('login/authenticate/', admin_views.admin_login, name='admin_login'),
    path('logout/', admin_views.admin_logout, name='logout'),

    # Dashboard
    path('dashboard/', admin_views.admin_dashboard, name='admin_dashboard'),

    # Profile routes
    *[
        path('my-profile/', admin_views.show_admin_profile, name='show_admin_profile'),
        path('my-profile/edit/', admin_views.show_edit_admin_profile, name='show_edit_admin_profile'),
        path('my-profile/update/', admin_views.update_admin_profile, name='update_admin_profile'),
        path('my-profile/email/edit/', admin_views.show_edit_admin_email, name='show_edit_admin_email'),
        path('my-profile/email/update/', admin_views.update_admin_email, name='update_admin_email'),
        path('my-profile/password/edit/', admin_views.show_edit_admin_password, name='show_edit_admin_password'),
        path('my-profile/password/update/', admin_views.update_admin_password, name='update_admin_password'),
    ],

    # Program
    *[
        path('program/<int:program_id>/dashboard/', admin_views.program_dashboard, name='program_dashboard'),
        path('program/<int:program_id>/students/', admin_views.program_students, name='program_students'),
        path('program/<int:program_id>/teachers/', admin_views.program_teachers, name='program_teachers'),
        path('program/<int:program_id>/users/', admin_views.program_users, name='program_users'),
        path('program/<int:program_id>/activities', admin_views.program_activities, name='program_activities'),
    ]
]
