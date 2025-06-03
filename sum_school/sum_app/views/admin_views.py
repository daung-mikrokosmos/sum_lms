from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from ..models.admin import Admin
from ..models.program import Program
from ..models.module import Module
from ..models.registration import Registration
from ..models.activity import Activity
from ..models.rolecall import RoleCall
from ..models.task import Task
from ..models.module_class import Class
from ..models.leave import Leave
from ..models.user import User
from django.db.models import Q, Count
from django.contrib.auth.hashers import check_password, make_password
from django.utils import timezone
from django.utils.timezone import now
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware, is_naive
from datetime import datetime, time
from django.db.models import Prefetch
import datetime
import re

# admin login view
def show_admin_login(request):
    if request.session.get("admin_id"):
        return redirect(reverse("sum_admin:admin_dashboard"))
    return render(request, "auth/admin_login.html")


# admin login
def admin_login(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()

        # Store the entered email in session
        request.session["login_old_email"] = email

        if not email or not password:
            messages.error(request, "Please enter both email and password.")
            return redirect(reverse("sum_admin:show_admin_login"))

        try:
            admin = Admin.objects.get(email=email)
            if check_password(password, admin.password):
                request.session["admin_id"] = admin.admin_id
                messages.success(request, f"Welcome back, {admin.name}!")
                request.session.pop("login_old_email", None)
                return redirect(reverse("sum_admin:admin_dashboard"))
            else:
                messages.error(request, "Invalid credentials.")
        except Admin.DoesNotExist:
            messages.error(request, "Invalid credentials.")

    return redirect(reverse("sum_admin:show_admin_login"))


# admin dashboard
def admin_dashboard(request):
    admin_id = request.session.get("admin_id")
    if not admin_id:
        messages.error(
            request, "You do not have permission to access the admin dashboard."
        )
        return redirect("sum_admin:show_admin_login")

    admin = Admin.objects.get(admin_id=admin_id)
    programs = Program.objects.all()
    context = {
        "programs": programs,
        "admin": admin,
    }
    return render(request, "admin/dashboard.html", context)


# admin logout
def admin_logout(request):
    request.session.flush()
    messages.success(request, "You have been logged out successfully.")
    return redirect("sum_admin:show_admin_login")


# show admin profile
def show_admin_profile(request):
    admin_id = request.session.get("admin_id")
    if not admin_id:
        messages.error(
            request, "You do not have permission to access the admin profile."
        )
        return redirect("sum_admin:show_admin_login")

    admin = Admin.objects.get(admin_id=admin_id)
    context = {
        "admin": admin,
    }
    return render(request, "admin/profile/profile.html", context)


# Edit admin profile
def show_edit_admin_profile(request):
    admin_id = request.session.get("admin_id")
    if not admin_id:
        messages.error(request, "You do not have permission to access.")
        return redirect("sum_admin:show_admin_login")

    admin = Admin.objects.get(admin_id=admin_id)
    return render(request, "admin/profile/edit_profile.html", {"admin": admin})


# Update admin profile
def update_admin_profile(request):
    admin_id = request.session.get("admin_id")
    if not admin_id:
        messages.error(
            request, "You do not have permission to access the admin profile."
        )
        return redirect("sum_admin:show_admin_login")

    admin = Admin.objects.get(admin_id=admin_id)

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        phone = request.POST.get("phone_no", "").strip()
        errors = {}

        # Validation
        if not name:
            errors["name"] = "Name is required."
        elif len(name) > 50:
            errors["name"] = "Name must not exceed 50 characters."

        if phone:
            if not phone.isdigit():
                errors["phone_no"] = "Phone number must contain only digits."
            elif len(phone) > 12 or len(phone) < 7:
                errors["phone_no"] = "Phone number must not exceed 12 digits."

        if errors:
            return render(
                request,
                "admin/profile/edit_profile.html",
                {
                    "admin": admin,
                    "form_data": {"name": name, "phone_no": phone},
                    "errors": errors,
                },
            )

        # Save if no errors
        admin.name = name
        admin.phone_no = phone
        admin.save()
        messages.success(request, "Profile updated successfully.")
        return redirect("sum_admin:show_admin_profile")

    return redirect("sum_admin:show_edit_admin_profile")


# edit admin email
def show_edit_admin_email(request):
    admin_id = request.session.get("admin_id")
    if not admin_id:
        messages.error(request, "You do not have permission to access.")
        return redirect("sum_admin:show_admin_login")

    admin = Admin.objects.get(admin_id=admin_id)
    return render(request, "admin/profile/edit_email.html", {"admin": admin})


# Update admin email
def update_admin_email(request):
    admin_id = request.session.get("admin_id")
    if not admin_id:
        messages.error(
            request, "You do not have permission to access the admin profile."
        )
        return redirect("sum_admin:show_admin_login")

    admin = Admin.objects.get(admin_id=admin_id)

    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        errors = {}

        # Email Validation
        if not email:
            errors["email"] = "Email is required."
        elif len(email) > 255:
            errors["email"] = "Email must not exceed 255 characters."
        elif not re.match(r"^[\w\.-]+@[\w\.-]+\.\w{2,4}$", email):
            errors["email"] = "Enter a valid email address."
        elif email == admin.email:
            errors["email"] = "This is the old email."
        else:
            # Password Validation
            if not password:
                errors["password"] = "Password is required."
            elif not check_password(password, admin.password):
                errors["password"] = "Incorrect password."

        if errors:
            return render(
                request,
                "admin/profile/edit_email.html",
                {
                    "admin": admin,
                    "form_data": {"email": email},
                    "errors": errors,
                },
            )

        # Save if no errors
        admin.email = email
        admin.save()
        messages.success(request, "Email updated successfully.")
        return redirect("sum_admin:show_admin_profile")

    return redirect("sum_admin:show_edit_admin_email")


# edit admin password
def show_edit_admin_password(request):
    admin_id = request.session.get("admin_id")
    if not admin_id:
        messages.error(request, "You do not have permission to access.")
        return redirect("sum_admin:show_admin_login")

    return render(request, "admin/profile/edit_password.html")


# update admin password
def update_admin_password(request):
    admin_id = request.session.get("admin_id")
    if not admin_id:
        messages.error(request, "You do not have permission to access.")
        return redirect("sum_admin:show_admin_login")

    admin = Admin.objects.get(admin_id=admin_id)

    if request.method == "POST":
        old_password = request.POST.get("old_password", "")
        new_password = request.POST.get("new_password", "")
        confirm_password = request.POST.get("cf_password", "")
        errors = {}

        # Password validation
        if not old_password:
            errors["old_password"] = "Old password is required."

        if not new_password:
            errors["new_password"] = "New password is required."

        if not confirm_password:
            errors["cf_password"] = "Confirm password is required."

        if old_password and not check_password(old_password, admin.password):
            errors["old_password"] = "Incorrect old password."

        if new_password:
            if len(new_password) < 8 or len(new_password) > 24:
                errors["new_password"] = "Password must be between 8 and 24 characters."
            elif not re.search(r"[A-Z]", new_password):
                errors["new_password"] = (
                    "Password must contain at least 1 uppercase letter."
                )
            elif not re.search(r"\d", new_password):
                errors["new_password"] = "Password must contain at least 1 number."

        if new_password and confirm_password and new_password != confirm_password:
            errors["cf_password"] = "Passwords do not match."

        if errors:
            return render(
                request,
                "admin/profile/edit_password.html",
                {
                    "admin": admin,
                    "errors": errors,
                },
            )

        # Save new password securely
        admin.password = make_password(new_password)
        admin.save()
        messages.success(request, "Password updated successfully.")
        return redirect("sum_admin:show_admin_profile")

    return redirect("sum_admin:show_edit_admin_password")


# program dashboard
def program_dashboard(request, program_id):
    admin_id = request.session.get("admin_id")
    if not admin_id:
        messages.error(
            request, "You do not have permission to access the admin dashboard."
        )
        return redirect("sum_admin:show_admin_login")

    admin = Admin.objects.get(admin_id=admin_id)
    program = Program.objects.get(program_id=program_id)

    # Total modules
    total_modules = Module.objects.filter(program=program).count()

    # Total teachers
    total_teachers = Registration.objects.filter(
        program_id=program, teacher_flag=True
    ).count()

    # Total students
    total_students = (
        Registration.objects.filter(program=program)
        .filter(Q(teacher_flag=False) | Q(teacher_flag__isnull=True))
        .count()
    )

    # Get all module IDs in this program
    module_ids = Module.objects.filter(program=program).values_list(
        "module_id", flat=True
    )

    # Total activities across all modules
    total_activities = Activity.objects.filter(module_id__in=module_ids).count()

    # Total tasks across all modules
    total_tasks = Task.objects.filter(module_id__in=module_ids).count()
    
    # Total classes
    total_tasks = Class.objects.filter(module_id__in=module_ids).count()
    
    # total leaves
    total_leaves = Leave.objects.filter(program=program).count()

    context = {
        "program": program,
        "admin": admin,
        "total_modules": total_modules,
        "total_teachers": total_teachers,
        "total_students": total_students,
        "total_activities": total_activities,
        "total_tasks": total_tasks,
        "total_classes": total_tasks,
        "total_leaves": total_leaves,
    }
    return render(request, "admin/program/dashboard.html", context)

# show programs students
def program_students(request, program_id):
    admin_id = request.session.get("admin_id")
    if not admin_id:
        messages.error(
            request, "You do not have permission to access the admin dashboard."
        )
        return redirect("sum_admin:show_admin_login")

    admin = Admin.objects.get(admin_id=admin_id)
    program = Program.objects.get(program_id=program_id)

    # Get all students in this program
    users = Registration.objects.filter(
        program_id=program,
        teacher_flag=False,
        deleted_at__isnull=True
    ).select_related('user').order_by('-created_at')

    context = {
        "program": program,
        "admin": admin,
        "users": users,
        "is_student": True,
    }
    return render(request, "admin/user/users.html", context)

# show programs teachers
def program_teachers(request, program_id):
    admin_id = request.session.get("admin_id")
    if not admin_id:
        messages.error(
            request, "You do not have permission to access the admin dashboard."
        )
        return redirect("sum_admin:show_admin_login")

    admin = Admin.objects.get(admin_id=admin_id)
    program = Program.objects.get(program_id=program_id)

    # Get all teachers in this program
    users = Registration.objects.filter(
        program_id=program,
        teacher_flag=True,
        deleted_at__isnull=True
    ).select_related('user').order_by('-created_at')

    context = {
        "program": program,
        "admin": admin,
        "users": users,
        "is_student": False,
    }
    return render(request, "admin/user/users.html", context)


# show programs users
def program_users(request, program_id):
    admin_id = request.session.get("admin_id")
    if not admin_id:
        messages.error(
            request, "You do not have permission to access the admin dashboard."
        )
        return redirect("sum_admin:show_admin_login")

    admin = Admin.objects.get(admin_id=admin_id)
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
        "admin": admin,
        "teachers": teachers,
        "students": students,
    }
    return render(request, "admin/user/all_users.html", context)

