from django.db import models
from django.contrib.auth.models import User

class JobSeeker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    skills = models.TextField()
    experience = models.IntegerField()
    expected_salary = models.IntegerField()
    address = models.TextField()
    education = models.TextField()

    def __str__(self):
        return self.user.username

class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    company_address = models.TextField()

    def __str__(self):
        return self.company_name
    

class Job(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    skills_required = models.TextField()
    vacancies = models.IntegerField()
    salary = models.IntegerField()
    office_time = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    job_type = models.CharField(max_length=50)
    deadline = models.DateField()

    def __str__(self):
        return self.title
    

class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    job_seeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField()
    status = models.CharField(max_length=20, choices=[('Under Review', 'Under Review'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], default='Under Review')

    def __str__(self):
        return f"{self.job_seeker.user.username} - {self.job.title}"
