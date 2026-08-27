# main.py 

from fastapi import FastAPI, Depends 
from sqlalchemy.orm import Session 
from database import Base, engine, get_db 
from models import ProdutoDB 
from models import LivroDB # tem q ter exatamente o mesmo nome no models.py
from schemas import ProdutoCreate, ProdutoResponse 
from schemas import LivroCreate, LivroResponse
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI() 

app.add_middleware(
 CORSMiddleware,
 allow_origins=['*'],
 # em produção, restringir para o domínio real do front-end
 allow_methods=['*'],
 allow_headers=['*'],
)

  

app = FastAPI() 
@app.on_event("startup")
def criar_tabelas():
    Base.metadata.create_all(bind=engine)

  
def buscar_produto(db: Session, produto_id: int):
    return db.query(ProdutoDB).filter(ProdutoDB.id == produto_id).first()

@app.get('/produtos', response_model=list[ProdutoResponse])
def listar_produtos(db: Session = Depends(get_db)):
    return db.query(ProdutoDB).all()

@app.post('/produtos', response_model=ProdutoResponse, status_code=201)
def criar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    novo_produto = ProdutoDB(**produto.dict())
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    return novo_produto

@app.get('/produtos/{produto_id}', response_model=ProdutoResponse)
def obter_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = buscar_produto(db, produto_id)
    if produto is None:
        raise HTTPException(status_code=404, detail='Produto não encontrado')
    return produto

@app.put('/produtos/{produto_id}', response_model=ProdutoResponse)
def atualizar_produto(produto_id: int, dados: ProdutoCreate, db: Session = Depends(get_db)):
    produto = buscar_produto(db, produto_id)
    if produto is None:
        raise HTTPException(status_code=404, detail='Produto não encontrado')
    produto.nome = dados.nome
    produto.preco = dados.preco
    produto.quantidade = dados.quantidade
    db.commit()
    db.refresh(produto)
    return produto

@app.delete('/produtos/{produto_id}', status_code=204)
def remover_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = buscar_produto(db, produto_id)
    if produto is None:
        raise HTTPException(status_code=404, detail='Produto não encontrado')
    db.delete(produto)
    db.commit()

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