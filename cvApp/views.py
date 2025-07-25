import io
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import ResumeUploadForm, RegisterForm, LoginForm
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
import json
import ollama
from docx import Document
from django.http import FileResponse

@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')


def landing_view(request):
    return render(request, 'home.html')

def analyze_view(request):
    analysis_result = None
    job_description = None
    match_percentage = None
    strengths = None
    weaknesses = None
    suggestions = None
    edit_suggestions = None
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        job_description = request.POST.get('job_description', '').strip()
        action = request.POST.get('action', 'analyze')
        if form.is_valid():
            resume_file = form.cleaned_data['resume']
            resume_text = ""
            if hasattr(resume_file, 'read'):
                try:
                    content = resume_file.read()
                    try:
                        resume_text = content.decode('utf-8')
                    except Exception:
                        resume_text = "[Resume file uploaded, but could not decode as text.]"
                except Exception:
                    resume_text = "[Error reading resume file.]"
            else:
                resume_text = str(resume_file)
                
           
                try:
                    prompt = (
                        "You are a strict resume screening assistant. "
                        "Compare the resume to the job description and provide a JSON response with these keys: "
                        "percentage (number, 0-100), qualified (yes/no), strengths (list), weaknesses (list), missing (list of missing skills/requirements), suggestions (list). "
                        "Be evidence-based: justify the percentage and qualification with specific examples from the resume. "
                        "If a skill or requirement is missing, list it in 'missing'. "
                        "Example: {\"percentage\": 70, \"qualified\": \"no\", \"strengths\": [..], \"weaknesses\": [..], \"missing\": [..], \"suggestions\": [..]}\n"
                        f"Resume: {resume_text}\nJob Description: {job_description}"
                    )
                    response = ollama.generate(
                        model="llama3.2:1b",
                        prompt=prompt
                    )
                   
                    raw = response['response'] if 'response' in response else response
                    try:
                        # Try to extract JSON from the response
                        start = raw.find('{')
                        end = raw.rfind('}') + 1
                        json_str = raw[start:end]
                        data = json.loads(json_str)
                        match_percentage = data.get('percentage')
                        strengths = data.get('strengths')
                        weaknesses = data.get('weaknesses')
                        suggestions = data.get('suggestions')
                        missing = data.get('missing')
                        qualified = data.get('qualified')
                        analysis_result = None
                    except Exception:
                        analysis_result = raw
                except Exception as e:
                    analysis_result = f"Ollama error: {e}"
    else:
        form = ResumeUploadForm()
    return render(request, 'analyze.html', {
        'form': form,
        'analysis_result': analysis_result,
        'job_description': job_description,
        'match_percentage': match_percentage,
        'strengths': strengths,
        'weaknesses': weaknesses,
        'suggestions': suggestions,
        'missing': missing if 'missing' in locals() else None,
        'qualified': qualified if 'qualified' in locals() else None,
        'edit_suggestions': edit_suggestions,
    })

def edit_resume_view(request):
    form = ResumeUploadForm()
    resume_text = ""
    edit_suggestions = None

    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            resume_file = form.cleaned_data['resume']

            # Read resume content
            try:
                content = resume_file.read()
                resume_text = content.decode('utf-8', errors='ignore')
            except:
                resume_text = "[Error reading resume]"

            # Call Ollama for edit suggestions
            try:
                prompt = (
                    "You are a professional resume editor. "
                    "Review the following resume for grammar mistakes, formatting issues, and suggest corrections or improvements. "
                    "Do NOT return the resume itself or any personal data. Do NOT return the resume in JSON format. "
                    "Return your response as JSON with keys: grammar (list), formatting (list), corrections (list). "
                    "Example: {\"grammar\": [..], \"formatting\": [..], \"corrections\": [..]}\n"
                    f"Resume: {resume_text}"
                )
                response = ollama.generate(model="llama3.2:1b", prompt=prompt)
                raw = response['response'] if 'response' in response else response
                start = raw.find('{')
                end = raw.rfind('}') + 1
                json_str = raw[start:end]
                edit_suggestions = json.loads(json_str)

            except Exception as e:
                edit_suggestions = {"error": str(e)}
    return render(request, 'edit.html', {
        'form': form,
        'edit_suggestions': edit_suggestions
    })

def suggestion_view(request):
    return render(request, 'suggestion.html')

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            if password:
                user.set_password(password)
            user.save()
            print(f"User {user.username} saved to database.")
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