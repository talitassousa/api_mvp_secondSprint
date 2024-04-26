from pydantic import BaseModel
from typing import Optional, List
from model.product import Product

from schemas import ComentarioSchema


class ProductSchema(BaseModel):
    """Define como um novo product a ser inserido deve ser representado"""

    # id: int = 0
    nome: str = ""
    recipiente: float = 0.6
    quantidade: Optional[int] = 5
    valor: float = 7.50
    fornecedor: str = ""



class ProductBuscaSchema(BaseModel):
    """Define como deve ser a estrutura que representa a busca. Que será
    feita apenas com base no nome do product.
    """
    id: int = 0


class ListagemProductsSchema(BaseModel):
    """Define como uma listagem de products será retornada."""

    products: List[ProductSchema]

def apresenta_products(products: List[Product]):
    """ Retorna uma representação do produto seguindo o schema definido em
        ProdutoViewSchema.
    """
    result = []
    for product in products:
        result.append({
            "nome": product.nome,
            "recipiente": product.recipiente,
            "quantidade": product.quantidade,
            "valor": product.valor,
            "fornecedor": product.fornecedor,
        })

    return {"produtos": result}


class ProductViewSchema(BaseModel):
    """Define como um product será retornado: product + comentários."""

    id: int = 1
    nome: str = "Fanta"
    recipiente: float = 0.6
    quantidade: Optional[int] = 12
    valor: float = 12.50
    fornecedor: str = "Mys Distribuidora"
    total_cometarios: int = 1
    comentarios: List[ComentarioSchema]


class ProductDelSchema(BaseModel):
    """Define como deve ser a estrutura do dado retornado após uma requisição
    de remoção.
    """
    message: str
    nome: str

def apresenta_product(product: Product):
    """Retorna uma representação do product seguindo o schema definido em
    productViewSchema.
    """
    return {
        "id": product.id,
        "nome": product.nome,
        "recipiente": product.recipiente,
        "quantidade": product.quantidade,
        "valor": product.valor,
        "fornecedor": product.fornecedor,
        "total_cometarios": len(product.comentarios),
        "comentarios": [{"texto": c.texto} for c in product.comentarios],
    }
