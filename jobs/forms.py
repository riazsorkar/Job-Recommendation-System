from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class JobSeekerSignUpForm(UserCreationForm):
    skills = forms.CharField(max_length=255)
    experience = forms.IntegerField()
    expected_salary = forms.IntegerField()
    address = forms.CharField(widget=forms.Textarea)
    education = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'skills', 'experience', 'expected_salary', 'address', 'education')

class EmployerSignUpForm(UserCreationForm):
    company_name = forms.CharField(max_length=100)
    company_address = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'company_name', 'company_address')


from django import forms
from .models import Job

class JobPostForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'skills_required', 'vacancies', 'salary', 'office_time', 'location', 'job_type', 'deadline']


from django import forms
from .models import Application

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['name', 'phone', 'email', 'resume', 'cover_letter']



from django import forms
from .models import JobSeeker

class JobSeekerProfileForm(forms.ModelForm):
    class Meta:
        model = JobSeeker
        fields = ['skills', 'experience', 'expected_salary', 'address', 'education']


from django import forms
from .models import Employer, Job

class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = ['company_name', 'company_address']

class JobEditForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'skills_required', 'vacancies', 'salary', 'office_time', 'location', 'job_type', 'deadline']

from django import forms
from .models import Application

class ApplicationStatusForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['status']