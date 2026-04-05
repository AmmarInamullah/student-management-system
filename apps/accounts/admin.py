from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import User, Department, AcademicYear, Semester

# Unregister the default Group admin if you want to customize it
# admin.site.unregister(Group)

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_staff', 'is_active')
    list_filter = ('user_type', 'is_staff', 'is_active', 'groups')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'address', 'date_of_birth', 'profile_picture')}),
        ('Permissions', {'fields': ('user_type', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'user_type'),
        }),
    )

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'head_of_department', 'created_at')
    search_fields = ('name', 'code')

class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('year', 'start_date', 'end_date', 'is_current')
    list_filter = ('is_current',)

class SemesterAdmin(admin.ModelAdmin):
    list_display = ('academic_year', 'semester_type', 'start_date', 'end_date', 'is_current')
    list_filter = ('is_current', 'semester_type', 'academic_year')

# Register your models
admin.site.register(User, CustomUserAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(AcademicYear, AcademicYearAdmin)
admin.site.register(Semester, SemesterAdmin)

# Optional: Customize the admin site header
admin.site.site_header = "Student Management System Administration"
admin.site.site_title = "Student Management Admin"
admin.site.index_title = "Welcome to Student Management System"