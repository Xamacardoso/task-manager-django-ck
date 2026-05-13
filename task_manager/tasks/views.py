from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import Task

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'  # define qual html que vai renderizar
    context_object_name = 'tasks'           # serve para acessar o tasks no html "{% for task in tasks %}"

    def get_queryset(self):
        # Apenas mostra as tarefas do usuário logado
        return Task.objects.filter(user=self.request.user)   