# program activities
def program_activities(request, program_id):
    admin_id = request.session.get("admin_id")
    if not admin_id:
        messages.error(
            request, "You do not have permission to access the admin dashboard."
        )
        return redirect("sum_admin:show_admin_login")

    admin = Admin.objects.get(admin_id=admin_id)
    program = Program.objects.get(program_id=program_id)

    # Get all activities in this program
    activities = Activity.objects.filter(module__program=program).select_related('module').order_by('-created_at')

    context = {
        "program": program,
        "admin": admin,
        "activities": activities,
    }
    return render(request, "admin/activity/activities.html", context)

# program classes
def program_classes(request, program_id):
    admin_id = request.session.get("admin_id")
    if not admin_id:
        messages.error(
            request, "You do not have permission to access the admin dashboard."
        )
        return redirect("sum_admin:show_admin_login")

    admin = Admin.objects.get(admin_id=admin_id)
    program = Program.objects.get(program_id=program_id)

    # Get all classes in this program
    classes = Class.objects.filter(module__program=program).select_related('module').order_by('-created_at')

    context = {
        "program": program,
        "admin": admin,
        "classes": classes,
    }
    return render(request, "admin/class/classes.html", context)

# program leaves
def program_leaves(request, program_id):
    admin_id = request.session.get("admin_id")
    if not admin_id:
        messages.error(
            request, "You do not have permission to access the admin dashboard."
        )
        return redirect("sum_admin:show_admin_login")

    admin = Admin.objects.get(admin_id=admin_id)
    program = Program.objects.get(program_id=program_id)

    # Get all leaves in this program
    # leaves = Leave.objects.filter(program=program).select_related('user').order_by('-created_at')

    from django.db.models import Prefetch

    # Prefetch registration for the same program
    registration_qs = Registration.objects.filter(program=program)

    leaves = Leave.objects.filter(program=program) \
        .select_related('user') \
        .prefetch_related(Prefetch('user__registration_set', queryset=registration_qs, to_attr='reg')) \
        .order_by('-created_at')

    context = {
        "program": program,
        "admin": admin,
        "leaves": leaves,
    }
    return render(request, "admin/leave/leaves.html", context)


