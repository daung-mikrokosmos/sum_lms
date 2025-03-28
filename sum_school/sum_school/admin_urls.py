from django.urls import path
from sum_app import views


urlpatterns = [
    path('login/', views.show_admin_login, name='show_admin_login'),
    path('admin_login/', views.admin_login, name='admin_login'),
]
