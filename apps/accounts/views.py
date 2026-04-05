from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard_redirect')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name()}!')
            
            if user.user_type == 'student':
                return redirect('student_dashboard')
            elif user.user_type == 'teacher':
                return redirect('teacher_dashboard')
            elif user.user_type == 'management':
                return redirect('management_dashboard')
            else:
                return redirect('/admin/')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')
    
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

@login_required
def dashboard_redirect(request):
    if request.user.user_type == 'student':
        return redirect('student_dashboard')
    elif request.user.user_type == 'teacher':
        return redirect('teacher_dashboard')
    elif request.user.user_type == 'management':
        return redirect('management_dashboard')
    else:
        return redirect('/admin/')