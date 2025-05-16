from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from ..models import User
from django.contrib.auth.hashers import check_password

# user login view
def show_student_login(request):
    if request.session.get('s_id'):
        return redirect(reverse('sum_student:student_dashboard'))
    return render(request, 'auth/user_login.html')

# user login
def student_login(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        # Store email in session to prefill form if error occurs
        request.session['user_login_email'] = email

        if not email or not password:
            messages.error(request, 'Please enter both email and password.')
            return redirect(reverse('sum_student:show_student_login'))

        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password) and not user.is_teacher:
                request.session['s_id'] = user.user_id
                messages.success(request, f'Welcome back, {user.name}!')
                request.session.pop('user_login_email', None)  # Clear old email
                return redirect(reverse('sum_student:student_dashboard'))
            else:
                messages.error(request, 'Invalid credentials.')
        except User.DoesNotExist:
            messages.error(request, 'Invalid credentials.')

    return redirect(reverse('sum_student:show_student_login'))

# user dashboard
def student_dashboard(request):
    user_id = request.session.get('s_id')
    if not user_id:
        messages.error(request, 'You do not have permission to access the user dashboard.')
        return redirect('sum_student:show_student_login')

    user = User.objects.get(user_id=user_id)
    context = {
        'title': 'user Dashboard',
        'user': user,
        'total_users': User.objects.count(),
    }
    return render(request, 'student/dashboard.html', context)

# user logout
def student_logout(request):
    request.session.flush()
    messages.success(request, 'You have been logged out successfully.')
    return redirect('sum_student:show_student_login')
