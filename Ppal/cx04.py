from fastapi import FastAPI, Form, Request, status
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory='templates')

@app.get('/')
def pide(rpta: Request):
    return templates.TemplateResponse('radio3.html', {'request': rpta})


@app.post('/respuesta')
def da(nombre : str = Form(...), estudios : str = Form(...)):

        if nombre=="Rafael" or nombre=="Isabel":
              return(RedirectResponse(url=f'/nombre/{nombre}', status_code=status.HTTP_303_SEE_OTHER)) #Completamente necesario el return, si no sigue para adelante en el código y termina haciendo el sgte return que encuentra
        
        if nombre=="Paco":
               return(RedirectResponse(url='/postnoensenya', status_code=status.HTTP_303_SEE_OTHER))  #Llama a post y no lo reconoce

        s=f'/p{estudios}/{nombre}'
        return(RedirectResponse(url=s, status_code=status.HTTP_303_SEE_OTHER))

@app.get('/p1/{nom}')
def p1(nom):
        return (f'Pinchaste p1, {nom}')

@app.get('/p2/{nom}')
def p2(nom):
        return ("Pinchaste p2")

@app.get('/nombre/{nom}', response_class=HTMLResponse)
def p3(nom):
        return (f'<h1>Hola, {nom}')

@app.post('/postnoensenya', response_class=HTMLResponse)
def p4():
        return ("Mira a barra y no verás querystring")

        

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)