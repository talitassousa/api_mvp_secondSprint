from pydantic import BaseModel
from typing import Optional, List
from model.provider import Provider

from schemas import ComentarioSchema


class ProviderSchema(BaseModel):
    """Define como um novo product a ser inserido deve ser representado"""

    # id: int = 0
    nome: str = ""
    cnpj: str = ""
    cep: str = ""
    cidade: str = ""
    uf: str = ""


class ProviderBuscaSchema(BaseModel):
    """Define como deve ser a estrutura que representa a busca. Que será
    feita apenas com base no nome do product.
    """
    cnpj: str = ""
    


class ListagemProvidersSchema(BaseModel):
    """Define como uma listagem de products será retornada."""

    providers: List[ProviderSchema]

def apresenta_providers(providers: List[Provider]):
    """ Retorna uma representação do proider seguindo o schema definido em
        ProdutoViewSchema.
    """
    result = []
    for provider in provider:
        result.append({
            "nome": provider.nome,
            "cnpj": provider.cnpj,
            "cep": provider.cep,
            "cidade": provider.cidade,
            "uf":provider.uf,
        })

    return {"fornedores": result}


class ProviderViewSchema(BaseModel):
    """Define como um product será retornado: provider + comentários."""

    nome: str = "Mix beer distribuidora"
    cnpj: str = "85.222.870/0001-68"
    cep: str = "05570-990"
    cidade: str = "Brasilia"
    uf: str = "DF"
    


class ProviderDelSchema(BaseModel):
    """Define como deve ser a estrutura do dado retornado após uma requisição
    de remoção.
    """
    message: str
    nome: str

def apresenta_provider(provider: Provider):
    """Retorna uma representação do product seguindo o schema definido em
    productViewSchema.
    """
    return {
        "nome": provider.nome,
        "cnpj": provider.cnpj,
        "cep": provider.cep,
        "cidade": provider.cidade,
        "uf": provider.uf,
        "comentarios": [comentario.texto for comentario in provider.comentarios]
        if hasattr(provider, "comentarios") else []
    }
