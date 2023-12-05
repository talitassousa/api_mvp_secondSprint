from flask_openapi3 import OpenAPI, Info, Tag
from flask import Flask, request, jsonify, redirect, abort
from urllib.parse import unquote
import sqlite3
from fastapi import HTTPException
from fastapi import Path

from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from model import Session, Product
from logger import logger
from schemas import *
from flask_cors import CORS, cross_origin

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
cors = CORS(app)

app.config["CORS_HEADERS"] = "Content-Type"

db_name = "db.sqlite3"

# definindo tags
home_tag = Tag(
    name="Documentação",
    description="Seleção de documentação: Swagger, Redoc ou RapiDoc",
)
produto_tag = Tag(
    name="Produto", description="Visualização, adição, edição e remoção de produtos à base"
)
comentario_tag = Tag(
    name="Comentario",
    description="Adição de um comentário à um produtos cadastrado na base",
)


@app.get("/", tags=[home_tag])
@cross_origin()
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação."""
    return redirect("/openapi")

@app.get(
    "/products",
    tags=[produto_tag],
    responses={"200": ListagemProductsSchema, "404": ErrorSchema},
)
@cross_origin()
def get_products():
    """Faz a busca por todos os Produtos cadastrados

    Retorna uma representação da listagem de produtos.
    """
    session = Session()

    products = session.execute("SELECT * FROM product")

    products_json = [
        {
            "id": p[0],
            "nome": p[1],
            "recipiente": p[2],
            "quantidade": p[3],
            "valor": p[4],
        }
        for p in products
    ]
    return products_json


@app.get(
    "/product/",
    tags=[produto_tag],
    responses={"200": ProductViewSchema, "404": ErrorSchema},
)
@cross_origin()
def get_product(query: ProductBuscaSchema):
    """Faz a busca por um Produto a partir do id do produto

    Retorna uma representação dos produtos e comentários associados.
    """
    product_id = query.id
    logger.debug(f"Coletando dados sobre product #{product_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    product = session.query(Product).filter(Product.id == product_id).first()

    if not product:
        # se o produto não foi encontrado
        error_msg = "product não encontrado na base :/"
        logger.warning(f"Erro ao buscar product '{product_id}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"product encontrado: '{product.nome}'")
        # retorna a representação de produto
        return apresenta_product(product), 200



@app.post(
    "/product",
    tags=[produto_tag],
    responses={"200": ProductViewSchema, "409": ErrorSchema, "400": ErrorSchema},
)
@cross_origin()
def add_product(form: ProductSchema):
    """Adiciona um novo Produto à base de dados

    Retorna uma representação dos produtos e comentários associados.
    """
    product = Product(
        nome=form.nome,
        recipiente=form.recipiente,
        quantidade=form.quantidade,
        valor=form.valor,
    )
    logger.debug(f"Adicionando product de nome: '{product.nome}'")
    try:
        # criando conexão com a base
        session = Session()

        nome = form.nome
        recipiente = form.recipiente

        # Verificar se o produto já existe no banco de dados
        existing_product = (
            session.query(Product).filter_by(nome=nome, recipiente=recipiente).first()
        )

        if existing_product is not None:
            raise RuntimeError

        # adicionando produto
        session.add(product)

        # efetivando o comando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado product de nome: '{product.nome}'")
        return apresenta_product(product), 200

    except RuntimeError as runtimeError:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "produto de mesmo nome e recipiente já salvo na base :/"
        logger.warning(f"Erro ao adicionar product '{product.nome}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as error:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar product '{product.nome}', {error_msg}")
        return {"message": error_msg}, 400




@app.put(
    "/product/", tags=[produto_tag],
    responses={"200": ProductViewSchema, "409": ErrorSchema, "400": ErrorSchema}
)
@cross_origin()
def update_product(query: ProductBuscaSchema, form: ProductSchema):
    """Faz a edição de Produtos já cadastrados"""
    product_id = query.id
    try:
        # criando conexão com a base
        session = Session()

        # Verificar se o produto existe no banco de dados
        existing_product = (
            session.query(Product).filter(Product.id == product_id).first()
        )

        if existing_product is None:
            raise HTTPException(
                status_code=404, detail=f"Produto de id {product_id} não encontrado"
            )

        # Atualizar os campos do produto com os novos valores
        existing_product.nome = form.nome
        existing_product.recipiente = form.recipiente
        existing_product.quantidade = form.quantidade
        existing_product.valor = form.valor

        session.commit()
        logger.debug(f"Atualizado product de id: {product_id}")
        return apresenta_product(existing_product), 200

    except Exception as error:
        error_msg = f"Erro interno ao processar a requisição: {str(error)}"
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)


@app.delete("/product/",  tags=[produto_tag],
    responses={"200": ProductViewSchema, "409": ErrorSchema, "400": ErrorSchema})
@cross_origin()
def del_product(query: ProductBuscaSchema):
    """Deleta um Produto cadastrado 

    Retorna uma mensagem de confirmação da remoção.
    """
    product_id = query.id
    logger.debug(f"Coletando dados sobre product #{product_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    product = session.query(Product).filter(Product.id == product_id).first()

    if product:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletando dados sobre product #{product_id}")
        logger.debug(f"Deletado product #{product}")

        session.delete(product)
        session.commit()
        return {"message": "produto removido", "id": product_id}
    else:
        # se o produto não foi encontrado
        error_msg = "product não encontrado na base :/"
        logger.warning(f"Erro ao deletar product #'{product}', {error_msg}")
        return {"message": error_msg}, 404
