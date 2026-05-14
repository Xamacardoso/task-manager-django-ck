from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views import View
from django.shortcuts import get_object_or_404, redirect

from django.http import JsonResponse

from .models import Task
from .forms import TaskForm

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'  # define qual html que vai renderizar
    context_object_name = 'tasks'           # serve para acessar o tasks no html "{% for task in tasks %}"

    def get_queryset(self):
        # Apenas mostra as tarefas do usuário logado
        return Task.objects.filter(user=self.request.user)   

class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task

    # nao precisa do fields porque ja tem no form
    form_class = TaskForm
    template_name = 'tasks/task_form.html'

    # quando clicar em salvar, ele vai redirecionar para a lista de tarefas. estrutura é <app_name>:<path_name>. path name vem de urls.py
    success_url = reverse_lazy('tasks:task_list') 

    success_message = 'Tarefa criada com sucesso!'
    
    def form_valid(self, form):
        # aqui conseguimos acessar o self.request.user para injetar
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # serve para passar info para o html, junto com o form
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Criar Tarefa'
        return context 


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:task_list')
    
    success_message = 'Tarefa atualizada com sucesso!'

    def get_queryset(self):
        # Apenas mostra as tarefas do usuário logado
        return Task.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        # serve para passar info para o html, junto com o form
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Editar Tarefa'
        return context 

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('tasks:task_list')

    success_message = 'Tarefa excluída com sucesso!'

    def get_queryset(self):
        # Apenas mostra as tarefas do usuário logado
        return Task.objects.filter(user=self.request.user)
    
    def form_valid(self, form):
        # no delete usamos o messages.success para fazer o popup aparecer antes do redirecionamento
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

class TaskToggleCompleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        # busca tarefa específica do usuario logado
        task = get_object_or_404(Task, pk=pk, user=request.user)
        task.is_completed = not task.is_completed
        task.save()

        # mensagem de sucesso
        estado = 'concluída' if task.is_completed else 'pendente'
        
        # verifica se o pedido foi feito por javascript (ajax)
        accept_header = request.headers.get('Accept', '')
        if 'application/json' in accept_header:
            return JsonResponse({
                'message': f'Tarefa marcada como {estado}!',
                'is_completed': task.is_completed,
                'status': 'success'
            })


        messages.success(request, f'Tarefa marcada como {estado}!')
        return redirect('tasks:task_list')