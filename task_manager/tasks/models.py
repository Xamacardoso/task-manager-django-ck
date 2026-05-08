from django.conf import settings
from django.db import models
from django.utils import timezone
from model_utils.models import TimeStampedModel

# Timestamped model usa created e modified atualizados automaticamente
class Task(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name='Usuário' # verbose faz com que os nomes dos campos sejam exibidos em portugues no admin
    )

    title = models.CharField(
        max_length=255,
        verbose_name='Título'
    )
    
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descrição'
    )

    due_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='Data de Prazo'
    )

    is_completed = models.BooleanField(
        default=False,
        verbose_name='Está Concluída?'
    )

    completed_at = models.DateTimeField(
        blank=True, # blank faz com que o campo seja opcional no formulário
        null=True, # null faz com que o campo seja opcional no banco de dados, permitindo valores None
        verbose_name='Data de Conclusão'
    )

    class Meta:
        ordering = ['-created']
        verbose_name = 'Tarefa'
        verbose_name_plural = 'Tarefas'

    def __str__(self):
        return self.title
    
    # sobrescreve o metodo save do modelo para adicionar logica
    def save(self, *args, **kwargs):
        if self.is_completed and not self.completed_at:
            self.completed_at = timezone.now()
        # Se a tarefa for desmarcada como concluída, removemos a data de conclusão
        elif not self.is_completed and self.completed_at:
            self.completed_at = None

        super().save(*args, **kwargs)