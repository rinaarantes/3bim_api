# main.py 

from fastapi import FastAPI, Depends 
from sqlalchemy.orm import Session 
from database import Base, engine, get_db 
from models import ProdutoDB 
from models import livroDB 
from schemas import ProdutoCreate, ProdutoResponse 
from models import LivroDB
from schemas import LivroCreate, LivroResponse
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware

#falta um textin aq pra funcionar esse app



  
Base.metadata.create_all(bind=engine)  # cria as tabelas, se ainda não existirem 
  
app = FastAPI() 

app.add_middleware(
 CORSMiddleware,
 allow_origins=['*'],
 # em produção, restringir para o domínio real do front-end
 allow_methods=['*'],
 allow_headers=['*'],
)

  
Base.metadata.create_all(bind=engine)  # cria as tabelas, se ainda não existirem 
  
app = FastAPI() 
  
@app.get('/produtos/{produto_id}', response_model=ProdutoResponse)
def obter_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(ProdutoDB).filter(ProdutoDB.id == produto_id).first()
    if produto is None:
        raise HTTPException(status_code=404, detail='Produto não encontrado')
    return produto

# LIVROS 

# GET -> retorna um único livro pelo id
@app.get('/livros/{livro_id}', response_model=LivroResponse)
def obter_livro(livro_id: int, db: Session = Depends(get_db)):
    livro = db.query(LivroDB).filter(LivroDB.id == livro_id).first()
    if livro is None:
        raise HTTPException(status_code=404, detail='Livro não encontrado')
        return livro

# DELETE -> remove 
@app.delete('/livros/{livro_id}', status_code=204)
def remover_livro(livro_id: int, db: Session = Depends(get_db)):
    livro = db.query(LivroDB).filter(LivroDB.id == livro_id).first()
    if livro is None:
        raise HTTPException(status_code=404, detail='Livro não encontrado')
        db.delete(livro)
        db.commit()

# PUT -> atualiza 
@app.put('/livros/{livro_id}', response_model=LivroResponse)
def atualizar_livro(livro_id: int, dados: LivroCreate, db:
Session = Depends(get_db)):
    livro = db.query(LivroDB).filter(LivroDB.id == livro_id).first()
    if livro is None:
        raise HTTPException(status_code=404, detail='Livro não encontrado')
        livro.nome = dados.nome
        livro.preco = dados.preco
        livro.quantidade = dados.quantidade
        db.commit()
        db.refresh(livro)
        return livro

@app.get('/livros', response_model=list[LivroResponse])
def listar_livros(db: Session = Depends(get_db)):
    return db.query(LivroDB).all()

@app.post('/livros', response_model=LivroResponse, status_code=201)
def criar_livro(livro: LivroCreate, db: Session = Depends(get_db)):
    novo_livro = LivroDB(**livro.dict())
    db.add(novo_livro)
    db.commit()
    db.refresh(novo_livro)
    return novo_livro