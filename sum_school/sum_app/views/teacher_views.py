from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from ..models.program import Program
from ..models import User
from django.contrib.auth.hashers import check_password, make_password
from django.db.models import Prefetch
from ..models.registration import Registration
from ..models.module import Module
from ..models.module_class import Class
from ..models.rolecall import RoleCall
from ..models.activity import Activity
from ..models.file import File
from django.utils.dateparse import parse_date
from ..models.task import Task
from ..models.submitted_task import SubmittedTask
from ..models.submitted_file import SubmittedFile
from ..models.registration import Registration
import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.utils.text import slugify
from datetime import date
import secrets
from django.db.models import Subquery
import re

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
    programs = Program.objects.filter(
        registration__user_id=teacher_id,
    )
    context = {
        'user': user,
        'programs': programs,
    }
    return render(request, 'teacher/dashboard.html', context)

# user logout
def teacher_logout(request):
    request.session.flush()
    messages.success(request, 'You have been logged out successfully.')
    return redirect('sum_teacher:show_teacher_login')

# user profile
def teacher_profile(request):
    teacher_id = request.session.get('t_id')
    if not teacher_id:
        messages.error(request, 'You do not have permission to access the user profile.')
        return redirect('sum_teacher:show_teacher_login')

    user = User.objects.get(user_id=teacher_id)
    context = {
        'user': user,
    }
    return render(request, 'teacher/profile.html', context)

def teacher_userdata_update(request):
    user_id = request.session.get('t_id')
    if not user_id:
        messages.error(request, 'You do not have permission to access this route.')
        return redirect('sum_teacher:show_teacher_login')
    
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
            return redirect('sum_teacher:teacher_profile')
            
    
    return redirect('sum_teacher:teacher_profile')


def teacher_update_password(request):
    user_id = request.session.get('t_id')
    if not user_id:
        messages.error(request, 'You do not have permission to access this route.')
        return redirect('sum_teacher:show_student_login')
    
    user = User.objects.get(user_id=user_id)
    
    def givemessageandredirect(text,type):
        if(type == 'error'): messages.error(request,text)
        if(type == 'success'): messages.success(request,text)
        return redirect('sum_teacher:teacher_profile')
        
    
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
        
    return redirect('sum_student:teacher_profile')

# show modules
def program_dashboard(request, program_id):
    teacher_id = request.session.get('t_id')
    if not teacher_id:
        messages.error(request, 'You do not have permission to access the user profile.')
        return redirect('sum_teacher:show_teacher_login')

    program = Program.objects.get(program_id=program_id)
    user = User.objects.get(user_id=teacher_id)
    
    modules = Module.objects.filter(program=program).select_related('teacher').prefetch_related(
        Prefetch(
            'teacher__registration_set',
            queryset=Registration.objects.filter(program=program),
            to_attr='filtered_registrations'
        )
    ).order_by('-module_code')
    
    context = {
        "user": user,
        "program": program,
        "modules": modules,
    }
    return render(request, "teacher/program/dashboard.html", context)

# program classes
def program_classes(request, program_id):
    teacher_id = request.session.get('t_id')
    if not teacher_id:
        messages.error(request, 'You do not have permission to access the user profile.')
        return redirect('sum_teacher:show_teacher_login')

    program = Program.objects.get(program_id=program_id)
    user = User.objects.get(user_id=teacher_id)

    # Get all classes in this program
    classes = Class.objects.filter(module__program=program).select_related('module').order_by('-start_time')

    context = {
        "program": program,
        "user": user,
        "classes": classes,
    }
    return render(request, "teacher/program/classes.html", context)

def show_rolecalls(request, program_id, class_id):
    teacher_id = request.session.get('t_id')
    if not teacher_id:
        messages.error(request, 'You do not have permission to access the user profile.')
        return redirect('sum_teacher:show_teacher_login')

    user = User.objects.get(user_id=teacher_id)
    program = Program.objects.get(program_id=program_id)
    students = Registration.objects.filter(
        program_id=program,
        teacher_flag=False
    ).order_by('-student_code')
    class_instance = Class.objects.get(class_id=class_id)
    rolecalls_qs = RoleCall.objects.filter(class_field_id=class_id)
    rolecalls = {rc.user_id: rc for rc in rolecalls_qs}
    
    context = {
        "program": program,
        "user": user,
        "rolecalls": rolecalls,
        "class_instance": class_instance,
        "students": students,
    }
    return render(request, "teacher/program/rolecalls.html", context)

