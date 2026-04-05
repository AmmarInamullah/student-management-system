from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum, Avg, Count
from django.utils import timezone
from apps.accounts.models import User, Department
from apps.students.models import StudentProfile, Subject, Enrollment
from apps.teachers.models import TeacherProfile, Salary, Grade
@login_required
def management_dashboard(request):
    if request.user.user_type != 'management':
        messages.error(request, 'Access denied.')
        return redirect('dashboard_redirect')
    
    # Statistics
    total_students = StudentProfile.objects.count()
    total_teachers = TeacherProfile.objects.count()
    total_subjects = Subject.objects.count()
    total_departments = Department.objects.count()
    
    # Recent students
    recent_students = StudentProfile.objects.select_related('user', 'department').order_by('-enrollment_date')[:5]
    
    # Grade statistics
    grade_stats = Grade.objects.aggregate(
        avg_grade=Avg('percentage'),
        total_grades=Count('id')
    )
    
    # Pending salaries
    pending_salaries = Salary.objects.filter(payment_status='pending').count()
    pending_amount = Salary.objects.filter(payment_status='pending').aggregate(total=Sum('net_amount'))['total'] or 0
    
    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_subjects': total_subjects,
        'total_departments': total_departments,
        'recent_students': recent_students,
        'pending_salaries': pending_salaries,
        'pending_amount': pending_amount,
        'avg_grade': round(grade_stats['avg_grade'], 2) if grade_stats['avg_grade'] else 0,
    }
    
    return render(request, 'management/dashboard.html', context)

@login_required
def manage_students(request):
    if request.user.user_type != 'management':
        messages.error(request, 'Access denied.')
        return redirect('dashboard_redirect')
    
    students = StudentProfile.objects.select_related('user', 'department').all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        students = students.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(student_id__icontains=search_query)
        )
    
    context = {
        'students': students,
        'search_query': search_query,
    }
    return render(request, 'management/students.html', context)

@login_required
def manage_teachers(request):
    if request.user.user_type != 'management':
        messages.error(request, 'Access denied.')
        return redirect('dashboard_redirect')
    
    teachers = TeacherProfile.objects.select_related('user', 'department').all()
    
    context = {
        'teachers': teachers,
    }
    return render(request, 'management/teachers.html', context)