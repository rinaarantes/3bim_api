# models.py criar tabeals e salva?
from sqlalchemy import Column, Integer, String, Float 
from database import Base 
  
class ProdutoDB(Base): 
    __tablename__ = 'produtos' 
  
    id = Column(Integer, primary_key=True, index=True) 
    nome = Column(String(100), nullable=False) 
    preco = Column(Float, nullable=False) 
    quantidade = Column(Integer, nullable=False)

    class livroDB(Base): 
       __tablename__ = 'livro' 
  
    livroId = Column(Integer, primary_key=True, index=True) 
    titulo = Column(String(255), nullable=False) 
    autor = Column(String(255), nullable=False)
    anoPublicacao  = Column(Integer, nullable=False)
    preco = Column(Decimal, nullable=False) 
   