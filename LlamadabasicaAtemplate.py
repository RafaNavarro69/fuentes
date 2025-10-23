from fastapi import FastAPI
from jinja2 import Environment, FileSystemLoader
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def raiz():

    entorno = Environment(loader=FileSystemLoader('templates'))

    template = entorno.get_template('temp01.html')

    contenido = {
                    'title': 'Aquí el titulito que quiera',
                    'heading': 'Bienvenido!',
                    'message': 'Hola Mundo, soy Rafa!'
                }

    rendered_html = template.render(contenido)

    return (rendered_html)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)