# Generated by Django 5.1.5 on 2025-03-08 06:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('skills_required', models.TextField()),
                ('vacancies', models.IntegerField()),
                ('salary', models.IntegerField()),
                ('office_time', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=100)),
                ('job_type', models.CharField(max_length=50)),
                ('deadline', models.DateField()),
                ('employer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.employer')),
            ],
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('resume', models.FileField(upload_to='resumes/')),
                ('cover_letter', models.TextField()),
                ('status', models.CharField(choices=[('Under Review', 'Under Review'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], default='Under Review', max_length=20)),
                ('job_seeker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.jobseeker')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.job')),
            ],
        ),
    ]
