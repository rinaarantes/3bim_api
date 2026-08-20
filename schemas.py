# schemas.py diz qual e o formato de troca de dados
from pydantic import BaseModel 
  
class ProdutoBase(BaseModel): 
    nome: str 
    preco: float 
    quantidade: int 
  
class ProdutoCreate(ProdutoBase): 
    pass 
  
class ProdutoResponse(ProdutoBase): 
    id: int 
  
    class Config: 
        from_attributes = True

class livroBase(BaseModel): 
    titulo: str 
    autor: str 
    anoPublicacao: int 
    preco: float 
    
  
class livroCreate(livroBase): 
    pass 
  
class livroResponse(livroBase): 
    livroId: int 
  
    class Config: 
        from_attributes = True