# program leave details
def leave_details(request, program_id, leave_id):
    admin_id = request.session.get("admin_id")
    if not admin_id:
        messages.error(
            request, "You do not have permission to access the admin dashboard."
        )
        return redirect("sum_admin:show_admin_login")

    admin = Admin.objects.get(admin_id=admin_id)
    leave = Leave.objects.select_related('program', 'user').get(leave_id=leave_id)
    program = Program.objects.get(program_id=program_id)

    context = {
        "admin": admin,
        "leave": leave,
        "program": program,
    }
    return render(request, "admin/leave/leave_details.html", context)

# approve leave
def approve_leave(request, program_id, leave_id):

    admin_id = request.session.get("admin_id")
    if not admin_id:
        messages.error(
            request, "You do not have permission to access the admin dashboard."
        )
        return redirect("sum_admin:show_admin_login")

    leave = Leave.objects.get(leave_id=leave_id)

    # Update approval status
    leave.approve_status = True
    leave.save()
    
    return redirect('sum_admin:leave_details', program_id, leave_id)

# cancel class
def cancel_class(request, program_id, class_id):
    admin_id = request.session.get("admin_id")
    if not admin_id:
        messages.error(
            request, "You do not have permission to access the admin dashboard."
        )
        return redirect("sum_admin:show_admin_login")

    class_instance = Class.objects.get(class_id=class_id)
    class_instance.canceled = True
    class_instance.save()
    messages.success(request, "Class cancelled successfully.")
    return redirect("sum_admin:program_classes", program_id=program_id)

