from django.db import models

# Create your models here.


class Treinamento(models.Model):
    site = models.URLField()
    conteudo = models.TextField()
    documento = models.FileField(upload_to='documentos')

    def __str__(self):
        return self.site
