from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from ..models import User
from ..models import Program
from ..models import Activity
from ..models import Module
from ..models import Task
from ..models import Class
from ..models import Leave
from ..models import Registration
import re
from django.contrib.auth.hashers import check_password, make_password
from datetime import datetime

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
    currentModule = Module.objects.get(
        module_code=module_code,
        program_id=program_id
    )
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
    alluser = Registration.objects.filter(
        program_id=program_id,
        deleted_at__isnull=True
    ).select_related('user').order_by('created_at')
    
    totalTeacher = alluser.filter(teacher_flag=True).count()
    totalStudent = alluser.filter(teacher_flag=False).count()
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
        'title': 'Program Schedule',
        "program": program,
        "user": user,
        "classes": classes,
    }
    
    return render(request,'student/program_details_layout.html',context);


#Leave Page
def student_leave(request,program_id):
    user_id = request.session.get('s_id')
    if not user_id:
        messages.error(request, 'You do not have permission to access this route.')
        return redirect('sum_student:show_student_login')
    
    user = User.objects.get(user_id=user_id)
    program = Program.objects.get(program_id=program_id)
    leaverecords = Leave.objects.filter(program=program,user=user).order_by('-created_at')
    
    context = {
        'title': 'Program Leave',
        'user' : user,
        'program' : program,
        "leaverecords" : leaverecords,
    }
    
    return render(request,'student/program_details_layout.html',context)
    
    
def student_leaveform(request,program_id):
    user_id = request.session.get('s_id')
    if not user_id:
        messages.error(request, 'You do not have permission to access this route.')
        return redirect('sum_student:show_student_login')
    
    user = User.objects.get(user_id=user_id)
    program = Program.objects.get(program_id=program_id)
    
    context = {
        'title': 'Program Leave Apply',
        'user' : user,
        'program' : program,
    }
    
    return render(request,'student/program_details_layout.html',context)  

def student_leave_create(request,program_id):
    user_id = request.session.get('s_id')
    if not user_id:
        messages.error(request, 'You do not have permission to access this route.')
        return redirect('sum_student:show_student_login')
    
    user = User.objects.get(user_id=user_id)
    program = Program.objects.get(program_id=program_id)
    
    context = {
        'title': 'Program Leave Apply',
        'user' : user,
        'program' : program,
    }
    
    if request.method == "POST":
        reason = request.POST.get("reason", "").strip()
        start_date_str = request.POST.get("start_date", "").strip()
        end_date_str = request.POST.get("end_date", "").strip()
        errors = {}
        
        if not reason:
            errors["reason"] = "Leave reason is required."
        
        # Parse and validate start_time
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        except Exception:
            start_date = None
            errors["start_date"] = "Invalid start date format."

        if not start_date:
            errors["start_date"] = "Start date is required or invalid."

        # Parse and validate end_time
        try:
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        except Exception:
            end_date = None
            errors["end_date"] = "Invalid end date format."

        if not end_date:
            errors["end_date"] = "End date is required or invalid."

        # Logical validation
        if start_date and end_date and start_date > end_date:
            errors["end_date"] = "End date must be after start time."
        
        if start_date < datetime.now().date():
            errors['start_date'] = 'Start date must be today or later!'
        
        if errors:
            for field in ['reason', 'start_date', 'end_date']:
                if errors.get(field):
                    messages.error(request, errors[field])
            url = reverse('sum_student:leaveform' , kwargs={"program_id" : program_id})
            return redirect(url)    
        
        leave = Leave(
            start_date = start_date,
            end_date = end_date,
            reason = reason,
            program_id = program_id,
            user_id = user_id,
            approve_status = False
        )     
        leave.save()
        messages.success(request,'Apply leave request success!')
        return redirect('sum_student:leave', program_id=program_id)
        
    url = reverse('sum_student:leaveform' , kwargs={"program_id" : program_id})
    return redirect(url)
    
#profile
def student_profile(request):
    user_id = request.session.get('s_id')
    if not user_id:
        messages.error(request, 'You do not have permission to access this route.')
        return redirect('sum_student:show_student_login')
    
    user = User.objects.get(user_id=user_id)
    
    context = {
        'title': 'Profile',
        'user' : user,
    }
    return render(request,'student/profile/profile.html' , context)

def student_update_userdata(request):
    user_id = request.session.get('s_id')
    if not user_id:
        messages.error(request, 'You do not have permission to access this route.')
        return redirect('sum_student:show_student_login')
    
    user = User.objects.get(user_id=user_id)
    
    if request.method == 'POST':
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        changed = False
        
        if name and name != user.name:
            user.name = name
            changed = True
        
        if email and email != user.email:
            user.email = email
            changed = True
        
        if changed:
            user.save()
            messages.success(request,'Update User data Successful!')
            return redirect('sum_student:profile')
            
    
    return redirect('sum_student:profile')


