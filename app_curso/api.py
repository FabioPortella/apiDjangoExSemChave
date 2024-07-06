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
    
@api.post('/tipocurso', response={201: TipoCursoSchema, 400: NotFoundSchema})
def inserir(request, tipoCurso: TipoCursoSchema) -> TipoCurso:
    try:
        # Verifica se o nome tem menos de três caracteres ou se é composto apenas por espaços em branco
        if len(tipoCurso.nome.strip()) < 3:
            return 400, {"message": "O nome do Tipo de Curso deve ter pelo menos três caracteres e não pode ser composto por espaços em branco."}
        
        # Verifica se já existe um TipoCurso com o mesmo nome
        if TipoCurso.objects.filter(nome=tipoCurso.nome).exists():
            return 400, {"message": "Tipo de Curso com este nome já existe."}
        
        # Cria um novo TipoCurso
        tipoCurso = TipoCurso.objects.create(**tipoCurso.dict())
        return 201, tipoCurso
    except Exception as e:
        return 400, {"message": "Erro ao salvar um novo Tipo de Curso"}
    

@api.put('/tipocurso/{id}', response={200: TipoCursoSchema, 404: NotFoundSchema, 400: NotFoundSchema})
def atualizar(request, id: int, tipoCurso: TipoCursoSchema) -> TipoCurso:
    try:
        # Verifica se o TipoCurso existe
        try:
            tipo_curso_atual = TipoCurso.objects.get(pk=id)
        except TipoCurso.DoesNotExist:
            return 404, {"message": "Tipo de Curso não encontrado."}
        
        # Verifica se o nome tem menos de três caracteres ou se é composto apenas por espaços em branco
        if len(tipoCurso.nome.strip()) < 3:
            return 400, {"message": "O nome do Tipo de Curso deve ter pelo menos três caracteres e não pode ser composto por espaços em branco."}
        
        # Atualiza os dados do TipoCurso
        tipo_curso_atual.nome = tipoCurso.nome
        tipo_curso_atual.descricao = tipoCurso.descricao
        tipo_curso_atual.save()
        
        return 200, tipo_curso_atual
    except Exception as e:
        return 400, {"message": "Erro ao atualizar o Tipo de Curso"}