def program_activities(request, program_id):
    teacher_id = request.session.get('t_id')
    if not teacher_id:
        messages.error(request, 'You do not have permission to access the user profile.')
        return redirect('sum_teacher:show_teacher_login')

    user = User.objects.get(user_id=teacher_id)
    program = Program.objects.get(program_id=program_id)

    # Get all activities in this program
    activities = Activity.objects.filter(module__program=program).select_related('module').order_by('-created_at')

    context = {
        "program": program,
        "user": user,
        "activities": activities,
    }
    return render(request, "teacher/program/activities.html", context)

def show_create_activity(request, program_id):
    teacher_id = request.session.get('t_id')
    if not teacher_id:
        messages.error(request, 'You do not have permission to access the user profile.')
        return redirect('sum_teacher:show_teacher_login')

    user = User.objects.get(user_id=teacher_id)
    program = Program.objects.get(program_id=program_id)

    # Get all teachers in this program
    modules = Module.objects.filter(
        program_id=program,
        deleted_at__isnull=True
    ).order_by('-created_at')

    context = {
        "program": program,
        "user": user,
        "modules": modules,
    }
    return render(request, "teacher/program/_activity_create.html", context)


def create_activity(request, program_id):
    teacher_id = request.session.get('t_id')
    if not teacher_id:
        messages.error(request, 'You do not have permission to access the user profile.')
        return redirect('sum_teacher:show_teacher_login')

    user = User.objects.get(user_id=teacher_id)
    program = Program.objects.get(program_id=program_id)
    modules = Module.objects.filter(
        program_id=program,
        deleted_at__isnull=True
    ).order_by('-created_at')
    
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        type_raw = request.POST.get("type", "").strip()
        schedule_raw = request.POST.get("schedule", "").strip()
        module_id = request.POST.get("module_id", "").strip()

        errors = {}
        form_data = {
            "title": title,
            "description": description,
            "type": type_raw,
            "schedule": schedule_raw,
            "module_id": module_id,
        }
        
        # Validate title
        if not title:
            errors["title"] = "Title is required."
        elif len(title) > 100:
            errors["title"] = "Title must be less than 100 characters."

        # Validate description
        if not description:
            errors["description"] = "Description is required."
        elif len(description) > 500:
            errors["description"] = "Description must be less than 500 characters."

        # Validate type
        if not type_raw or type_raw not in ["1", "2"]:
            errors["type"] = "Invalid type selected."

        # Validate schedule
        try:
            schedule = parse_date(schedule_raw)
            if not schedule:
                raise ValueError()
        except Exception:
            schedule = None
            errors["schedule"] = "Invalid date format."

        # Validate module
        try:
            module = Module.objects.get(module_id=module_id, program_id=program, deleted_at__isnull=True)
        except Module.DoesNotExist:
            errors["module_id"] = "Selected module does not exist."

        # If errors, re-render form with errors and old data
        if errors:
            return render(request, "teacher/program/_activity_create.html", {
                "errors": errors,
                "form_data": form_data,
                "program": program,
                "user": user,
                "modules": modules,
            })

        # Create activity
        Activity.objects.create(
            title=title,
            description=description,
            module=module,
            type=int(type_raw),
            schedule=schedule,
            created_by=teacher_id,
        )
        messages.success(request, "Activity created successfully.")
        return redirect("sum_teacher:program_activities", program_id=program.program_id)

    # If GET request
    return render(request, "teacher/program/_activity_create.html", {
        "program": program,
        "user": user,
        "modules": modules,
    })


