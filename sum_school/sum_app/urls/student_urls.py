from django.urls import path
from sum_app.views import student_views

app_name = 'sum_student'

urlpatterns = [
    path('login/', student_views.show_student_login, name='show_student_login'),
    path('login/authenticate/', student_views.student_login, name='student_login'),
    path('logout/', student_views.student_logout, name='logout'),
    
    
    path('dashboard/', student_views.student_dashboard, name='student_dashboard'),
    
    *[
        path('program/<int:program_id>', student_views.student_program , name='program'),
        path('program/<int:program_id>/activity', student_views.student_activity , name='activity'),
        
        path('program/<int:program_id>/module', student_views.student_module_redirect , name='module_redirect'),
        path('program/<int:program_id>/module/<str:module_code>', student_views.student_module , name='module'),
        
        path('program/<int:program_id>/assignment', student_views.student_assignment_redirect , name='assignment_redirect'),
        path('program/<int:program_id>/assignment/<str:module_code>', student_views.student_assignment , name='assignment'),
        
        path('program/<int:program_id>/people', student_views.student_people , name='people'),
        
        path('program/<int:program_id>/classes', student_views.student_classes , name='classes'),
        
        path('program/<int:program_id>/leave', student_views.student_leave , name='leave'),
        path('program/<int:program_id>/leaveform', student_views.student_leaveform , name='leaveform'),
        path('program/<int:program_id>/leaveform/submit', student_views.student_leave_create , name='leavecreate'),
    ]
]