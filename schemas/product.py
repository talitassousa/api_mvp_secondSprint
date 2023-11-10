from pydantic import BaseModel
from typing import Optional, List
from model.product import Product

from schemas import ComentarioSchema


class ProductSchema(BaseModel):
    """Define como um novo product a ser inserido deve ser representado"""

    id: int = 0
    nome: str = "FANTA"
    recipiente: float = 0.6
    quantidade: Optional[int] = 5
    valor: float = 7.50


class ProductBuscaSchema(BaseModel):
    """Define como deve ser a estrutura que representa a busca. Que será
    feita apenas com base no nome do product.
    """

    nome: str = "Teste"


class ListagemProductsSchema(BaseModel):
    """Define como uma listagem de products será retornada."""

    products: List[ProductSchema]


# def apresenta_products(products: List[Product]):
#     """Retorna uma representação do produto seguindo o schema definido em
#     ProdutoViewSchema.
#     """
#     result = []
#     for product in products:
#         result.append(
#             {
#                 "nome": product.nome,
#                 "recipiente": product.recipiente,
#                 "quantidade": product.quantidade,
#                 "valor": product.valor,
#             }
#         )


#     return {"products": result}
# def apresenta_products(products: List[Product]) -> List[dict]:
#     """Retorna uma representação do product seguindo o schema definido em
#     productViewSchema.
#     """

#     return [
#         {
#             "id": product.id,
#             "nome": product.nome,
#             "recipiente": product.recipiente,
#             "quantidade": product.quantidade,
#             "valor": product.valor,
#         }
#         for product in products
#     ]

    # result = []
    # for product in products:
    #     result.append(
    #         {
    #             "id": product.id,
    #             "nome": product.nome,
    #             "recipiente": product.recipiente,
    #             "quantidade": product.quantidade,
    #             "valor": product.valor,
    #         }
    #     )

    # return result


class ProductViewSchema(BaseModel):
    """Define como um product será retornado: product + comentários."""

    id: int = 1
    nome: str = "Banana Prata"
    quantidade: Optional[int] = 12
    valor: float = 12.50
    total_cometarios: int = 1
    comentarios: List[ComentarioSchema]


class ProductDelSchema(BaseModel):
    """Define como deve ser a estrutura do dado retornado após uma requisição
    de remoção.
    """

    mesage: str
    nome: str


def apresenta_product(product: Product):
    """Retorna uma representação do product seguindo o schema definido em
    productViewSchema.
    """
    return {
        "id": product.id,
        "nome": product.nome,
        "recipente": product.recipiente,
        "quantidade": product.quantidade,
        "valor": product.valor,
        "total_cometarios": len(product.comentarios),
        "comentarios": [{"texto": c.texto} for c in product.comentarios],
    }
