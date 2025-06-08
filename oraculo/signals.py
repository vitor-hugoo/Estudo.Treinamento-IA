from django.db.models.signals import post_save
from django.dispatch import receiver
from oraculo.models import Treinamento
from django_q.tasks import async_task


@receiver(post_save, sender=Treinamento)
def signals_treinamento_ia(sender, instance, created, **kwargs):
    if created:
        async_task('oraculo.tasks.task_treinar_ia',instance.id)
