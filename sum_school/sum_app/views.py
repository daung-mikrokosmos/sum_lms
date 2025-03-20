from django.shortcuts import render

def welcome(request):
    """Welcome view for the LMS homepage"""
    return render(request, 'welcome.html', {
        'title': 'WARMLY WELCOME',
        'welcome_message': 'Welcome to Spring University Myanmar'
    })
