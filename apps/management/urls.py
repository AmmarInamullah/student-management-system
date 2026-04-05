from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.management_dashboard, name='management_dashboard'),
    path('students/', views.manage_students, name='manage_students'),
    path('teachers/', views.manage_teachers, name='manage_teachers'),
]