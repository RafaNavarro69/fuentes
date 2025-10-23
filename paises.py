from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory='templates')

@app.get('/')
def pide(rpta: Request):
    return templates.TemplateResponse('paises.html', {'request': rpta})

@app.post('/paises', response_class=HTMLResponse)
def da(pais: str = Form(...)):
    return f'<h1>Escribiste {pais}</h1>'

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)