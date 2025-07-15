
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import ResumeUploadForm, RegisterForm, LoginForm
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')


def landing_view(request):
    return render(request, 'home.html')

def analyze_view(request):
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            resume_file = form.cleaned_data['resume']
            # 🧠 TODO: Analysis logic goes here
            return render(request, 'results.html', {'filename': resume_file.name})
    else:
        form = ResumeUploadForm()
    return render(request, 'analyze.html', {'form': form})

from users.models import UserProfile

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            # Create a UserProfile as well
            UserProfile.objects.create(
                username=user.username,
                email=user.email,
                password=user.password,  # hashed password
                first_name=user.first_name,
                last_name=user.last_name
            )
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def features_view(request):
    return render(request, 'features.html')