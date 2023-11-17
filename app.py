from flask_openapi3 import OpenAPI, Info, Tag
from flask import Flask, request, jsonify, redirect
from urllib.parse import unquote
import sqlite3

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


@app.get("/")
@cross_origin()
def home():
    return redirect("/openapi")


@app.post(
    "/product",
)
@cross_origin()
def add_product():
    data = request.get_json()
    if not data:
        return {"message": "Dados JSON ausentes no corpo da solicitação."}, 400

    product = Product(
        nome=data.get("nome"),
        recipiente=data.get("recipiente"),
        quantidade=data.get("quantidade"),
        valor=data.get("valor"),
    )
    logger.debug(f"Adicionando product de nome: '{product.nome}'")
    try:
        session = Session()

        session.add(product)

        session.commit()
        logger.debug(f"Adicionado product de nome: '{product.nome}'")
        return apresenta_product(product), 200

    except IntegrityError as e:
        error_msg = "product de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar product '{product.nome}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
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
    return jsonify(products_json)


@app.get(
    "/product",
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
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"product encontrado: '{product.nome}'")
        return apresenta_product(product), 200

@app.put("/product/<int:product_id>")
@cross_origin()
def update_product(product_id):
    session = Session()

    product = session.query(Product).filter(Product.id == product_id).first()

    if not product:
        error_msg = "Produto não encontrado na base :/"
        logger.warning(f"Erro ao buscar produto '{product_id}', {error_msg}")
        return {"message": error_msg}, 404

    data = request.get_json()

    if not data:
        return {"message": "Dados JSON ausentes no corpo da solicitação."}, 400

    # Atualizar os atributos do produto com os dados fornecidos no JSON
    product.nome = data.get("nome", product.nome)
    product.recipiente = data.get("recipiente", product.recipiente)
    product.quantidade = data.get("quantidade", product.quantidade)
    product.valor = data.get("valor", product.valor)

    try:
        session.commit()
        logger.debug(f"Produto atualizado: '{product.nome}'")
        return apresenta_product(product), 200

    except Exception as e:
        error_msg = "Não foi possível atualizar o produto :/"
        logger.warning(f"Erro ao atualizar produto '{product.nome}', {error_msg}")
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
