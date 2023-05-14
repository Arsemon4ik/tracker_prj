from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_page, name='dashboard'),
    path('subject/<int:subject_id>', views.edit_subject_page, name='edit_subject'),
    path('tasks', views.tasks_page, name='tasks'),
    path('subject/<int:subject_id>/tasks', views.tasks_by_subject_page, name='tasks_by_subject'),
    path('tasks/<int:task_id>', views.edit_task_page, name='edit_task'),
    path('create', views.dashboard_page, name='create_subject'),
    path('subject/delete/<int:subject_id>', views.delete_subject, name='delete_subject'),
    path('task/delete/<int:task_id>', views.delete_task, name='delete_task'),
]
