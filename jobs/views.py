from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import JobSeekerSignUpForm, EmployerSignUpForm
from django.contrib.auth.decorators import login_required
from .models import Employer, JobSeeker, Job, Application

from django.core.paginator import Paginator
from .forms import JobSearchForm

def home(request):
    # Get all jobs
    jobs = Job.objects.all()

    # Handle search query and filters
    form = JobSearchForm(request.GET or None)
    if form.is_valid():
        query = form.cleaned_data['query']
        location = form.cleaned_data['location']
        min_salary = form.cleaned_data['min_salary']
        max_salary = form.cleaned_data['max_salary']
        job_type = form.cleaned_data['job_type']

        # Apply filters
        if query:
            jobs = jobs.filter(
                title__icontains=query
            ) | jobs.filter(
                skills_required__icontains=query
            )
        if location:
            jobs = jobs.filter(location__icontains=location)
        if min_salary:
            jobs = jobs.filter(salary__gte=min_salary)
        if max_salary:
            jobs = jobs.filter(salary__lte=max_salary)
        if job_type:
            jobs = jobs.filter(job_type=job_type)

    # Paginate the jobs
    paginator = Paginator(jobs, 10)  # Show 10 jobs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'jobs/home.html', {
        'form': form,
        'page_obj': page_obj,
    })

def job_seeker_signup(request):
    if request.method == 'POST':
        form = JobSeekerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            JobSeeker.objects.create(
                user=user,
                skills=form.cleaned_data['skills'],
                experience=form.cleaned_data['experience'],
                expected_salary=form.cleaned_data['expected_salary'],
                address=form.cleaned_data['address'],
                education=form.cleaned_data['education']
            )
            login(request, user)
            return redirect('job_seeker_dashboard')
    else:
        form = JobSeekerSignUpForm()
    return render(request, 'jobs/job_seeker_signup.html', {'form': form})

def employer_signup(request):
    if request.method == 'POST':
        form = EmployerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            Employer.objects.create(
                user=user,
                company_name=form.cleaned_data['company_name'],
                company_address=form.cleaned_data['company_address']
            )
            login(request, user)
            return redirect('employer_dashboard')
    else:
        form = EmployerSignUpForm()
    return render(request, 'jobs/employer_signup.html', {'form': form})












@login_required
def job_seeker_dashboard(request):
    try:
        job_seeker = JobSeeker.objects.get(user=request.user)
        applications = job_seeker.application_set.all()  # Get all applications by this job seeker
        return render(request, 'jobs/job_seeker_dashboard.html', {'job_seeker': job_seeker, 'applications': applications})
    except JobSeeker.DoesNotExist:
        # If the user is not a Job Seeker, redirect to the home page or show an error
        return redirect('home')

    















    
@login_required
def employer_dashboard(request):
    try:
        employer = Employer.objects.get(user=request.user)
        # jobs = employer.job_set.all()  # Get all jobs posted by this employer
        jobs = Job.objects.filter(employer=employer)
        return render(request, 'jobs/employer_dashboard.html', {'employer': employer, 'jobs': jobs})
    except Employer.DoesNotExist:
        # If the user is not an Employer, redirect to the home page or show an error
        return redirect('home')
 


from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)  # Log the user in

            # Redirect based on user role
            if hasattr(user, 'jobseeker'):
                return redirect('job_seeker_dashboard')
            elif hasattr(user, 'employer'):
                return redirect('employer_dashboard')
            else:
                return redirect('home')  # Default redirect
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})




from django.shortcuts import render, redirect
from .forms import JobPostForm
from .models import Job, Employer

@login_required
def post_job(request):
    employer = Employer.objects.get(user=request.user)
    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = employer
            job.save()
            return redirect('employer_dashboard')
    else:
        form = JobPostForm()
    return render(request, 'jobs/post_job.html', {'form': form})


from django.shortcuts import render, redirect, get_object_or_404
from .forms import JobApplicationForm
from .models import Job, Application, JobSeeker

@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    job_seeker = JobSeeker.objects.get(user=request.user)
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.job_seeker = job_seeker
            application.save()
            return redirect('job_seeker_dashboard')
    else:
        form = JobApplicationForm()
    return render(request, 'jobs/apply_job.html', {'form': form, 'job': job})


from django.shortcuts import render, get_object_or_404
from .models import Job

def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'jobs/job_detail.html', {'job': job})


from django.shortcuts import render, redirect
from .forms import JobSeekerProfileForm
from .models import JobSeeker

@login_required
def edit_profile(request):
    job_seeker = JobSeeker.objects.get(user=request.user)
    if request.method == 'POST':
        form = JobSeekerProfileForm(request.POST, instance=job_seeker)
        if form.is_valid():
            form.save()
            return redirect('job_seeker_dashboard')
    else:
        form = JobSeekerProfileForm(instance=job_seeker)
    return render(request, 'jobs/edit_profile.html', {'form': form})


from django.shortcuts import render, redirect, get_object_or_404
from .forms import EmployerProfileForm, JobEditForm
from .models import Employer, Job

@login_required
def edit_employer_profile(request):
    employer = Employer.objects.get(user=request.user)
    if request.method == 'POST':
        form = EmployerProfileForm(request.POST, instance=employer)
        if form.is_valid():
            form.save()
            return redirect('employer_dashboard')
    else:
        form = EmployerProfileForm(instance=employer)
    return render(request, 'jobs/edit_employer_profile.html', {'form': form})


@login_required
def edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.method == 'POST':
        form = JobEditForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('employer_dashboard')
    else:
        form = JobEditForm(instance=job)
    return render(request, 'jobs/edit_job.html', {'form': form, 'job': job})


from django.shortcuts import render, get_object_or_404
from .models import Job, Application

@login_required
def manage_applications(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    applications = Application.objects.filter(job=job).order_by('-status')  # Sort by status (e.g., Accepted first)
    return render(request, 'jobs/manage_applications.html', {'job': job, 'applications': applications})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Application
from .forms import ApplicationStatusForm

@login_required
def update_application_status(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    if request.method == 'POST':
        form = ApplicationStatusForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            return redirect('manage_applications', job_id=application.job.id)
    else:
        form = ApplicationStatusForm(instance=application)
    return render(request, 'jobs/update_application_status.html', {'form': form, 'application': application})


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Job

@login_required
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    # Ensure only the job's employer can delete the job
    if job.employer.user != request.user:
        messages.error(request, "You do not have permission to delete this job.")
        return redirect('employer_dashboard')

    # Delete the job
    job.delete()
    messages.success(request, "Job deleted successfully.")
    return redirect('employer_dashboard')


from django.shortcuts import render, redirect
from .models import JobSeeker, Job
from .utils import recommend_jobs

@login_required
def recommended_jobs(request):
    try:
        job_seeker = JobSeeker.objects.get(user=request.user)
        jobs = Job.objects.all()  # Get all jobs
        recommended_jobs = recommend_jobs(job_seeker, jobs)  # Get recommended jobs
        # paginator = Paginator(jobs, 2)  # Show 10 jobs per page
        # page_number = request.GET.get('page')
        # page_obj = paginator.get_page(page_number)
        return render(request, 'jobs/recommended_jobs.html', {'recommended_jobs': recommended_jobs})
    except JobSeeker.DoesNotExist:
        # If the user is not a Job Seeker, redirect to the home page or show an error
        return redirect('home')
    


