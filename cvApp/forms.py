from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class ResumeUploadForm(forms.Form):
    resume = forms.FileField(
        label="Upload Your Resume",
        widget=forms.ClearableFileInput(attrs={
            'accept': '.pdf,.docx',
            'class': 'form-control'
        }),
        help_text="Accepted formats: PDF, DOCX"
    )
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        pwd = cleaned_data.get("password")
        confirm_pwd = cleaned_data.get("confirm_password")
        if pwd != confirm_pwd:
            self.add_error("confirm_password", "Passwords do not match.")

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))