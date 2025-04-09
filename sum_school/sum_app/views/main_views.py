from django.shortcuts import render, redirect
from django.urls import reverse

def welcome(request):
    """Welcome view for the LMS homepage"""
    # Redirect authenticated staff users to admin dashboard
    if request.user.is_authenticated and request.user.is_staff:
        return redirect(reverse('sum_admin:admin_dashboard'))

    return render(request, 'welcome.html', {
        'title': 'SUM',
        'page_title': 'WARMLY WELCOME TO SUM',
        'welcome_message': 'Welcome to Spring University Myanmar'
    })
