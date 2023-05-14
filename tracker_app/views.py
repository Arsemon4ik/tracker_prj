from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from .forms import SubjectForm, TaskForm, TaskFormSet
from .models import Subject, Task
import json


@login_required()
def dashboard_page(request):
    """ Dashboard function returns a template with subjects and tasks from DB based on user """
    subject_form = SubjectForm()
    task_form = TaskForm()
    if request.method == 'POST':
        if "btn-subject" in request.POST:
            form = SubjectForm(request.POST)
            if form.is_valid():
                subject = form.save(commit=False)
                subject.user = request.user
                subject.save()
                return redirect('dashboard')
        if "btn-task" in request.POST:
            form = TaskForm(request.POST)
            if form.is_valid():
                subject = form.save(commit=False)
                subject.user = request.user
                subject.save()
                return redirect('dashboard')
    subjects = Subject.objects.filter(user=request.user)
    tasks = Task.objects.filter(user=request.user)
    from .filters import TaskFilter
    # tasks = TaskFilter(request.GET, queryset=tasks)

    subject_names = [subject.theme for subject in subjects]
    parsed_names = json.dumps(subject_names, ensure_ascii=False)

    from django.db.models import Sum, Count
    subjects = subjects.annotate(task_per_subject=Count('task'))
    task_per_subject = [subject.task_per_subject for subject in subjects]
    # parsed_names = json.dumps(subject_names, ensure_ascii=False)
    # print(parsed_names)
    context = {'subjects': subjects, 'tasks': tasks,
               'task_form': task_form, 'subject_form': subject_form,
               'subject_names': parsed_names, 'task_per_subject': task_per_subject,
               }
    return render(request, 'tracker_app/dashboard.html', context=context)


@login_required()
def tasks_by_subject_page(request, subject_id):
    """ Dashboard function returns a template with subjects and tasks from DB based on user """

    subject = Subject.objects.filter(id=subject_id, user=request.user).first()

    if not subject:
        raise ObjectDoesNotExist()

    form = TaskForm()
    formset = TaskFormSet(instance=subject)
    # print(tasks)
    if request.method == "POST":
        if 'add_task' in request.POST:
            # print("ADDING")
            form = TaskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.user = request.user
                task.subject = subject
                task.save()
                return redirect('tasks_by_subject', subject.id)
            else:
                messages.error(request, f'Виникла помилка: {form.errors} під час створення, спробуйте ще раз')
        if 'edit_task' in request.POST:
            # print("EDIT")
            user = request.user
            formset = TaskFormSet(request.POST, instance=subject)
            if formset.is_valid():
                formset = formset.save(commit=False)
                for form in formset:
                    form.user = user
                    form.save()
                return redirect('tasks_by_subject', subject.id)
            else:
                # print(formset.get_form_error())
                messages.error(request, f'Виникла помилка: {formset.errors} під час створення, спробуйте ще раз')

    from django.db.models import Count, Case, When, IntegerField, Sum
    tasks = subject.task_set.filter(user=request.user)


    total = tasks.aggregate(total_score=Sum('score'), count_done=Count(Case(When(status="done", then=1),
                                                                            output_field=IntegerField())))

    context = {'subject': subject.theme, 'tasks': tasks,
               'formset': formset, 'form': form, 'total_score': total['total_score'],
               'total_done': total['count_done']}
    return render(request, 'tracker_app/tasks_by_subject.html', context=context)


@login_required()
def tasks_page(request):
    """ Dashboard function returns a template with subjects and tasks from DB based on user """
    tasks = Task.objects.filter(user=request.user)
    context = {'tasks': tasks}
    return render(request, 'tracker_app/tasks.html', context=context)


# @login_required()
# def create_subject_page(request):
#     """ Subject function returns a template with subjects and tasks from DB based on user """
#     form = SubjectForm()
#     if request.method == 'POST':
#         form = SubjectForm(request.POST)
#         if form.is_valid():
#             subject = form.save(commit=False)
#             subject.user = request.user
#             subject.save()
#             return redirect('dashboard')
#         else:
#             messages.error(request, 'Something wrong with creating, please try again')
#     return render(request, 'authentication/register.html', {'form': form})

@login_required()
def edit_subject_page(request, subject_id):
    """ Subject function returns a template with subjects and tasks from DB based on user """
    subject = Subject.objects.filter(id=subject_id, user=request.user).first()
    if not subject:
        ...
        # raise 404 page
    form = SubjectForm(instance=subject)
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
        else:
            messages.error(request, 'Виникла помилка під час редагування, спробуйте ще раз')
    return render(request, 'tracker_app/edit_subject.html', {'form': form, 'subject_theme': subject.theme})


@login_required()
def edit_task_page(request, task_id):
    """ Subject function returns a template with subjects and tasks from DB based on user """
    task = Task.objects.filter(id=task_id, user=request.user).first()
    if not task:
        raise ObjectDoesNotExist()
        # raise 404 page
    form = TaskForm(instance=task)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('dashboard')
        else:
            # print(form.ge)
            messages.error(request, f'Виникла помилка {form.errors} під час редагування, спробуйте ще раз')
    return render(request, 'tracker_app/edit_task.html', {'task_name': task.name, 'form': form})


@login_required()
def delete_subject(request, subject_id):
    """ Dashboard function returns a template with subjects and tasks from DB based on user """
    subject = Subject.objects.filter(id=subject_id, user=request.user).first()
    if subject:
        subject.delete()
        return redirect('dashboard')
    return render(request, 'tracker_app/tasks_by_subject.html', {})


@login_required()
def delete_task(request, task_id):
    """ Dashboard function returns a template with subjects and tasks from DB based on user """
    task = Task.objects.filter(id=task_id, user=request.user).first()
    if task:
        task.delete()
        return redirect('dashboard')
    return render(request, 'tracker_app/tasks_by_subject.html', {})


@login_required()
def update_subject_page(request):
    """ Dashboard function returns a template with subjects and tasks from DB based on user """
    subjects = Subject.objects.filter(user=request.user)
    context = {'subjects': subjects}
    return render(request, 'tracker_app/dashboard.html', context=context)


@login_required()
def delete_subject_page(request):
    """ Dashboard function returns a template with subjects and tasks from DB based on user """
    subjects = Subject.objects.filter(user=request.user)
    context = {'subjects': subjects}
    return render(request, 'tracker_app/dashboard.html', context=context)
