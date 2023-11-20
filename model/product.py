from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base, Comentario


class Product(Base):
    __tablename__ = 'product'

    id = Column("pk_product", Integer, primary_key=True)
    nome = Column(String(140))
    recipiente = Column(Float)
    quantidade = Column(Integer)
    valor = Column(Float)
    data_insercao = Column(DateTime, default=datetime.now())

    comentarios = relationship("Comentario")

    def __init__(self, nome:str, quantidade:int, valor:float, recipiente:float,
                 data_insercao:Union[DateTime, None] = None):
    
        self.nome = nome
        self.recipiente = recipiente
        self.quantidade = quantidade
        self.valor = valor

        # se não for informada, será a data exata da inserção no banco;
        if data_insercao:
            self.data_insercao = data_insercao

    def adiciona_comentario(self, comentario:Comentario):
       
        self.comentarios.append(comentario)

