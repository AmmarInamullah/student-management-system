from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('grades/', views.view_grades, name='student_grades'),
    path('attendance/', views.view_attendance, name='student_attendance'),
]