# show create program
def show_create_program(request):
    admin_id = request.session.get("admin_id")
    if not admin_id:
        messages.error(
            request, "You do not have permission to access the admin dashboard."
        )
        return redirect("sum_admin:show_admin_login")

    return render(request, "admin/program/create.html")

# create program
def create_program(request):
    admin_id = request.session.get("admin_id")
    if not admin_id:
        messages.error(request, "You do not have permission to access the admin dashboard.")
        return redirect("sum_admin:show_admin_login")

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        program_code = request.POST.get("program_code", "").strip()
        fees = request.POST.get("fees", "").strip()
        start_date = request.POST.get("start_date", "").strip()
        end_date = request.POST.get("end_date", "").strip()

        # Convert fees
        try:
            fees = int(fees) if fees else None
        except ValueError:
            fees = None

        errors = {}
        today = timezone.localdate()

        # Validate fields
        if not name:
            errors["name"] = "Program name is required."
        elif len(name) > 100:
            errors["name"] = "Program name must not exceed 100 characters."

        if not program_code:
            errors["program_code"] = "Program code is required."
        elif len(program_code) > 5:
            errors["program_code"] = "Program code must not exceed 5 characters."
        elif len(program_code) < 2:
            errors["program_code"] = "Program code must be at least 2 characters."
        elif Program.objects.filter(program_code=program_code).exists():
            errors["program_code"] = "Program code already exists."

        if fees is not None:
            if fees < 0:
                errors["fees"] = "Fees must be a non-negative number."
            elif fees > 100000000:
                errors["fees"] = "Fees must not exceed 100,000,000."

        try:
            parsed_start = datetime.date.fromisoformat(start_date)
            if parsed_start < today:
                errors["start_date"] = "Start date cannot be in the past."
        except Exception:
            errors["start_date"] = "Invalid start date format."

        try:
            parsed_end = datetime.date.fromisoformat(end_date)
            if start_date and parsed_start >= parsed_end:
                errors["end_date"] = "End date must be after start date."
        except Exception:
            errors["end_date"] = "Invalid end date format."

        if errors:
            return render(request, "admin/program/create.html", {
                "form_data": {
                    "name": name,
                    "program_code": program_code,
                    "fees": fees,
                    "start_date": start_date,
                    "end_date": end_date,
                },
                "errors": errors
            })

        program = Program.objects.create(
            name=name,
            program_code=program_code,
            fees=fees or 0,
            start_date=parsed_start,
            end_date=parsed_end,
            created_by=admin_id,
        )

        messages.success(request, "Program created successfully.")
        return redirect("sum_admin:program_dashboard", program_id=program.program_id)

    return render(request, "admin/program/create.html")


