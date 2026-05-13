from task_manager.tasks.views import TaskUpdateView
from task_manager.tasks.views import TaskCreateView
from django.urls import path
from .views import TaskListView

app_name = "tasks"
urlpatterns = [
    path('', TaskListView.as_view(), name='task_list'),
    path('create/', TaskCreateView.as_view(), name='task_create'),
    path('<int:pk>/update/', TaskUpdateView.as_view(), name='task_update'),
]