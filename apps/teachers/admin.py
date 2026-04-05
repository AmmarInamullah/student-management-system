from django.contrib import admin
from .models import TeacherProfile, Salary, Assignment, Grade, Attendance

class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('teacher_id', 'user', 'department', 'employment_type')
    search_fields = ('teacher_id', 'user__username', 'user__first_name', 'user__last_name')
    list_filter = ('department', 'employment_type')

class SalaryAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'month', 'amount', 'net_amount', 'payment_status')
    list_filter = ('payment_status', 'month')

class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'teacher', 'due_date', 'status')
    list_filter = ('status', 'subject__department')

class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'grade_letter', 'percentage', 'uploaded_at')
    list_filter = ('subject', 'grade_letter')

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'date', 'is_present')
    list_filter = ('is_present', 'date', 'subject')

admin.site.register(TeacherProfile, TeacherProfileAdmin)
admin.site.register(Salary, SalaryAdmin)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(Grade, GradeAdmin)
admin.site.register(Attendance, AttendanceAdmin)