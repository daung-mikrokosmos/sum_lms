from django.shortcuts import render

def welcome(request):
    """Welcome view for the LMS homepage"""
    return render(request, 'welcome.html', {
        'title': 'SUM',
        'page_title': 'WARMLY WELCOME TO SUM',
        'welcome_message': 'Welcome to Spring University Myanmar'
    })

def login(request):
    return render(request, 'auth/user_login.html')


def register(request):
    return render(request, 'auth/user_register.html')

def admin_login(request):
    return render(request, 'auth/admin_login.html')