def student_update_password(request):
    user_id = request.session.get('s_id')
    if not user_id:
        messages.error(request, 'You do not have permission to access this route.')
        return redirect('sum_student:show_student_login')
    
    user = User.objects.get(user_id=user_id)
    
    def givemessageandredirect(text,type):
        if(type == 'error'): messages.error(request,text)
        if(type == 'success'): messages.success(request,text)
        return redirect('sum_student:profile')
        
    
    if request.method == 'POST':
        current_password = request.POST.get("current-password", "").strip()
        password = request.POST.get("password", "").strip()
        confirm_password = request.POST.get("confirm-password", "").strip()
        print(current_password,password,confirm_password)
        
        # Password validation
        if not current_password:
            return givemessageandredirect('Please Enter Current Passowrd','error')

        if not password:
            return givemessageandredirect('Please Enter Password','error')

        if not confirm_password:
            return givemessageandredirect('Please Enter Confirm Password','error')

        if current_password and not check_password(current_password, user.password):
            return givemessageandredirect('Incorrect Current Password! Try Again!','error')

        if password:
            if len(password) < 8 or len(password) > 24:
                return givemessageandredirect('Password must be between 8 and 24 characters','error')
            elif not re.search(r"[A-Z]", password):
                return givemessageandredirect("Password must contain at least 1 uppercase letter.",'error')
            elif not re.search(r"\d", password):
                return givemessageandredirect("Password must contain at least 1 number.",'error')

        if password and confirm_password and password != confirm_password:
            return givemessageandredirect('Passwords and Confirm Password do not match.','error')
        
        user.password = make_password(password)
        user.save()
        return givemessageandredirect('Password updated successfully.','success')
        
    return redirect('sum_student:profile')

# show program profile
def program_profile(request, program_id):
    user_id = request.session.get('s_id')
    if not user_id:
        messages.error(request, 'You do not have permission to access this route.')
        return redirect('sum_student:show_student_login')

    user = User.objects.get(user_id=user_id)
    registration = Registration.objects.filter(
        program_id=program_id,
        user_id=user_id,
        teacher_flag=False,
        deleted_at__isnull=True
    ).first()
    program = Program.objects.get(program_id=program_id)

    context = {
        "program": program,
        "user": user,
        "registration": registration,
    }
    return render(request, "student/program/profile.html", context)

# show edit nickname
def show_edit_nickname(request, program_id):
    user_id = request.session.get('s_id')
    if not user_id:
        messages.error(request, 'You do not have permission to access this route.')
        return redirect('sum_student:show_student_login')

    user = User.objects.get(user_id=user_id)
    registration = Registration.objects.filter(
        program_id=program_id,
        user_id=user_id,
        teacher_flag=False,
        deleted_at__isnull=True
    ).first()
    program = Program.objects.get(program_id=program_id)

    context = {
        "program": program,
        "user": user,
        "registration": registration,
    }
    return render(request, "student/program/edit_nickname.html", context)

# update nickname
def update_nickname(request, program_id):
    user_id = request.session.get('s_id')
    if not user_id:
        messages.error(request, 'You do not have permission to access this route.')
        return redirect('sum_student:show_student_login')

    user = User.objects.get(user_id=user_id)
    registration = Registration.objects.filter(
        program_id=program_id,
        user_id=user_id,
        teacher_flag=False,
        deleted_at__isnull=True
    ).first()
    program = Program.objects.get(program_id=program_id)
    
    if request.method == "POST":
        nickname = request.POST.get("nickname", "").strip()
        errors = {}

        # Validation
        if not nickname:
            errors["nickname"] = "nickname is required."
        elif len(nickname) > 50:
            errors["nickname"] = "nickname must not exceed 50 characters."
        elif not re.match(r'^[a-zA-Z0-9_ ]*$', nickname):
            errors["nickname"] = "Nickname must not contain special characters."

        if errors:
            return render(
                request,
                "student/program/edit_nickname.html",
                {
                    "program": program,
                    "user": user,
                    "registration": registration,
                    "form_data": {"nickname": nickname},
                    "errors": errors,
                },
            )

        # Save if no errors
        registration.nickname = nickname
        registration.save()
        messages.success(request, "Profile updated successfully.")
        return redirect("sum_student:program_profile", program_id=program.program_id)

    return redirect("sum_student:show_edit_nickname", program_id=program_id)

