from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User

def welcome(request):
    """Welcome view for the LMS homepage"""
    return render(request, 'welcome.html', {
        'title': 'SUM',
        'page_title': 'WARMLY WELCOME TO SUM',
        'welcome_message': 'Welcome to Spring University Myanmar'
    })

def show_admin_login(request):
    """Admin login view"""
    return render(request, 'admin/admin_login.html')

def admin_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # Check if the user exists
        try:
            user = User.objects.get(email=email)
            if user.is_admin:  # Check if it's an admin user
                # Authenticate the user
                user = authenticate(request, username=user.username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('admin_dashboard')  # Redirect to your admin dashboard or home page
                else:
                    messages.error(request, 'Invalid password.')
            else:
                messages.error(request, 'You are not authorized to log in as an admin.')
        except User.DoesNotExist:
            messages.error(request, 'No account found with this email.')

    return render(request, 'admin_login.html')