def program_users(request, program_id):
    teacher_id = request.session.get('t_id')
    if not teacher_id:
        messages.error(request, 'You do not have permission to access the user profile.')
        return redirect('sum_teacher:show_teacher_login')

    user = User.objects.get(user_id=teacher_id)
    program = Program.objects.get(program_id=program_id)

    # Get all teachers in this program
    teachers = Registration.objects.filter(
        program_id=program,
        teacher_flag=True,
        deleted_at__isnull=True
    ).select_related('user').order_by('-created_at')

    
    students = Registration.objects.filter(
        program_id=program,
        teacher_flag=False,
        deleted_at__isnull=True
    ).select_related('user').order_by('-created_at')

    context = {
        "program": program,
        "user": user,
        "teachers": teachers,
        "students": students,
    }
    return render(request, "teacher/program/users.html", context)

# show assignments
def show_assignments(request, program_id):
    teacher_id = request.session.get('t_id')
    if not teacher_id:
        messages.error(request, 'You do not have permission to access the user profile.')
        return redirect('sum_teacher:show_teacher_login')

    user = User.objects.get(user_id=teacher_id)
    program = Program.objects.get(program_id=program_id)

    # Get all assignments in this program
    assignments = Task.objects.filter(
        module__program=program,
        module__teacher__user_id=teacher_id,
        deleted_at__isnull=True
        ).select_related('module', 'file').order_by('-created_at')

    context = {
        "program": program,
        "user": user,
        "assignments": assignments,
    }
    return render(request, "teacher/program/assignments.html", context)

# show create assignment form
def show_create_assignment(request, program_id):
    teacher_id = request.session.get('t_id')
    if not teacher_id:
        messages.error(request, 'You do not have permission to access the user profile.')
        return redirect('sum_teacher:show_teacher_login')

    user = User.objects.get(user_id=teacher_id)
    program = Program.objects.get(program_id=program_id)

    # Get all modules in this program
    modules = Module.objects.filter(
        program=program,
        teacher_id=teacher_id,
        deleted_at__isnull=True
    ).order_by('-created_at')

    context = {
        "program": program,
        "user": user,
        "modules": modules,
    }
    return render(request, "teacher/program/assignment_create.html", context)


def handle_uploaded_file(uploaded_file):
    ext = uploaded_file.name.split('.')[-1].lower()
    file_name = secrets.token_hex(8)
    full_name = f"{file_name}.{ext}"
    save_path = os.path.join('tasks', full_name)
    full_path = os.path.join(settings.MEDIA_ROOT, save_path)

    # ✅ Ensure the directory exists
    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    # Save the file
    with open(full_path, 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)

    return save_path  # This is a relative path like 'uploads/myfile.pdf

def create_assignment(request, program_id):
    teacher_id = request.session.get('t_id')
    if not teacher_id:
        messages.error(request, 'You do not have permission to access the user profile.')
        return redirect('sum_teacher:show_teacher_login')

    user = User.objects.get(user_id=teacher_id)
    program = Program.objects.get(program_id=program_id)

    # Get all modules in this program
    modules = Module.objects.filter(
        program=program,
        teacher_id=teacher_id,
        deleted_at__isnull=True
    ).order_by('-created_at')

    if request.method == "POST":
        errors = {}
        form_data = request.POST.dict()
        file_obj = request.FILES.get('file')

        # Extract fields
        title = form_data.get('title', '').strip()
        end_date = form_data.get('end_date')
        type_val = form_data.get('type')
        module_id = form_data.get('module_id')
        max_score = form_data.get('max_score')

        # ======== VALIDATIONS ========
        if not title or len(title) > 100 or not title.replace(" ", "").isalnum():
            errors['title'] = "Title is required, max 100 characters, and should not contain special characters."

        if type_val not in ['1', '2']:
            errors['type'] = "Invalid task type."

        if not module_id or not Module.objects.filter(module_id=module_id).exists():
            errors['module_id'] = "Invalid module."

        if not max_score or not max_score.isdigit() or not (1 <= int(max_score) <= 100):
            errors['max_score'] = "Max score must be a number between 1 and 100."

        if file_obj:
            allowed_exts = ['jpg', 'jpeg', 'png', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'txt',
                            'html', 'css', 'js', 'ts', 'json', 'xml', 'py', 'php', 'java', 'cpp', 'c', 'cs', 'rb',
                            'go', 'sh', 'sql', 'swift']
            ext = file_obj.name.split('.')[-1].lower()
            if ext not in allowed_exts:
                errors['file'] = "Invalid file type."
            elif file_obj.size > 10 * 1024 * 1024:
                errors['file'] = "File must be less than 10MB."

        if errors:
            # Prepare modules for re-rendering the form
            return render(request, 'teacher/program/assignment_create.html', {
                'errors': errors,
                'form_data': form_data,
                'modules': modules,
                'program': program,
                'user': user,
            })

        if file_obj:
            # ======== SAVE FILE ========
            file_path = handle_uploaded_file(file_obj)
            new_file = File.objects.create(
                original_name=file_obj.name,
                type=1,
                size=file_obj.size,
                url=os.path.join(settings.MEDIA_URL, file_path)
            )
        else:
            new_file = None

        # ======== SAVE TASK ========
        Task.objects.create(
            module_id=module_id,
            title=title,
            type=type_val,
            max_score=max_score,
            end_date=end_date,
            file=new_file,
            created_by=teacher_id,
        )

        messages.success(request, "Assignment created successfully.")
        return redirect('sum_teacher:show_assignments', program_id=program_id)

    return redirect('sum_teacher:show_create_assignment', program_id=program_id)

