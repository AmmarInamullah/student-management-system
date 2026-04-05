from django.db import models
from django.contrib.auth import get_user_model
from apps.accounts.models import Department

User = get_user_model()

class TeacherProfile(models.Model):
    EMPLOYMENT_TYPES = (
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    teacher_id = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPES)
    qualification = models.CharField(max_length=200)
    specialization = models.CharField(max_length=200)
    joining_date = models.DateField()
    subjects_taught = models.ManyToManyField('students.Subject', related_name='teachers', blank=True)
    
    def __str__(self):
        return f"{self.teacher_id} - {self.user.get_full_name()}"

class Salary(models.Model):
    PAYMENT_STATUS = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('late', 'Late'),
    )
    
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name='salaries')
    month = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(null=True, blank=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    payment_method = models.CharField(max_length=50, blank=True)
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        self.net_amount = self.amount + self.bonus - self.deduction
        super().save(*args, **kwargs)
    
    class Meta:
        unique_together = ['teacher', 'month']
        ordering = ['-month']
    
    def __str__(self):
        return f"{self.teacher} - {self.month.strftime('%B %Y')}"

class Assignment(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('closed', 'Closed'),
    )
    
    subject = models.ForeignKey('students.Subject', on_delete=models.CASCADE, related_name='assignments')
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='assignments/', null=True, blank=True)
    due_date = models.DateTimeField()
    total_marks = models.IntegerField(default=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.subject.code} - {self.title}"

class Grade(models.Model):
    student = models.ForeignKey('students.StudentProfile', on_delete=models.CASCADE, related_name='grades')
    subject = models.ForeignKey('students.Subject', on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, null=True, blank=True)
    exam_type = models.CharField(max_length=50)
    marks_obtained = models.FloatField()
    total_marks = models.IntegerField()
    percentage = models.FloatField()
    grade_letter = models.CharField(max_length=2)
    remarks = models.TextField(blank=True)
    uploaded_by = models.ForeignKey(TeacherProfile, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        self.percentage = (self.marks_obtained / self.total_marks) * 100
        if self.percentage >= 90:
            self.grade_letter = 'A'
        elif self.percentage >= 80:
            self.grade_letter = 'B+'
        elif self.percentage >= 70:
            self.grade_letter = 'B'
        elif self.percentage >= 60:
            self.grade_letter = 'C+'
        elif self.percentage >= 50:
            self.grade_letter = 'C'
        elif self.percentage >= 40:
            self.grade_letter = 'D'
        else:
            self.grade_letter = 'F'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.student} - {self.subject} - {self.grade_letter}"

class Attendance(models.Model):
    student = models.ForeignKey('students.StudentProfile', on_delete=models.CASCADE, related_name='attendance')
    subject = models.ForeignKey('students.Subject', on_delete=models.CASCADE)
    date = models.DateField()
    is_present = models.BooleanField(default=False)
    marked_by = models.ForeignKey(TeacherProfile, on_delete=models.SET_NULL, null=True)
    remarks = models.TextField(blank=True)
    marked_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['student', 'subject', 'date']
    
    def __str__(self):
        return f"{self.student} - {self.subject} - {self.date}"