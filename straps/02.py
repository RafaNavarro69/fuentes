import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader
from fastapi.responses import HTMLResponse


app = FastAPI()

@app.get('/')
def pide(rpta: Request):
    entorno = Environment(loader=FileSystemLoader('straps'))

    template = entorno.get_template('eco01Strap2.html')

    PideUnDatoRendered = template.render()

    print(PideUnDatoRendered)

#    return HTMLResponse(PideUnDatoRendered)

    templates = Jinja2Templates(directory='straps')
    return templates.TemplateResponse('eco01Strap2.html', {'request': rpta})


@app. post('/AceptaDatos')
def ensenya ():
    return 'En AceptaDatos'


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)