# show assignment details
def show_assignment_details(request, program_id, task_id):
    teacher_id = request.session.get('t_id')
    if not teacher_id:
        messages.error(request, 'You do not have permission to access the user profile.')
        return redirect('sum_teacher:show_teacher_login')

    user = User.objects.get(user_id=teacher_id)
    program = Program.objects.get(program_id=program_id)
    assignment = Task.objects.filter(
        task_id=task_id,
        module__program=program,
        module__teacher__user_id=teacher_id,
        deleted_at__isnull=True
    ).select_related('module', 'file').first()
    submitted_user_ids = SubmittedTask.objects.filter(task_id=task_id).values('student_id').distinct()
    not_sub_students = Registration.objects.filter(
        user__is_teacher=False,
        program_id=program,
        teacher_flag=False,
        deleted_at__isnull=True
    ).exclude(
        user_id__in=Subquery(submitted_user_ids)
    ).select_related('user')

    if not assignment:
        messages.error(request, 'Assignment not found.')
        return redirect('sum_teacher:show_assignments', program_id=program.program_id)

    context = {
        "program": program,
        "user": user,
        "assignment": assignment,
        "not_sub_students": not_sub_students,
    }
    return render(request, "teacher/program/assignment_details.html", context)

# show program profile
def program_profile(request, program_id):
    teacher_id = request.session.get('t_id')
    if not teacher_id:
        messages.error(request, 'You do not have permission to access the user profile.')
        return redirect('sum_teacher:show_teacher_login')

    user = User.objects.get(user_id=teacher_id)
    registration = Registration.objects.filter(
        program_id=program_id,
        user_id=teacher_id,
        teacher_flag=True,
        deleted_at__isnull=True
    ).first()
    program = Program.objects.get(program_id=program_id)

    context = {
        "program": program,
        "user": user,
        "registration": registration,
    }
    return render(request, "teacher/program/profile.html", context)

# show edit nickname
def show_edit_nickname(request, program_id):
    teacher_id = request.session.get('t_id')
    if not teacher_id:
        messages.error(request, 'You do not have permission to access the user profile.')
        return redirect('sum_teacher:show_teacher_login')

    user = User.objects.get(user_id=teacher_id)
    registration = Registration.objects.filter(
        program_id=program_id,
        user_id=teacher_id,
        teacher_flag=True,
        deleted_at__isnull=True
    ).first()
    program = Program.objects.get(program_id=program_id)

    context = {
        "program": program,
        "user": user,
        "registration": registration,
    }
    return render(request, "teacher/program/edit_nickname.html", context)

# update nickname
def update_nickname(request, program_id):
    teacher_id = request.session.get('t_id')
    if not teacher_id:
        messages.error(request, 'You do not have permission to access the user profile.')
        return redirect('sum_teacher:show_teacher_login')

    user = User.objects.get(user_id=teacher_id)
    registration = Registration.objects.filter(
        program_id=program_id,
        user_id=teacher_id,
        teacher_flag=True,
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
                "teacher/program/edit_nickname.html",
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
        return redirect("sum_teacher:program_profile", program_id=program.program_id)

    return redirect("sum_teacher:show_edit_nickname")