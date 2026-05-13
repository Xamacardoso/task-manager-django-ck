from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
    
from .models import Task
from .forms import TaskForm

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'  # define qual html que vai renderizar
    context_object_name = 'tasks'           # serve para acessar o tasks no html "{% for task in tasks %}"

    def get_queryset(self):
        # Apenas mostra as tarefas do usuário logado
        return Task.objects.filter(user=self.request.user)   

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task

    # nao precisa do fields porque ja tem no form
    form_class = TaskForm
    template_name = 'tasks/task_form.html'

    # quando clicar em salvar, ele vai redirecionar para a lista de tarefas. estrutura é <app_name>:<path_name>. path name vem de urls.py
    success_url = reverse_lazy('tasks:task_list') 
    
    def form_valid(self, form):
        # aqui conseguimos acessar o self.request.user para injetar
        form.instance.user = self.request.user
        return super().form_valid(form)