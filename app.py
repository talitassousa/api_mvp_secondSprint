from flask_openapi3 import OpenAPI, Info, Tag
from flask import Flask, request, jsonify, redirect, abort
from urllib.parse import unquote
import sqlite3
from fastapi import HTTPException

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
    name="Produto", description="Adição, visualização e remoção de produtos à base"
)
comentario_tag = Tag(
    name="Comentario",
    description="Adição de um comentário à um produtos cadastrado na base",
)


@app.get("/", tags=[home_tag])
@cross_origin()
def home():
    return redirect("/openapi")


@app.post(
    "/product",
)
@cross_origin()
def add_product(form: ProductSchema):
    product = Product(
        nome=form.nome,
        recipiente=form.recipiente,
        quantidade=form.quantidade,
        valor=form.valor,
    )
    logger.debug(f"Adicionando product de nome: '{product.nome}'")
    try:
        session = Session()

        nome = form.nome
        recipiente = form.recipiente

        # Verificar se o produto já existe no banco de dados
        existing_product = (
            session.query(Product).filter_by(nome=nome, recipiente=recipiente).first()
        )

        if existing_product is not None:
            raise RuntimeError

        session.add(product)

        session.commit()
        logger.debug(f"Adicionado product de nome: '{product.nome}'")
        return apresenta_product(product), 200

    except RuntimeError as runtimeError:
        error_msg = "produto de mesmo nome e recipiente já salvo na base :/"
        logger.warning(f"Erro ao adicionar product '{product.nome}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as error:
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar product '{product.nome}', {error_msg}")
        return {"message": error_msg}, 400


@app.get("/products")
@cross_origin()
def get_products():
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
)
@cross_origin()
def get_product(query: ProductBuscaSchema):
    product_id = query.id
    logger.debug(f"Coletando dados sobre product #{product_id}")
    session = Session()
    product = session.query(Product).filter(Product.id == product_id).first()

    if not product:
        error_msg = "product não encontrado na base :/"
        logger.warning(f"Erro ao buscar product '{product_id}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"product encontrado: '{product.nome}'")
        return apresenta_product(product), 200



@app.put(
    "/product/{product_id}",
)
@cross_origin()
def update_product(product_id: int, form: ProductSchema):
    try:
        session = Session()

        # Verificar se o produto existe no banco de dados
        existing_product = session.query(Product).filter_by(id=product_id).first()

        if existing_product is None:
            raise HTTPException(status_code=404, detail="Produto não encontrado")

        # Atualizar os atributos do produto com os dados do formulário
        existing_product.nome = form.nome
        existing_product.recipiente = form.recipiente
        existing_product.quantidade = form.quantidade
        existing_product.valor = form.valor

        session.commit()

        logger.debug(f"Produto de ID {product_id} atualizado com sucesso")
        return apresenta_product(existing_product), 200

    except HTTPException as httpException:
        return {"message": httpException.detail}, httpException.status_code

    except Exception as error:
        error_msg = "Não foi possível atualizar o produto :/"
        logger.warning(f"Erro ao atualizar produto de ID {product_id}, {error_msg}")
        return {"message": error_msg}, 400


@app.delete("/product/")
@cross_origin()
def del_product(query: ProductBuscaSchema):
    product_id = query.id
    logger.debug(f"Coletando dados sobre product #{product_id}")
    session = Session()
    product = session.query(Product).filter(Product.id == product_id).first()

    if product:
        logger.debug(f"Deletando dados sobre product #{product_id}")
        logger.debug(f"Deletado product #{product}")

        session.delete(product)
        session.commit()
        return {"message": "produto removido", "id": product_id}
    else:
        error_msg = "product não encontrado na base :/"
        logger.warning(f"Erro ao deletar product #'{product}', {error_msg}")
        return {"message": error_msg}, 404
