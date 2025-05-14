from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from ..models.admin import Admin
from ..models.program import Program
from django.contrib.auth.hashers import check_password

# admin login view
def show_admin_login(request):
    if request.session.get('admin_id'):
        return redirect(reverse('sum_admin:admin_dashboard'))
    return render(request, 'auth/admin_login.html')

# admin login
def admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email)
        print(password)

        try:
            admin = Admin.objects.get(email=email)
            print(admin)
            if check_password(password, admin.password):
                # Log the admin in manually using session
                request.session['admin_id'] = admin.admin_id
                messages.success(request, f'Welcome back, {admin.name}!')
                return redirect(reverse('sum_admin:admin_dashboard'))
            else:
                messages.error(request, 'Invalid credentials.')
        except Admin.DoesNotExist:
            messages.error(request, 'No admin account found with this email.')

    return redirect(reverse('sum_admin:show_admin_login'))

# admin dashboard
def admin_dashboard(request):
    admin_id = request.session.get('admin_id')
    if not admin_id:
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('sum_admin:show_admin_login')

    admin = Admin.objects.get(admin_id=admin_id)
    programs = Program.objects.all()
    context = {
        'programs': programs,
        'admin': admin,
    }
    return render(request, 'admin/dashboard.html', context)

# admin logout
def admin_logout(request):
    request.session.flush()
    messages.success(request, 'You have been logged out successfully.')
    return redirect('sum_admin:show_admin_login')

# show admin profile
def show_admin_profile(request):
    admin_id = request.session.get('admin_id')
    if not admin_id:
        messages.error(request, 'You do not have permission to access the admin profile.')
        return redirect('sum_admin:show_admin_login')

    admin = Admin.objects.get(admin_id=admin_id)
    context = {
        'admin': admin,
    }
    return render(request, 'admin/profile/profile.html', context)