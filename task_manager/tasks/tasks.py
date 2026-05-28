import csv
from io import StringIO
from celery import shared_task
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from .models import Task

User = get_user_model()

# Avisa ao celery que essa função é uma task a ser executada em background
@shared_task
def export_tasks_report (user_id, user_email):
    # busca as tarefas do usuário
    tasks = Task.objects.filter(user_id=user_id)

    # cria um buffer em memoria para armazenar o csv
    try:
        buffer = StringIO()
        writer = csv.writer(buffer)

        # escreve o cabeçalho
        writer.writerow(['ID', 'Título', 'Descrição', 'Data de Prazo', 'Status'])

        # adiciona cada tarefa ao csv
        for task in tasks:
            status = 'Concluida' if task.is_completed else 'Pendente'
            prazo = task.due_date.strftime('%d/%m/%Y %H:%M') if task.due_date else 'Sem Prazo'
            writer.writerow([
                task.id,
                task.title,
                task.description,
                prazo,
                status
            ])

        # prepara o email
        msg = EmailMessage(
            subject='Relatório de Tarefas',
            body='Segue em anexo o relatório de suas tarefas.',
            from_email="sistema@taskmanager.com",
            to=[user_email],
        )

        # anexa o csv
        msg.attach('tasks_report.csv', buffer.getvalue(), 'text/csv')

        # envia o email
        msg.send()

        return f"Relatório enviado com sucesso para {user_email}"

    except Exception as e:
        return f"Erro ao gerar relatório: {str(e)}"