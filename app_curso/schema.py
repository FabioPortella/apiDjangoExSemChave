from ninja import ModelSchema, Schema

from app_curso.models import Curso, TipoCurso

class TipoCursoSchema(ModelSchema):
    class Config:
        model = TipoCurso
        model_fields = ['id', 'nome', 'descricao']


class CursoSchema(ModelSchema):
    tipoDoCurso: TipoCursoSchema 

    class Config:
        model = Curso
        model_fields = ['id', 'nome', 'tipoDoCurso']


class CursoCreateSchema(Schema):
    nome: str
    tipoDoCurso: int
    

class NotFoundSchema(Schema):
    message: str

