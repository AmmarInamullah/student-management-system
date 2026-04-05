from django.db import models
from django.contrib.auth import get_user_model
from apps.accounts.models import Department, Semester

User = get_user_model()

class StudentProfile(models.Model):
    YEAR_LEVELS = [(i, f"Year {i}") for i in range(1, 5)]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    student_id = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    year_level = models.IntegerField(choices=YEAR_LEVELS, default=1)
    current_semester = models.ForeignKey(Semester, on_delete=models.SET_NULL, null=True)
    enrollment_date = models.DateField(auto_now_add=True)
    guardian_name = models.CharField(max_length=100, blank=True)
    guardian_phone = models.CharField(max_length=15, blank=True)
    guardian_email = models.EmailField(blank=True)
    
    def __str__(self):
        return f"{self.student_id} - {self.user.get_full_name()}"

class Subject(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    credits = models.IntegerField(default=3)
    description = models.TextField(blank=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.code} - {self.name}"

class Enrollment(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='enrollments')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['student', 'subject']
    
    def __str__(self):
        return f"{self.student} enrolled in {self.subject}"