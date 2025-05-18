from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from ..models.admin import Admin
from ..models.program import Program
from ..models.module import Module
from ..models.registration import Registration
from ..models.activity import Activity
from ..models.task import Task
from django.db.models import Q, Count
from django.contrib.auth.hashers import check_password
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
import re
from django.contrib.auth.hashers import check_password, make_password


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

    context = {
        "program": program,
        "admin": admin,
        "total_modules": total_modules,
        "total_teachers": total_teachers,
        "total_students": total_students,
        "total_activities": total_activities,
        "total_tasks": total_tasks,
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
        teacher_flag=False
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
        teacher_flag=True
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
        teacher_flag=True
    ).select_related('user').order_by('-created_at')
    
    students = Registration.objects.filter(
        program_id=program,
        teacher_flag=False
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