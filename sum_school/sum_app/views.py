from django.shortcuts import render

def welcome(request):
    """Welcome view for the LMS homepage"""
    return render(request, 'welcome.html', {
        'title': 'SUM',
        'page_title': 'WARMLY WELCOME TO SUM',
        'welcome_message': 'Welcome to Spring University Myanmar'
    })
