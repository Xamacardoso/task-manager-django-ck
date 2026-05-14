from task_manager.tasks.views import TaskToggleCompleteView
from django.urls import path

from task_manager.tasks.views import TaskDeleteView, TaskUpdateView, TaskCreateView, TaskListView


app_name = "tasks"
urlpatterns = [
    path('', TaskListView.as_view(), name='task_list'),
    path('create/', TaskCreateView.as_view(), name='task_create'),
    path('<int:pk>/update/', TaskUpdateView.as_view(), name='task_update'),
    path('<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),

    path('<int:pk>/toggle/', TaskToggleCompleteView.as_view(), name='task_toggle_complete'),
]