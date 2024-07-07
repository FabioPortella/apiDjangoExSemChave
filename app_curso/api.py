from typing import Optional, List
from django.shortcuts import get_object_or_404
from django.db.models import Q
from ninja import NinjaAPI

from .schema import CursoCreateSchema, NotFoundSchema, TipoCursoSchema, CursoSchema
from .models import Curso, TipoCurso

api = NinjaAPI()

@api.get('/tipocurso', response={200: List[TipoCursoSchema], 400: NotFoundSchema, 404: NotFoundSchema})
def listar(request, nome: Optional[str] = None):
    try:
        if nome:
            tipo_curso = TipoCurso.objects.filter(nome__icontains=nome)
            if not tipo_curso:
                return 404, {"message": "Este NOME não está cadastrado como Tipo de Curso"}
            return 200, TipoCurso.objects.filter(nome__icontains=nome)
        return 200, TipoCurso.objects.all() 
    except Exception as e:
        return 400, {"message": "Erro ao listar Tipo de Curso"}


@api.get('/tipocurso/{id}', response={200: TipoCursoSchema, 404: NotFoundSchema})
def obter(request, id: int):
    try:
        tipocurso = TipoCurso.objects.get(pk=id)
        return 200, tipocurso
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
def atualizar(request, id: int, tipoCursoAlterado: TipoCursoSchema) -> TipoCursoSchema:
    try:
        # Verifica se o TipoCurso existe
        tipo_curso_atual = get_object_or_404(TipoCurso, pk=id)
        
        # Verifica se o nome tem menos de três caracteres ou se é composto apenas por espaços em branco
        if len(tipoCursoAlterado.nome.strip()) < 3:
            return 400, {"message": "O nome do Tipo de Curso deve ter pelo menos três caracteres e não pode ser composto por espaços em branco."}
        
        # Verifica se o nome alterado já existe em outro registro
        if TipoCurso.objects.filter(Q(nome=tipoCursoAlterado.nome) & ~Q(pk=id)).exists():
            return 400, {"message": "O nome do Tipo de Curso já está em uso."}

        # Atualiza os dados do TipoCurso
        for attribute, value in tipoCursoAlterado.dict().items():
            setattr(tipo_curso_atual, attribute, value)
        tipo_curso_atual.save()        
        
        return 200, tipo_curso_atual
    
    except TipoCurso.DoesNotExist:
        return 404, {"message": "Tipo de Curso não encontrado."}
    
    except Exception as e:
        return 400, {"message": f"Erro ao atualizar o Tipo de Curso: {str(e)}"}
    

@api.delete('/tipocurso/{id}', response={200: None, 404: NotFoundSchema, 400: NotFoundSchema})
def remover(request, id: int):
    try:
        try:
            tipo_curso = TipoCurso.objects.get(pk=id)
        except TipoCurso.DoesNotExist:
            return 404, {"message": "Tipo de Curso não encontrado."}
        
        tipo_curso.delete()
        return 200, {"message": "Tipo Curso removido com sucesso"}
    except Exception as e:
        return 400, {"message": "Erro ao excluir o Tipo de Curso"}


@api.get("/curso", response={200: List[CursoSchema], 400: NotFoundSchema, 404: NotFoundSchema})
def listar_cursos(request, nome: Optional[str] = None):
    try:
        if nome:
            cursos = Curso.objects.filter(nome__icontains=nome).select_related('tipoDoCurso')
            if not cursos:
                return 404, {"message": "Este NOME não está cadastrado como Curso"}    
        cursos = Curso.objects.all().select_related('tipoDoCurso')
        return 200, cursos
    except Exception as e:
        return 400, {"message": "Erro ao listar Cursos"}
  
   
@api.get('/curso/{id}', response={200: CursoSchema, 404: NotFoundSchema})
def obter_curso(request, id: int):
    try:
        curso = Curso.objects.get(pk=id)
        return 200, curso
    except Curso.DoesNotExist as e:
        return 404, {"message": "Curso não cadastrado"}


@api.post("/curso", response={201: CursoSchema, 404: NotFoundSchema})
def inserir_curso(request, payload: CursoCreateSchema):
    try:
        tipo_do_curso = TipoCurso.objects.get(id=payload.tipoDoCurso)
    except TipoCurso.DoesNotExist:
        return 404, {"message": "Tipo do Curso não existe"}
    
    curso = Curso.objects.create(
        nome=payload.nome,
        tipoDoCurso=tipo_do_curso
    )
    return 201, curso

@api.delete('/curso/{id}', response={200: None, 404: NotFoundSchema, 400: NotFoundSchema})
def remover_curso(request, id: int):
    try:
        try:
            curso = Curso.objects.get(pk=id)
        except Curso.DoesNotExist:
            return 404, {"message": "Curso não encontrado."}
        
        curso.delete()
        return 200, {"message": "Curso removido com sucesso"}
    except Exception as e:
        return 400, {"message": "Erro ao excluir Curso"}
