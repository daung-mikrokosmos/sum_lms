from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

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

user = {
    "name" : 'Maung Maung',
    "role" : 'user',
}


def dashboard(request):
    
    return render(request, 'users/dashboard.html' , {
        'title' : 'SUM | dashboard',
        'user' : user
    })
    
def programDetails(request,course_id):
    print(request.path)
    return redirect(f"{request.path}activity")


def activity(request,course_id) :
   
    return render(request,'users/program_details_layout.html' ,{
        "user" : user,
        "course_id" : course_id
    })
    
def activityCreate(request,course_id):
    
    if (user['role'] != 'teacher'):
        url = reverse('activity' , kwargs={'course_id' : course_id})
        messages.error(request,'You have no permission to access create new activity route!')
        return redirect(url)
    else :
        return render(request,'users/program_details_layout.html' ,{
            "user" : user,
            "course_id" : course_id
        })
        
    
def moduleRedirect(request,course_id):
    print(request.path)
    return redirect(f"{request.path}1")

def module(request,course_id,m):
    
    return render(request,'users/program_details_layout.html' ,{
        "user" : user,
        "course_id" : course_id,
        'module' : m
    })
    
def moduleUploadLesson(request,course_id):
    if (user['role'] != 'teacher'):
        url = reverse('moduleRedirect' , kwargs={"course_id" : course_id})
        messages.error(request,'You have no permission to access upload lesson route!')
        return redirect(url)
    else :
        return render(request,'users/program_details_layout.html' ,{
            "user" : user,
            "course_id" : course_id
        })
    
def assignmentRedirect(request,course_id):
    return redirect(f"{request.path}1?status=all")

def assignment(request,course_id,m):
    
    statusFilter = request.GET.get('status');
    
    return render(request,'users/program_details_layout.html',{
        "user" : user,
        "course_id" : course_id,
        "module" : m,
        "status" : statusFilter
    })
    
def assignmentDetails(request,course_id,m,assignment_id):
    
    return render(request, 'users/program_details_layout.html' , {
        "user" : user,
        "course_id" : course_id,
        "module" : m,
        "assignment_id" : assignment_id
    })
    
    
def people(request , course_id):

    return render(request, 'users/program_details_layout.html' , {
        "user" : user,
        "course_id" : course_id
    })
    
def classes(request,course_id):
    
    return render(request, 'users/program_details_layout.html' , {
        "user" : user,
        "course_id" : course_id
    })