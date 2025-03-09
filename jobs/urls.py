from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('job-seeker-signup/', views.job_seeker_signup, name='job_seeker_signup'),
    path('employer-signup/', views.employer_signup, name='employer_signup'),
    # path('login/', auth_views.LoginView.as_view(template_name='jobs/login.html'), name='login'),
    path('login/', views.custom_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('job-seeker-dashboard/', views.job_seeker_dashboard, name='job_seeker_dashboard'),
    path('employer-dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('post-job/', views.post_job, name='post_job'),
    path('apply-job/<int:job_id>/', views.apply_job, name='apply_job'),
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),
    path('apply-job/<int:job_id>/', views.apply_job, name='apply_job'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('edit-employer-profile/', views.edit_employer_profile, name='edit_employer_profile'),
    path('edit-job/<int:job_id>/', views.edit_job, name='edit_job'),
    path('manage-applications/<int:job_id>/', views.manage_applications, name='manage_applications'),
    path('update-application-status/<int:application_id>/', views.update_application_status, name='update_application_status'),
    path('recommended-jobs/', views.recommended_jobs, name='recommended_jobs'),
    path('delete-job/<int:job_id>/', views.delete_job, name='delete_job'),
]