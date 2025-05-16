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
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        # Store old email to show in the form if error occurs
        request.session['user_login_email'] = email

        if not email or not password:
            messages.error(request, 'Please enter both email and password.')
            return redirect(reverse('sum_teacher:show_teacher_login'))

        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password) and user.is_teacher:
                request.session['t_id'] = user.user_id
                messages.success(request, f'Welcome back, {user.name}!')
                request.session.pop('user_login_email', None)
                return redirect(reverse('sum_teacher:teacher_dashboard'))
            else:
                messages.error(request, 'Invalid credentials.')
        except User.DoesNotExist:
            messages.error(request, 'Invalid credentials.')

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
