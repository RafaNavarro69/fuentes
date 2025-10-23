from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory='templates')

@app.get('/')
def pideNombre(rpta: Request):
    return templates.TemplateResponse('nombre.html', {'request': rpta})

@app.post('/accion', response_class=HTMLResponse)
def daNombre(nombre: str = Form(...)):
    return f'<h1>Escribiste {nombre}</h1>'


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)