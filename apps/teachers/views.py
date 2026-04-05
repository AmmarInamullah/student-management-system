from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
from .models import TeacherProfile, Assignment, Grade, Salary
from apps.students.models import Subject, StudentProfile, Enrollment
from .forms import AssignmentForm


@login_required
def teacher_dashboard(request):
    if request.user.user_type != 'teacher':
        messages.error(request, 'Access denied.')
        return redirect('dashboard_redirect')
    
    try:
        teacher = request.user.teacher_profile
    except:
        messages.error(request, 'Teacher profile not found.')
        return redirect('dashboard_redirect')
    
    subjects = teacher.subjects_taught.all()
    students_count = StudentProfile.objects.filter(
        enrollments__subject__in=subjects
    ).distinct().count()
    
    recent_assignments = Assignment.objects.filter(
        teacher=teacher
    ).order_by('-created_at')[:5]
    
    pending_grades = Assignment.objects.filter(
        teacher=teacher,
        status='published'
    ).exclude(
        grade__isnull=False
    ).count()
    
    current_month = timezone.now().replace(day=1).date()
    current_salary = Salary.objects.filter(
        teacher=teacher,
        month=current_month
    ).first()
    
    context = {
        'teacher': teacher,
        'subjects': subjects,
        'subjects_count': subjects.count(),
        'students_count': students_count,
        'recent_assignments': recent_assignments,
        'pending_grades': pending_grades,
        'current_salary': current_salary,
    }
    
    return render(request, 'teachers/dashboard.html', context)


@login_required
def create_assignment(request):
    if request.user.user_type != 'teacher':
        messages.error(request, 'Access denied.')
        return redirect('dashboard_redirect')
    
    teacher = request.user.teacher_profile
    
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.teacher = teacher
            assignment.save()
            messages.success(request, f'Assignment "{assignment.title}" created successfully!')
            return redirect('teacher_dashboard')
    else:
        form = AssignmentForm()
        form.fields['subject'].queryset = teacher.subjects_taught.all()
    
    return render(request, 'teachers/create_assignment.html', {'form': form})


@login_required
def upload_grades(request, assignment_id=None):
    teacher = request.user.teacher_profile
    
    if assignment_id:
        assignment = get_object_or_404(Assignment, id=assignment_id, teacher=teacher)
        students = StudentProfile.objects.filter(
            enrollments__subject=assignment.subject,
            enrollments__is_active=True
        ).distinct()
        
        if request.method == 'POST':
            for student in students:
                marks = request.POST.get(f'marks_{student.id}')
                exam_type = request.POST.get(f'exam_type_{student.id}', 'Assignment')
                
                if marks and marks.strip():
                    Grade.objects.update_or_create(
                        student=student,
                        subject=assignment.subject,
                        assignment=assignment,
                        defaults={
                            'marks_obtained': float(marks),
                            'total_marks': assignment.total_marks,
                            'exam_type': exam_type,
                            'uploaded_by': teacher
                        }
                    )
            messages.success(request, f'Grades uploaded for {assignment.title}!')
            return redirect('teacher_dashboard')
        
        context = {
            'assignment': assignment,
            'students': students,
        }
        return render(request, 'teachers/upload_grades.html', context)
    
    pending_assignments = Assignment.objects.filter(
        teacher=teacher,
        status='published'
    ).exclude(
        grade__isnull=False
    ).distinct()
    
    return render(request, 'teachers/grade_assignments.html', {
        'pending_assignments': pending_assignments
    })


@login_required
def salary_view(request):
    if request.user.user_type != 'teacher':
        messages.error(request, 'Access denied.')
        return redirect('dashboard_redirect')
    
    try:
        teacher = request.user.teacher_profile
    except:
        messages.error(request, 'Teacher profile not found.')
        return redirect('dashboard_redirect')
    
    salaries = Salary.objects.filter(teacher=teacher).order_by('-month')
    
    total_earned = salaries.aggregate(total=Sum('net_amount'))['total'] or 0
    total_paid = salaries.filter(payment_status='paid').aggregate(total=Sum('net_amount'))['total'] or 0
    total_pending = salaries.filter(payment_status='pending').aggregate(total=Sum('net_amount'))['total'] or 0
    
    context = {
        'salaries': salaries,
        'total_earned': total_earned,
        'total_paid': total_paid,
        'total_pending': total_pending,
    }
    return render(request, 'teachers/salary.html', context)


@login_required
def view_subject_students(request, subject_id):
    if request.user.user_type != 'teacher':
        messages.error(request, 'Access denied.')
        return redirect('dashboard_redirect')
    
    try:
        subject = Subject.objects.get(id=subject_id)
        teacher = request.user.teacher_profile
        
        if subject not in teacher.subjects_taught.all():
            messages.error(request, 'You are not authorized to view this subject.')
            return redirect('teacher_dashboard')
        
        enrollments = Enrollment.objects.filter(
            subject=subject,
            is_active=True
        ).select_related('student', 'student__user')
        
        students = [e.student for e in enrollments]
        
        grades = Grade.objects.filter(
            subject=subject,
            student__in=students
        ).select_related('student')
        
        grade_dict = {}
        for grade in grades:
            grade_dict[grade.student.id] = grade
        
        context = {
            'subject': subject,
            'students': students,
            'grades': grade_dict,
            'student_count': len(students),
        }
        return render(request, 'teachers/subject_students.html', context)
        
    except Subject.DoesNotExist:
        messages.error(request, 'Subject not found.')
        return redirect('teacher_dashboard')