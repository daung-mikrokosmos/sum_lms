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
    path('dashboard/users/', admin_views.show_all_people, name='show_all_people'),
    path('dashboard/users/create/', admin_views.show_create_user, name='show_create_user'),
    path('dashboard/users/create/submit/', admin_views.create_user, name='create_user'),

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
        path('program/create', admin_views.show_create_program, name='show_create_program'),
        path('program/create/submit', admin_views.create_program, name='create_program'),

        path('program/<int:program_id>/dashboard/', admin_views.program_dashboard, name='program_dashboard'),
        path('program/<int:program_id>/students/', admin_views.program_students, name='program_students'),
        path('program/<int:program_id>/teachers/', admin_views.program_teachers, name='program_teachers'),
        path('program/<int:program_id>/people/', admin_views.program_users, name='program_users'),
        path('program/<int:program_id>/activities', admin_views.program_activities, name='program_activities'),
        path('program/<int:program_id>/classes', admin_views.program_classes, name='program_classes'),
        path('program/<int:program_id>/leaves', admin_views.program_leaves, name='program_leaves'),
        path('program/<int:program_id>/leaves/<int:leave_id>/details/', admin_views.leave_details, name='leave_details'),
        
        path('program/<int:program_id>/leave/<int:leave_id>/approve/', admin_views.approve_leave, name='approve_leave'),
        path('program/<int:program_id>/class/<int:class_id>/cancel/', admin_views.cancel_class, name='cancel_class'),
        path('program/<int:program_id>/class/<int:class_id>/rolecalls/', admin_views.show_rolecalls, name='show_rolecalls'),
        path('program/<int:program_id>/class/<int:class_id>/rolecalls/<int:user_id>/mark/<int:status>', admin_views.mark_rolecall, name='mark_rolecall'),
        
        path('program/<int:program_id>/user/register', admin_views.show_user_register, name='show_user_register'),
        path(
            'program/<int:program_id>/user/<int:user_id>/register/<str:teacher_flag>/<str:scholared>/',
            admin_views.register_user,
            name='register_user'
        ),
        path('program/<int:program_id>/user/remove/<int:user_id>', admin_views.remove_user, name="remove_user"),
        
        path('program/<int:program_id>/modules', admin_views.program_modules, name="program_modules"),
        path('program/<int:program_id>/module/create', admin_views.show_create_module, name='show_create_module'),
        path('program/<int:program_id>/module/create/submit', admin_views.create_module, name="create_module"),
        
        path('program/<int:program_id>/class/create', admin_views.show_create_class, name="show_create_class"),
        path('program/<int:program_id>/class/create/submit', admin_views.create_class, name="create_class"),
    ]
]
