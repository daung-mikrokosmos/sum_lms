from django.shortcuts import render, redirect
from django.urls import reverse

# welcoming page
def welcome(request):
    if request.session.get('admin_id'):
        return redirect('sum_admin:admin_dashboard')
    elif request.session.get('user_id'):
        return redirect('sum_student:student_dashboard')

    return render(request, 'welcome.html')
