from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count, Sum
from django.utils import timezone
from .models import StudentProfile, Enrollment, Subject
from apps.teachers.models import Grade, Assignment, Attendance

@login_required
def student_dashboard(request):
    # Check if user is a student
    if request.user.user_type != 'student':
        messages.error(request, 'Access denied. Student only area.')
        return redirect('dashboard_redirect')
    
    # Get student profile
    try:
        student_profile = request.user.student_profile
    except:
        messages.error(request, 'Student profile not found. Please contact admin.')
        return redirect('dashboard_redirect')
    
    # Get current enrollments
    enrollments = Enrollment.objects.filter(
        student=student_profile, 
        is_active=True
    ).select_related('subject', 'subject__department')
    
    # Get grades for all enrolled subjects
    grades = Grade.objects.filter(
        student=student_profile
    ).select_related('subject', 'assignment')
    
    # Calculate GPA (average of all grades)
    gpa = grades.aggregate(avg=Avg('percentage'))['avg']
    
    # Get attendance summary
    attendance_total = Attendance.objects.filter(student=student_profile).count()
    attendance_present = Attendance.objects.filter(student=student_profile, is_present=True).count()
    attendance_rate = (attendance_present / attendance_total * 100) if attendance_total > 0 else 0
    
    # Get pending assignments (not yet graded)
    pending_assignments = Assignment.objects.filter(
        subject__in=[e.subject for e in enrollments],
        status='published',
        due_date__gte=timezone.now()
    ).exclude(
        grade__student=student_profile
    ).select_related('subject')[:5]
    
    # Group grades by subject
    grades_by_subject = {}
    for grade in grades:
        if grade.subject.name not in grades_by_subject:
            grades_by_subject[grade.subject.name] = []
        grades_by_subject[grade.subject.name].append({
            'exam_type': grade.exam_type,
            'marks': grade.marks_obtained,
            'total': grade.total_marks,
            'percentage': grade.percentage,
            'grade': grade.grade_letter
        })
    
    context = {
        'student': student_profile,
        'enrollments': enrollments,
        'enrollment_count': enrollments.count(),
        'grades': grades,
        'grades_count': grades.count(),
        'gpa': round(gpa, 2) if gpa else 'N/A',
        'attendance_rate': round(attendance_rate, 1),
        'pending_assignments': pending_assignments,
        'pending_count': pending_assignments.count(),
        'grades_by_subject': grades_by_subject,
    }
    
    return render(request, 'students/dashboard.html', context)

@login_required
def view_grades(request):
    if request.user.user_type != 'student':
        messages.error(request, 'Access denied.')
        return redirect('dashboard_redirect')
    
    student_profile = request.user.student_profile
    grades = Grade.objects.filter(
        student=student_profile
    ).select_related('subject', 'assignment').order_by('-uploaded_at')
    
    # Calculate summary statistics
    total_subjects = grades.values('subject').distinct().count()
    average_percentage = grades.aggregate(avg=Avg('percentage'))['avg']
    highest_grade = grades.order_by('-percentage').first()
    
    context = {
        'grades': grades,
        'total_subjects': total_subjects,
        'average_percentage': round(average_percentage, 2) if average_percentage else 0,
        'highest_grade': highest_grade,
    }
    return render(request, 'students/grades.html', context)

@login_required
def view_attendance(request):
    if request.user.user_type != 'student':
        messages.error(request, 'Access denied.')
        return redirect('dashboard_redirect')
    
    student_profile = request.user.student_profile
    attendance_records = Attendance.objects.filter(
        student=student_profile
    ).select_related('subject').order_by('-date')[:30]
    
    # Group by subject
    attendance_by_subject = {}
    for record in attendance_records:
        if record.subject.name not in attendance_by_subject:
            attendance_by_subject[record.subject.name] = {
                'total': 0,
                'present': 0
            }
        attendance_by_subject[record.subject.name]['total'] += 1
        if record.is_present:
            attendance_by_subject[record.subject.name]['present'] += 1
    
    context = {
        'attendance_records': attendance_records,
        'attendance_by_subject': attendance_by_subject,
    }
    return render(request, 'students/attendance.html', context)