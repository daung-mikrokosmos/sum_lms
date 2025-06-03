from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

def error_404(request, exception=None):
    return render(request, '404.html')

def custom_404(request):
    if request.session.get('admin_id'):
        return render(request, '404.html')
    elif request.session.get('s_id'):
        return render(request, '404.html')
    elif request.session.get('t_id'):
        return render(request, '404.html')

    return redirect('welcome')


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
    "role" : 'teacher',
}


# Dashboard
def dashboard(request):
    
    return render(request, 'users/dashboard.html' , {
        'title' : 'SUM | dashboard',
        'user' : user
    })

# programDetails
def programDetails(request,course_id):
    print(request.path)
    return redirect(f"{request.path}activity")


# Activity Page
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
        
#Module Page
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


#Assignment Page
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
    
def assignmentCreate(request,course_id):
    if (user['role'] != 'teacher'):
        url = reverse('assignmentRedirect' , kwargs={"course_id" : course_id })
        messages.error(request,'You have no permission to access upload assignment route!')
        return redirect(url)
    else :
        return render(request,'users/program_details_layout.html' ,{
            "user" : user,
            "course_id" : course_id
        })
    
def assignmentDetails(request,course_id,m,assignment_id):
    
    return render(request, 'users/program_details_layout.html' , {
        "user" : user,
        "course_id" : course_id,
        "module" : m,
        "assignment_id" : assignment_id
    })
    
   
#People Page 
def people(request , course_id):

    return render(request, 'users/program_details_layout.html' , {
        "user" : user,
        "course_id" : course_id
    })
    
#Classes Page
def classes(request,course_id):
    
    return render(request, 'users/program_details_layout.html' , {
        "user" : user,
        "course_id" : course_id
    })