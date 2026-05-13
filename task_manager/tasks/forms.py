from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date']

        widgets  = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título da tarefa'
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descrição da tarefa'
            }),
            'due_date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),
        }




