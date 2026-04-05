from django.contrib import admin
from .models import StudentProfile, Subject, Enrollment

class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'user', 'department', 'year_level')
    search_fields = ('student_id', 'user__username', 'user__first_name', 'user__last_name')
    list_filter = ('department', 'year_level')

class SubjectAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'department', 'credits', 'semester')
    search_fields = ('code', 'name')
    list_filter = ('department', 'semester')

class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'enrollment_date', 'is_active')
    list_filter = ('is_active', 'subject__department')

admin.site.register(StudentProfile, StudentProfileAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)