from django.contrib import admin

from django.urls import path
from .views import UserProfile
from .models import UserProfile

admin.site.register(UserProfile)
list_display = ('username', 'email', 'first_name', 'last_name')



 