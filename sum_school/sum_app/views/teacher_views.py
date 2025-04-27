from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from ..models import User
from django.contrib.auth.hashers import check_password

# user login view
def show_teacher_login(request):
    if request.session.get('t_id'):
        return redirect(reverse('sum_teacher:teacher_dashboard'))
    return render(request, 'auth/user_login.html')

# user login
def teacher_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password) and user.is_teacher == True:
                # Log the user in manually using session
                request.session['t_id'] = user.user_id
                messages.success(request, f'Welcome back, {user.name}!')
                return redirect(reverse('sum_teacher:teacher_dashboard'))
            else:
                messages.error(request, 'Invalid credentials.')
        except User.DoesNotExist:
            messages.error(request, 'No user account found with this email.')

    return redirect(reverse('sum_teacher:show_teacher_login'))

# user dashboard
def teacher_dashboard(request):
    teacher_id = request.session.get('t_id')
    if not teacher_id:
        messages.error(request, 'You do not have permission to access the user dashboard.')
        return redirect('sum_teacher:show_teacher_login')

    user = User.objects.get(user_id=teacher_id)
    context = {
        'title': 'user Dashboard',
        'user': user,
        'total_users': User.objects.count(),
    }
    return render(request, 'teacher/dashboard.html', context)

# user logout
def teacher_logout(request):
    request.session.flush()
    messages.success(request, 'You have been logged out successfully.')
    return redirect('sum_teacher:show_teacher_login')
