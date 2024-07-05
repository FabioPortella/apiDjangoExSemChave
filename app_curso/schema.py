from ninja import ModelSchema, Schema

from .models import TipoCurso


class TipoCursoSchema(ModelSchema):
    class Config:
        model = TipoCurso 
        model_fields = ['id', 'nome', 'descricao']


class NotFoundSchema(Schema):
    message: str