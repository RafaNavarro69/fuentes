import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory='straps')

app = FastAPI()

@app.get('/')
def pide(rpta: Request):
#    return templates.TemplateResponse('baseEco.html', {'request': rpta})
    return templates.TemplateResponse('eco03Strap.html', {'request': rpta})

@app. post('/salida')
def ensenya ():
    return 1

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)

