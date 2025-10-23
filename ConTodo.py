from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from typing import Union, List

app = FastAPI()
templates = Jinja2Templates(directory='templates')

@app.get('/')
def pide(rpta: Request):
    return templates.TemplateResponse('ConTodo.html', {'request': rpta})

@app.post('/persona', response_class=HTMLResponse)
def da ( 
        nombre : str = Form(...), 
        lenguaje : str = Form(...), 
        estudios : str = Form(...), 
        Coc: Union[str, None] = Form(None),
        Dep: Union[str, None] = Form(None),
        Tv: Union[str, None] = Form(None),
        Mus: Union[str, None] = Form(None),
        docDeUpload : UploadFile = File(...),
        docs : List[UploadFile] = File(...)
       ):

    s=""
    for docum in docs:
        s=s + " " + docum.filename
    return f'{s} y {docDeUpload.filename} como currículum' 

    if Dep=="on": 
        return "Hola, deportista"
    else:    
        return f'<h1>Escribiste {nombre} {lenguaje}</h1>'

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)