from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    USER_TYPES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('management', 'Management'),
    )
    
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='student')
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} - {self.get_user_type_display()}"

class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    head_of_department = models.ForeignKey(
        'teachers.TeacherProfile', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='headed_departments'  # ADD THIS LINE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class AcademicYear(models.Model):
    year = models.CharField(max_length=20)
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)
    
    def __str__(self):
        return self.year

class Semester(models.Model):
    SEMESTER_TYPES = (
        ('fall', 'Fall'),
        ('spring', 'Spring'),
        ('summer', 'Summer'),
    )
    
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    semester_type = models.CharField(max_length=20, choices=SEMESTER_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.academic_year} - {self.get_semester_type_display()}"