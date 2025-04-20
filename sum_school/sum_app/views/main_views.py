from django.shortcuts import render, redirect
from django.urls import reverse

# welcoming page
def welcome(request):
    # Redirect authenticated staff users to admin dashboard
    if request.user.is_authenticated and request.user.is_staff:
        return redirect(reverse('sum_admin:admin_dashboard'))

    return render(request, 'welcome.html')
