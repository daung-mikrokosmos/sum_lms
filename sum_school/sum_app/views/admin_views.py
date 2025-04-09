from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse

def show_admin_login(request):
    """Admin login view"""
    if request.user.is_authenticated and request.user.is_staff:
        return redirect(reverse('sum_admin:admin_dashboard'))
    return render(request, 'admin/admin_login.html')

def admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            if user.is_staff:  # Check if user has staff permissions
                user = authenticate(request, username=user.username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Welcome back, admin!')
                    return redirect(reverse('sum_admin:admin_dashboard'))
                else:
                    messages.error(request, 'Invalid password.')
            else:
                messages.error(request, 'You are not authorized to log in as an admin.')
        except User.DoesNotExist:
            messages.error(request, 'No account found with this email.')

    return redirect(reverse('sum_admin:show_admin_login'))

@login_required(login_url='sum_admin:show_admin_login')
def admin_dashboard(request):
    """Admin dashboard view"""
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('welcome')

    context = {
        'title': 'Admin Dashboard',
        'total_users': User.objects.count(),
    }
    return render(request, 'admin/dashboard.html', context)

@login_required(login_url='sum_admin:show_admin_login')
def admin_logout(request):
    """Handle admin logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('welcome')
