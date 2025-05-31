from django.urls import path
from sum_app.views import student_views

app_name = 'sum_student'

urlpatterns = [
    path('login/', student_views.show_student_login, name='show_student_login'),
    path('login/authenticate/', student_views.student_login, name='student_login'),
    path('logout/', student_views.student_logout, name='logout'),
    
    
    path('dashboard/', student_views.student_dashboard, name='student_dashboard'),
    
    *[
        path('programs/<int:program_id>', student_views.student_program , name='program'),
        path('programs/<int:program_id>/activity', student_views.student_activity , name='activity'),
        
        path('programs/<int:program_id>/module', student_views.student_module_redirect , name='module_redirect'),
        path('programs/<int:program_id>/module/lesson/<str:module_code>', student_views.student_module , name='module'),
        path('programs/<int:program_id>/module/<int:task_id>/details', student_views.student_tutorial_details, name='show_turorial_details'),

        
        path('programs/<int:program_id>/assignment', student_views.student_assignment_redirect , name='assignment_redirect'),
        path('programs/<int:program_id>/assignment/module/<str:module_code>', student_views.student_assignment , name='assignment'),
        path('programs/<int:program_id>/assignments/<int:task_id>/details/', student_views.show_assignment_details, name='show_assignment_details'),
        path('programs/<int:program_id>/assignments/<int:task_id>/submit', student_views.submit_assignment, name='submit_assignment'),
        
        path('programs/<int:program_id>/people', student_views.student_people , name='people'),
        
        path('programs/<int:program_id>/classes', student_views.student_classes , name='classes'),
        
        path('programs/<int:program_id>/leave', student_views.student_leave , name='leave'),
        path('programs/<int:program_id>/leaveform', student_views.student_leaveform , name='leaveform'),
        path('programs/<int:program_id>/leaveform/submit', student_views.student_leave_create , name='leavecreate'),
        
        path('programs/<int:program_id>/my-profile', student_views.program_profile , name='program_profile'),
        path('programs/<int:program_id>/my-profile/edit', student_views.show_edit_nickname , name='show_edit_nickname'),
        path('programs/<int:program_id>/my-profile/edit/submit', student_views.update_nickname , name='update_nickname'),
    ],
    
    *[
        path('profile' ,student_views.student_profile,name='profile'),
        path('profile/update' ,student_views.student_update_userdata,name='updateuserdata'),
        path('profile/updatepassword' ,student_views.student_update_password,name='updatepassword'),
    ]
]