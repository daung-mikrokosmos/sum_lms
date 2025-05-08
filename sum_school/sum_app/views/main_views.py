from django.shortcuts import render, redirect
from django.urls import reverse

def custom_404(request, exception):
    return render(request, 'errors/404.html', status=404)


# welcoming page
def welcome(request):
    if request.session.get('admin_id'):
        return redirect('sum_admin:admin_dashboard')
    elif request.session.get('s_id'):
        return redirect('sum_student:student_dashboard')
    elif request.session.get('t_id'):
        return redirect('sum_teacher:teacher_dashboard')

    return render(request, 'welcome.html')

def show_register(request):
    return render(request, 'auth/user_register.html')

# UI
def dashboard(request):
    user = {
            "name" : 'Maung Maung',
            "role" : 'student',
            "user_image" : 'image'
        }
    
    return render(request, 'users/dashboard.html' , {
        'title' : 'SUM | dashboard',
        'user' : user
    })
    
def programDetails(request,course_id):
    print(request.path)
    return redirect(f"{request.path}activity")


def activity(request,course_id) :
    user = {
            "name" : 'Maung Maung',
            "role" : 'student',
            "user_image" : 'image'
        }
    
    return render(request,'users/program_details_layout.html' ,{
        "user" : user
    })