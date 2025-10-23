from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory='templates')

@app.get('/')
def pide(rpta: Request):
    return templates.TemplateResponse('radio.html', {'request': rpta})

@app.post('/respuesta', response_class=HTMLResponse)
def da(nombre : str = Form(...), estudios : str = Form(...)):
    return f'<h1>{nombre}, tus estudios son {estudios}</h1>'

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)