# show rolecalls
def show_rolecalls(request, program_id, class_id):
    admin_id = request.session.get("admin_id")
    if not admin_id:
        messages.error(
            request, "You do not have permission to access the admin dashboard."
        )
        return redirect("sum_admin:show_admin_login")

    admin = Admin.objects.get(admin_id=admin_id)
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
        "admin": admin,
        "rolecalls": rolecalls,
        "class_instance": class_instance,
        "students": students,
    }
    return render(request, "admin/class/rolecalls.html", context)

# mark rolecall
def mark_rolecall(request, program_id, class_id, user_id, status):
    admin_id = request.session.get("admin_id")
    if not admin_id:
        messages.error(
            request, "You do not have permission to access the admin dashboard."
        )
        return redirect("sum_admin:show_admin_login")
    
    already_marked = RoleCall.objects.filter(user_id=user_id, class_field_id=class_id).exists()
    if already_marked:
        rolecall = RoleCall.objects.get(user_id=user_id, class_field_id=class_id)
        rolecall.status = status
        rolecall.save()
    else:
        rolecall = RoleCall(
            user_id=user_id,
            class_field_id=class_id,
            status=status
        )
        rolecall.save()
    messages.success(request, "Rolecall marked successfully.")
    return redirect("sum_admin:show_rolecalls", program_id=program_id, class_id=class_id)

# show all people
def show_all_people(request):
    admin_id = request.session.get("admin_id")
    if not admin_id:
        messages.error(
            request, "You do not have permission to access the admin dashboard."
        )
        return redirect("sum_admin:show_admin_login")

    admin = Admin.objects.get(admin_id=admin_id)
    users = User.objects.all().order_by('-created_at')

    context = {
        "admin": admin,
        "users": users,
    }
    return render(request, "admin/user/all_people.html", context)

