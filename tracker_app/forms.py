from django.contrib.auth.forms import forms
from django.forms import ModelForm, inlineformset_factory, formset_factory, modelformset_factory
from .models import Subject, Task
from django.forms.widgets import DateTimeInput


class SubjectForm(ModelForm):
    class Meta:
        model = Subject
        fields = ['theme', 'description', 'max_score']
        widgets = {
            'theme': forms.TextInput(attrs={'placeholder': 'Тема', 'class': 'form-control'}, ),
            'description': forms.Textarea(attrs={'placeholder': 'Опис', 'class': 'form-control', 'rows': '5'}),
            'max_score': forms.TextInput(attrs={'placeholder': 'Максимальна кіл. балів', 'class': 'form-control'}),
        }


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        exclude = ['id', 'created_at']

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Назва', 'class': 'form-control'}, ),
            'score': forms.NumberInput(attrs={'placeholder': 'Кіл. балів', 'class': 'form-control'}),
            'deadline': forms.DateTimeInput(
                format=('%Y-%m-%d %H:%M'),
                attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'placeholder': 'Статус', 'class': 'form-control'}),
        }


TaskFormSet = inlineformset_factory(Subject, Task,
                                    form=TaskForm,
                                    extra=0
                                    )
# TaskFormSet = formset_factory(Task,
#                                 # form=TaskForm,
#                                     extra=0,
#                                     # widgets={
#                                     #     'name': forms.TextInput(
#                                     #         attrs={'placeholder': 'Назва', 'class': 'form-control'}, ),
#                                     #     'score': forms.NumberInput(
#                                     #         attrs={'placeholder': 'Кіл. балів', 'class': 'form-control'}),
#                                     #     'deadline': DateTimeInput(
#                                     #         format=('%Y-%m-%d %H:%M'),
#                                     #         attrs={'class': 'form-control',
#                                     #                "type": "datetime-local"}),
#                                     #     'subject': forms.Select(attrs={'class': 'form-control'}),
#                                     #     'status': forms.Select(
#                                     #         attrs={'placeholder': 'Статус', 'class': 'form-control'}),
#                                     # }
#                                     )
