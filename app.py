from flask_openapi3 import OpenAPI, Info, Tag
from flask import Flask, request, jsonify, redirect
from urllib.parse import unquote
import sqlite3

from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from model import Session, Product
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = Flask(__name__, info=info)
CORS(app)

# Configuração do CORS
cors = CORS(app, resources={r"/products/*": {"origins": "http://localhost:4200"}})

# Configuração do banco de dados SQLite
db_name = "exemplo.db"

# Cria a tabela se ela não existir
def create_table():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL,
            concluida BOOLEAN NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# home_tag = Tag(
#     name="Documentação",
#     description="Seleção de documentação: Swagger, Redoc ou RapiDoc",
# )
# product_tag = Tag(
#     name="Product", description="Adição, visualização e remoção de products à base"
# )


@app.get("/", tags=[home_tag])
def home():
    return redirect("/openapi")


@app.post(
    "/product",
    tags=[product_tag],
    responses={"200": ProductViewSchema, "409": ErrorSchema, "400": ErrorSchema},
)
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


# @app.get(
#     "/products",
#     tags=[product_tag],
#     responses={"200": ListagemProductsSchema, "404": ErrorSchema},
# )
# def get_products():
#     logger.debug(f"Coletando products ")
#     session = Session()
#     products = session.query(Product).all()

#     products = [...]
    
#     products_representation = apresenta_products(products)
    
#     return jsonify({"products": products_representation})
    # if not products:
    #     return [], 200
    # else:
    #     logger.debug(f"%d products encontrados" % len(products))
    #     return apresenta_products(products), 200

# @app.get('/products')
# def get_products():
#     logger.debug(f"Coletando produtos ")
#     session = Session()
#     products = session.query(Product).all()

#     if not products:
#         return {"produtos": []}, 200
#     else:
#         logger.debug(f"%d rodutos econtrados" % len(products))
#         print(products)
#         return products, 200

# @app.get('/products', )
# def get_products():
#     logger.debug(f"Coletando produtos ")
#     session = Session()
#     products = session.query(Product).all()

#     if not products:
#         return JSONResponse(content=[], status_code=200)
#     else:
#         logger.debug(f"%d produtos encontrados" % len(products))
#         return JSONResponse(content=apresenta_products(products), status_code=200)


# @app.route("/products", tags=[product_tag],
#    responses={"200": ListagemProductsSchema, "404": ErrorSchema})

# def get_products():
#     products= [{ "nome": p[0], "recipiente": p[1], "quantidade": p[2], "valor": p[3]} for p in products ] 
#     products_array = [products]
#     return jsonify(products_array)

# if __name__ == '__main__':
#     app.run(debug=True)

@app.route('/tarefas', methods=['GET'])
def get_products():
    create_table()
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    tarefas = cursor.fetchall()
    conn.close()
    tarefas_json = [{ "nome": p[0], "recipiente": p[1], "quantidade": p[2], "valor": p[3]} for p in products]
    return jsonify(tarefas_json)



@app.get(
    "/product",
    tags=[product_tag],
    responses={"200": ProductViewSchema, "404": ErrorSchema},
)
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


@app.delete(
    "/product",
    tags=[product_tag],
    responses={"200": ProductDelSchema, "404": ErrorSchema},
)
def del_product(query: ProductBuscaSchema):
    product_nome = unquote(unquote(query.nome))
    print(product_nome)
    logger.debug(f"Deletando dados sobre product #{product_nome}")
    session = Session()
    count = session.query(Product).filter(Product.nome == product_nome).delete()
    session.commit()

    if count:
        logger.debug(f"Deletado product #{product_nome}")
        return {"mesage": "product removido", "id": product_nome}
    else:
        error_msg = "product não encontrado na base :/"
        logger.warning(f"Erro ao deletar product #'{product_nome}', {error_msg}")
        return {"mesage": error_msg}, 404