# show create user
def show_create_user(request):
    admin_id = request.session.get("admin_id")
    if not admin_id:
        messages.error(request, "You do not have permission to access.")
        return redirect("sum_admin:show_admin_login")

    admin = Admin.objects.get(admin_id=admin_id)
    return render(request, "admin/user/create.html", {"admin": admin})

# create user
def create_user(request):
    admin_id = request.session.get("admin_id")
    if not admin_id:
        messages.error(request, "You do not have permission to access.")
        return redirect("sum_admin:show_admin_login")

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        phone_no = request.POST.get("phone_no", "").strip()
        is_teacher_raw = request.POST.get("is_teacher", "False")
        is_teacher = is_teacher_raw == "True"
        password = request.POST.get("password", "").strip()
        errors = {}
        
        # Validation
        if not name:
            errors["name"] = "Name is required."
        elif len(name) > 50:
            errors["name"] = "Name must not exceed 50 characters."

        if not email:
            errors["email"] = "Email is required."
        elif len(email) > 255:
            errors["email"] = "Email must not exceed 255 characters."
        elif not re.match(r"^[\w\.-]+@[\w\.-]+\.\w{2,4}$", email):
            errors["email"] = "Enter a valid email address."
        elif User.objects.filter(email=email).exists():
            errors["email"] = "Email already exists."
        
        if phone_no and (not phone_no.isdigit() or len(phone_no) < 7 or len(phone_no) > 12):
            errors["phone_no"] = "Phone number must be between 7 and 12 digits."

        if not password:
            errors["password"] = "Password is required."
        elif len(password) < 8 or len(password) > 24:
            errors["password"] = "Password must be between 8 and 24 characters."
        
        if errors:
            return render(
                request,
                "admin/user/create.html",
                {
                    "form_data": {
                        "name": name,
                        "email": email,
                        "phone_no": phone_no,
                        "is_teacher": is_teacher,
                    },
                    "errors": errors,
                    "admin": Admin.objects.get(admin_id=admin_id),
                },
            )

        # Save if no errors
        user = User(
            name=name,
            email=email,
            phone_no=phone_no,
            is_teacher=is_teacher,
            is_approved=True,
            password=make_password(password),
        )
        user.save()
        messages.success(request, "User created successfully.")
        return redirect("sum_admin:show_all_people")
    
    return redirect("sum_admin:show_create_user")

# show user register
def show_user_register(request, program_id):
    admin_id = request.session.get("admin_id")
    if not admin_id:
        messages.error(request, "You do not have permission to access.")
        return redirect("sum_admin:show_admin_login")
    
    admin = Admin.objects.get(admin_id=admin_id)
    program = Program.objects.get(program_id=program_id)
    not_registered_users = User.objects.exclude(
        registration__program_id=program
    ).order_by('-created_at')

    context = {
        "admin": admin,
        "program": program,
        "users": not_registered_users,
    }

    return render(request, "admin/program/register.html", context)

# register user
def register_user(request, program_id, user_id, teacher_flag, scholared):
    teacher_flag = teacher_flag.lower() == "true"
    scholared = scholared.lower() == "true"
    admin_id = request.session.get("admin_id")
    if not admin_id:
        messages.error(request, "You do not have permission to access.")
        return redirect("sum_admin:show_admin_login")

    program = Program.objects.get(program_id=program_id)
    user = User.objects.get(user_id=user_id)

    # Check if already registered
    if Registration.objects.filter(program_id=program, user_id=user).exists():
        messages.error(request, "User is already registered in this program.")
        return redirect("sum_admin:show_user_register", program_id=program_id)
    
    if scholared:
        payment_status=3
    else:
        payment_status=0

    registration = Registration(
        program_id=program_id,
        user_id=user_id,
        teacher_flag=teacher_flag,
        scholared=scholared,
        payment_status=payment_status,
    )
    registration.save()
    messages.success(request, f"{user.name} has been registered successfully.")
    return redirect("sum_admin:show_user_register", program_id=program_id)

