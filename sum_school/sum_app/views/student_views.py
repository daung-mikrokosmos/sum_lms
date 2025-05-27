from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from ..models import User
from ..models import Program
from ..models import Activity
from ..models import Module
from ..models import Task
from ..models import Class
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

# user logout
def student_logout(request):
    request.session.flush()
    messages.success(request, 'You have been logged out successfully.')
    return redirect('sum_student:show_student_login')

# user dashboard
def student_dashboard(request):
    user_id = request.session.get('s_id')
    if not user_id:
        messages.error(request, 'You do not have permission to access the user dashboard.')
        return redirect('sum_student:show_student_login')

    user = User.objects.get(user_id=user_id)
    user_programs = Program.objects.filter(registration__user_id=user_id)
    context = {
        'title': 'user Dashboard',
        'user': user,
        'total_users': User.objects.count(),
        'programs' : user_programs
    }
    return render(request, 'student/dashboard.html', context)


# User Program
def student_program(request,program_id):
    url = reverse('sum_student:activity' , kwargs={'program_id' : program_id})
    return redirect(url)


# User Activity
def student_activity(request,program_id):
    user_id = request.session.get('s_id')
    if not user_id:
        messages.error(request, 'You do not have permission to access this program.')
        return redirect('sum_student:show_student_login')

    user = User.objects.get(user_id=user_id)
    user_activities = Activity.objects.filter(module__program_id=program_id).select_related('module').order_by('-created_at')
    program = Program.objects.get(program_id=program_id)
    context = {
        'title': 'Program Activities',
        'user': user,
        'activities' : user_activities,
        'program' : program
    }
    return render(request,'student/program_details_layout.html' , context)



#Module
def student_module_redirect(request,program_id):
    user_id = request.session.get('s_id')
    if not user_id:
        messages.error(request, 'You do not have permission to access this route.')
        return redirect('sum_student:show_student_login')
    
    modules = Module.objects.filter(program_id=program_id);
    url = reverse('sum_student:module' , kwargs={"program_id" : program_id,"module_code" : modules[0].module_code})
    return redirect(url);

def student_module(request,program_id,module_code):
    user_id = request.session.get('s_id')
    if not user_id:
        messages.error(request, 'You do not have permission to access this route.')
        return redirect('sum_student:show_student_login')
    
    user = User.objects.get(user_id=user_id)
    program = Program.objects.get(program_id=program_id)
    modules = Module.objects.filter(program_id=program_id).select_related('teacher');
    
    # Getting Turorial based on current Module
    currentModule = Module.objects.get(module_code=module_code)
    lessons = currentModule.tasks.filter(type=Task.TaskType.TUTORIAL).select_related('file').order_by('-created_at')
    
    print(lessons)
    
    context = {
        'title': 'Program Modules',
        'user': user,
        'program' : program,
        'modules' : modules,
        'currentmodule' : currentModule,
        'lessons' : lessons
    }
    return render(request,'student/program_details_layout.html',context)


#Assignment
def student_assignment_redirect(request,program_id):
    user_id = request.session.get('s_id')
    if not user_id:
        messages.error(request, 'You do not have permission to access this route.')
        return redirect('sum_student:show_student_login')
    
    modules = Module.objects.filter(program_id=program_id);
    url = reverse('sum_student:assignment' , kwargs={"program_id" : program_id,"module_code" : modules[0].module_code})
    urlWithQueryString = f"{url}?status=all"
    return redirect(urlWithQueryString);

def student_assignment(request,program_id,module_code):
    user_id = request.session.get('s_id')
    if not user_id:
        messages.error(request, 'You do not have permission to access this route.')
        return redirect('sum_student:show_student_login')
    
    statusFilter = request.GET.get('status');
    
    user = User.objects.get(user_id=user_id)
    program = Program.objects.get(program_id=program_id)
    modules = Module.objects.filter(program_id=program_id).select_related('teacher');
    
    # Getting Turorial based on current Module
    currentModule = Module.objects.get(module_code=module_code)
    base_query = currentModule.tasks.filter(type=Task.TaskType.ASSIGNMENT)
    
    if(statusFilter == 'finished'):
        query = base_query.filter(submittedtask__student=user)
    elif statusFilter == 'unfinished':
        query = base_query.exclude(submittedtask__student=user)
    else :
        query = base_query
        
    assignments = query.select_related('file').order_by('-created_at')
    context = {
        'title': 'Program Assignment',
        'user': user,
        'program' : program,
        'modules' : modules,
        'currentmodule' : currentModule,
        'assignments' : assignments,
        'count' : len(assignments),
        'status': statusFilter
    }
    
    return render(request,'student/program_details_layout.html',context)

#Peoeple
def student_people(request,program_id):
    user_id = request.session.get('s_id')
    if not user_id:
        messages.error(request, 'You do not have permission to access this route.')
        return redirect('sum_student:show_student_login')
    
    user = User.objects.get(user_id=user_id)
    program = Program.objects.get(program_id=program_id)
    alluser = User.objects.filter(registration__program_id=program_id);
    
    totalTeacher = alluser.filter(is_teacher=True).count()
    totalStudent = alluser.filter(is_teacher=False).count()
    context = {
        'title': 'Program Participants',
        'user': user,
        'program' : program,
        'alluser' : alluser,
        'totalTeacher' : totalTeacher,
        'totalStudent' : totalStudent
    }
    
    return render(request,'student/program_details_layout.html',context)

#Class Schedule
def student_classes(request,program_id):
    user_id = request.session.get('s_id')
    if not user_id:
        messages.error(request, 'You do not have permission to access this route.')
        return redirect('sum_student:show_student_login')
    
    user = User.objects.get(user_id=user_id)
    program = Program.objects.get(program_id=program_id)
    classes = Class.objects.filter(module__program_id=program_id).select_related('module').order_by('-created_at')

    context = {
        "program": program,
        "user": user,
        "classes": classes,
    }
    
    return render(request,'student/program_details_layout.html',context);
    