from typing import List
from ninja import NinjaAPI

from .schema import NotFoundSchema, TipoCursoSchema
from .models import Curso, TipoCurso

api = NinjaAPI()


@api.get('/tipocurso', response=List[TipoCursoSchema])
def listar(request):
    return TipoCurso.objects.all()


@api.get('/tipocurso/{id}', response={200: TipoCursoSchema, 404: NotFoundSchema})
def obter(request, id: int):
    try:
        tipocurso = TipoCurso.objects.get(pk=id)
        return tipocurso
    except TipoCurso.DoesNotExist as e:
        return 404, {"message": "Tipo de Curso não cadastrado"}