# remove user from program
def remove_user(request, program_id, user_id):
    admin_id = request.session.get("admin_id")
    if not admin_id:
        messages.error(request, "You do not have permission to access.")
        return redirect("sum_admin:show_admin_login")

    program = get_object_or_404(Program, program_id=program_id)
    try:
        registration = Registration.objects.get(program_id=program_id, user_id=user_id)
    except Registration.DoesNotExist:
        return redirect("sum:show_user_register", program_id=program_id)

    registration.updated_by = admin_id
    registration.deleted_at = now()
    registration.save()

    return redirect("sum_admin:program_users", program_id=program_id)

# show modules
def program_modules(request, program_id):
    admin_id = request.session.get("admin_id")
    if not admin_id:
        messages.error(request, "You do not have permission to access.")
        return redirect("sum_admin:show_admin_login")

    program = Program.objects.get(program_id=program_id)
    admin = Admin.objects.get(admin_id=admin_id)
    
    modules = Module.objects.filter(program=program).select_related('teacher').prefetch_related(
        Prefetch(
            'teacher__registration_set',
            queryset=Registration.objects.filter(program=program),
            to_attr='filtered_registrations'
        )
    ).order_by('-module_code')
    
    context = {
        "admin": admin,
        "program": program,
        "modules": modules,
    }
    return render(request, "admin/module/modules.html", context)

# create module view
def show_create_module(request, program_id):
    admin_id = request.session.get("admin_id")
    if not admin_id:
        messages.error(request, "You do not have permission to access.")
        return redirect("sum_admin:show_admin_login")

    program = Program.objects.get(program_id=program_id)
    admin = Admin.objects.get(admin_id=admin_id)

    # Get all teachers in this program
    teachers = Registration.objects.filter(
        program_id=program,
        teacher_flag=True,
        deleted_at__isnull=True
    ).select_related('user').order_by('-created_at')
    
    context = {
        "admin": admin,
        "program": program,
        "teachers": teachers,
    }

    return render(request, "admin/module/create.html", context)

# create module
def create_module(request, program_id):
    admin_id = request.session.get("admin_id")
    if not admin_id:
        messages.error(request, "You do not have permission to access.")
        return redirect("sum_admin:show_admin_login")

    program = Program.objects.get(program_id=program_id)
    admin = Admin.objects.get(admin_id=admin_id)

    # Get all teachers in this program
    teachers = Registration.objects.filter(
        program_id=program,
        teacher_flag=True,
        deleted_at__isnull=True
    ).select_related('user').order_by('-created_at')
    
    context = {
        "admin": admin,
        "program": program,
        "teachers": teachers,
    }
    
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        module_code = request.POST.get("module_code", "").strip()
        credit = request.POST.get("credit", "").strip()
        teacher_id = request.POST.get("teacher_id", "").strip()
        errors = {}
    
        # Validation
        if not name:
            errors["name"] = "Name is required."
        elif len(name) > 50:
            errors["name"] = "Name must not exceed 50 characters."
        
        if not module_code:
            errors["module_code"] = "Code is required."
        elif len(module_code) > 8 or len(module_code) < 3:
            errors["module_code"] = "Code must be 3 to 8 characters."
        elif Module.objects.filter(program_id=program_id, module_code=module_code).exists():
            errors['module_code'] = "Code already used."
        
        if credit:
            if credit and (len(credit) > 3 or len(credit) < 1):
                errors["credit"] = "Credit must be 1 to 3 digit."
            else:
                try:
                    credit = int(credit)
                except ValueError:
                    errors["credit"] = "Credit must be a number."

        if not teacher_id:
            errors["teacher_id"] = "Teacher is required."
        elif not Registration.objects.filter(program_id=program, user_id=teacher_id).exists():
            errors["credit"] = "Teacher does not exitst."
        
        if errors:
            return render(
                request,
                "admin/module/create.html",
                {
                    "form_data": {
                        "name": name,
                        "module_code": module_code,
                        "credit": credit,
                        "teacher_id": teacher_id,
                    },
                    "errors": errors,
                    "admin": admin,
                    "program": program,
                    "teachers": teachers,
                },
            )

        # Save if no errors
        module = Module(
            name=name,
            module_code=module_code,
            credit=credit,
            teacher_id=teacher_id,
            program_id=program_id,
            created_by=admin_id,
        )
        module.save()
        messages.success(request, "Module created successfully.")
        return redirect("sum_admin:program_modules", program_id=program_id)
    
    return redirect("sum_admin:show_create_module", context)

