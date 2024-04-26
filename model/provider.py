from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from  model import Base, Comentario


class Provider(Base):
    __tablename__ = 'provider'

    nome = Column(String(140))
    cnpj = Column("cnpj", String , primary_key=True)
    cep = Column(String)
    cidade = Column(String)
    uf = Column(String)

    # comentarios = relationship("Comentario")

    def __init__(self, nome:str, cnpj:str, cep:str, cidade:str, uf:str):
    
        self.nome = nome
        self.cnpj = cnpj
        self.cep = cep
        self.cidade = cidade
        self.uf = uf

    # def adiciona_comentario(self, comentario:Comentario):
       
    #     self.comentarios.append(comentario)

