from django.db import models


class TipoCurso(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.CharField(max_length=100)

    class Meta:
        ordering = ['nome']

    def __str__(self) -> str:
        return self.nome
    

class Curso(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    tipo_curso_id = models.ForeignKey(TipoCurso, on_delete=models.CASCADE)

    class Meta:
        ordering = ['nome']

    def __str__(self) -> str:
        return self.nome
    