# create module view
def show_create_class(request, program_id):
    admin_id = request.session.get("admin_id")
    if not admin_id:
        messages.error(request, "You do not have permission to access.")
        return redirect("sum_admin:show_admin_login")

    program = Program.objects.get(program_id=program_id)
    admin = Admin.objects.get(admin_id=admin_id)

    # Get all teachers in this program
    modules = Module.objects.filter(
        program_id=program,
        deleted_at__isnull=True
    ).order_by('-created_at')
    
    context = {
        "admin": admin,
        "program": program,
        "modules": modules,
    }

    return render(request, "admin/class/create.html", context)
    
def create_class(request, program_id):
    admin_id = request.session.get("admin_id")
    if not admin_id:
        messages.error(request, "You do not have permission to access.")
        return redirect("sum_admin:show_admin_login")

    program = Program.objects.get(program_id=program_id)
    admin = Admin.objects.get(admin_id=admin_id)

    # Get all teachers in this program
    modules = Module.objects.filter(
        program_id=program,
        deleted_at__isnull=True
    ).order_by('-created_at')
    
    context = {
        "admin": admin,
        "program": program,
        "modules": modules,
    }

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        start_time_raw = request.POST.get("start_time", "").strip()
        end_time_raw = request.POST.get("end_time", "").strip()
        module_id = request.POST.get("module_id", "").strip()

        errors = {}
        form_data = {
            "title": title,
            "start_time": start_time_raw,
            "end_time": end_time_raw,
            "module_id": module_id,
        }

        # Validation: Title
        if not title:
            errors["title"] = "Title is required."
        elif len(title) > 100:
            errors["title"] = "Title must be less than 100 characters."

        # Parse and validate start_time
        try:
            start_time = parse_datetime(start_time_raw)
            if start_time and is_naive(start_time):
                start_time = make_aware(start_time)
        except Exception:
            start_time = None
            errors["start_time"] = "Invalid start time format."

        if not start_time:
            errors["start_time"] = "Start time is required or invalid."

        # Parse and validate end_time
        try:
            end_time = parse_datetime(end_time_raw)
            if end_time and is_naive(end_time):
                end_time = make_aware(end_time)
        except Exception:
            end_time = None
            errors["end_time"] = "Invalid end time format."

        if not end_time:
            errors["end_time"] = "End time is required or invalid."

        # Logical validation
        if start_time and end_time and start_time >= end_time:
            errors["end_time"] = "End time must be after start time."
        
        if not module_id:
            errors["module_id"]= "Module is required."
        elif not Module.objects.filter(program_id=program).exists():
            errors["module_id"]= "Module not exists."

        # Return with errors if any
        if errors:
            return render(request, "admin/class/create.html", {
                "errors": errors,
                "form_data": form_data,
                "admin": admin,
                "program": program,
                "modules": modules,
            })

        # Create the module
        Class.objects.create(
            title=title,
            start_time=start_time,
            end_time=end_time,
            canceled=False,
            module_id=module_id,
            created_by=admin_id,
        )

        messages.success(request, "Module created successfully.")
        return redirect("sum_admin:program_classes", program_id=program_id)

    return redirect("sum_admin:show_create_class", program_id=program_id)