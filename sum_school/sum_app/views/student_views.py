from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from ..models import User
from django.contrib.auth.hashers import check_password

# user login view
def show_login(request):
    if request.session.get('user_id'):
        return redirect(reverse('sum_student:student_dashboard'))
    return render(request, 'student/login.html')

# user login
def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password) and user.is_teacher == False:
                # Log the user in manually using session
                request.session['user_id'] = user.user_id
                messages.success(request, f'Welcome back, {user.name}!')
                return redirect(reverse('sum_student:student_dashboard'))
            else:
                messages.error(request, 'Invalid credentials.')
        except User.DoesNotExist:
            messages.error(request, 'No user account found with this email.')

    return redirect(reverse('sum_student:show_login'))

# user dashboard
def student_dashboard(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, 'You do not have permission to access the user dashboard.')
        return redirect('sum_student:show_login')

    user = User.objects.get(user_id=user_id)
    context = {
        'title': 'user Dashboard',
        'user': user,
        'total_users': User.objects.count(),
    }
    return render(request, 'student/dashboard.html', context)

# user logout
def user_logout(request):
    request.session.flush()
    messages.success(request, 'You have been logged out successfully.')
    return redirect('sum_student:show_login')
