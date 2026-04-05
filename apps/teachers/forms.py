from django import forms
from .models import Assignment, Grade

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['subject', 'title', 'description', 'file', 'due_date', 'total_marks', 'status']
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'total_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Limit subjects to those taught by the teacher
        if 'initial' in kwargs and 'teacher' in kwargs['initial']:
            teacher = kwargs['initial']['teacher']
            self.fields['subject'].queryset = teacher.subjects_taught.all()

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['marks_obtained', 'exam_type', 'remarks']
        widgets = {
            'marks_obtained': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'exam_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Midterm, Final, Quiz'}),
            'remarks': forms.Textarea(attrs={'rows': 2, 'class': 'form-control', 'placeholder': 'Optional remarks'}),
        }