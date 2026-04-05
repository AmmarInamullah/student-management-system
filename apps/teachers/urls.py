from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('assignments/create/', views.create_assignment, name='create_assignment'),
    path('grades/upload/', views.upload_grades, name='upload_grades'),
    path('grades/upload/<int:assignment_id>/', views.upload_grades, name='upload_grades'),
    path('salary/', views.salary_view, name='teacher_salary'),
    path('subject/<int:subject_id>/students/', views.view_subject_students, name='view_subject_students'),
]