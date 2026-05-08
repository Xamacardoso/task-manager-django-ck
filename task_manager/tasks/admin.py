from django.contrib import admin
from .models import Task


# Register your models here.

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    # Campos que serão exibidos na lista de tarefas
    list_display = ('title', 'user', 'due_date', 'is_completed', 'created', 'modified')

    # Filtros que serão exibidos na barra lateral
    list_filter = ('is_completed', 'due_date', 'user')

    # Campos que serão pesquisados
    search_fields = ('title', 'description', 'user__username', 'user__email')
    
    # Campos que não poderão ser editados no admin
    readonly_fields = ('created', 'modified', 'completed_at')

    # Ordenação padrão
    ordering = ('-created',)
