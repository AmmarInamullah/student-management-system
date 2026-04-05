from django.db import models
from django.contrib.auth import get_user_model
from apps.teachers.models import TeacherProfile

User = get_user_model()

class StaffRecord(models.Model):
    STAFF_TYPES = (
        ('admin', 'Administrative'),
        ('support', 'Support Staff'),
        ('technical', 'Technical Staff'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_record')
    staff_id = models.CharField(max_length=20, unique=True)
    staff_type = models.CharField(max_length=20, choices=STAFF_TYPES)
    position = models.CharField(max_length=100)
    joining_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    emergency_contact = models.CharField(max_length=15)
    emergency_contact_name = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.staff_id} - {self.user.get_full_name()}"

class PaymentRecord(models.Model):
    PAYMENT_TYPES = (
        ('salary', 'Salary'),
        ('bonus', 'Bonus'),
        ('reimbursement', 'Reimbursement'),
    )
    
    recipient_type = models.CharField(max_length=20)
    recipient_id = models.IntegerField()
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100, blank=True)
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='processed_payments')
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.get_payment_type_display()} - {self.amount}"