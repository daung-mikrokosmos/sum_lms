from django.urls import path
from sum_app.views import teacher_views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'sum_teacher'

urlpatterns = [
    path('login/', teacher_views.show_teacher_login, name='show_teacher_login'),
    path('dashboard/', teacher_views.teacher_dashboard, name='teacher_dashboard'),
    path('login/authenticate/', teacher_views.teacher_login, name='teacher_login'),
    path('logout/', teacher_views.teacher_logout, name='logout'),
    path('my-profile/', teacher_views.teacher_profile, name='teacher_profile'),
    path('my-profile/update', teacher_views.teacher_userdata_update, name='updateuserdata'),
    path('my-profile/updatepassword', teacher_views.teacher_update_password, name='updatepassword'),
    
    path('programs/<int:program_id>/module/', teacher_views.module_redirect, name='module_redirect'),
    path('programs/<int:program_id>/module/lesson/<str:module_code>', teacher_views.program_module, name='program_module'),
    path('programs/<int:program_id>/module/create', teacher_views.show_tutorial_create, name='show_turorial_create'),
    path('programs/<int:program_id>/module/create/submit/', teacher_views.create_tutorial, name='create_tutorial'),
    path('programs/<int:program_id>/module/<int:task_id>/details', teacher_views.program_tutorial_details, name='show_turorial_details'),
    
    path('programs/<int:program_id>/classes/', teacher_views.program_classes, name='program_classes'),
    
    
    path('programs/<int:program_id>/activities', teacher_views.program_activities, name='program_activities'),
    path('programs/<int:program_id>/activities/create/', teacher_views.show_create_activity, name='show_create_activity'),
    path('programs/<int:program_id>/activities/create/submit/', teacher_views.create_activity, name='create_activity'),
    
    path('programs/<int:program_id>/people', teacher_views.program_users, name='program_users'),
    
    path('programs/<int:program_id>/assignments/', teacher_views.show_assignments, name='show_assignments'),
    path('programs/<int:program_id>/assignments/create/', teacher_views.show_create_assignment, name='show_create_assignment'),
    path('programs/<int:program_id>/assignments/create/submit/', teacher_views.create_assignment, name='create_assignment'),
    path('programs/<int:program_id>/assignments/<int:task_id>/details/', teacher_views.show_assignment_details, name='show_assignment_details'),
    path('programs/<int:program_id>/assignments/score', teacher_views.give_score, name='give_score'),
    
    path('programs/<int:program_id>/my-profile', teacher_views.program_profile, name='program_profile'),
    path('programs/<int:program_id>/my-profile/edit/', teacher_views.show_edit_nickname, name='show_edit_nickname'),
    path('programs/<int:program_id>/my-profile/edit/submit/', teacher_views.update_nickname, name='update_nickname'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)