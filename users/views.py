from django.shortcuts import render
from .models import UserProfile


def UserProfile(request):
    """
    Render the user profile page.
    """
    # Here you would typically fetch user data from the database
    # For now, we will just render a simple template
    return render(request, 'profile.html')
