from fastapi import FastAPI 
app = FastAPI()
@app.get('/')
def raiz():
 return {'mensagem': 'Minha primeira API em FastAPI!'}

 @app.get('/')
def sobre():
 return {'mensagem': 'PÁGINA SOBRE O SITE'}