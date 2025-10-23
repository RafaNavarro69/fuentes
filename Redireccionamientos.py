from fastapi import FastAPI, Form, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse, RedirectResponse
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory='templates')

@app.get('/')
def pide(rpta: Request):
    return templates.TemplateResponse('radio2.html', {'request': rpta})

@app.get('/1')
def ac1(): 
    return FileResponse(path="C:\Rafa\Manuales\Building Applications.pdf", media_type="application/pdf")

@app.get('/2')
def f2(): 
    return FileResponse(path="C:\Rafa\Manuales\Common Built ins.pdf", media_type="application/pdf")

@app.get('/3')
def f3(): 
    return FileResponse(path="C:\Rafa\Manuales\Common Mistakes At First Certificate Cambridge.pdf", media_type="application/pdf")

@app.post('/docs', response_class=HTMLResponse)
def da(fic : int = Form(...)):
    match fic:
        case 1:
             return(RedirectResponse(url='/1', status_code=status.HTTP_303_SEE_OTHER)) # Si no pongo el parámetro de status, me dice método no permitido
        case 2:
             return(RedirectResponse(url='/2', status_code=status.HTTP_303_SEE_OTHER))
        case 3:
             return(RedirectResponse(url='/3', status_code=status.HTTP_303_SEE_OTHER))
        case 4:
             surl = f"http://www.elpais.es"
             return(RedirectResponse(url=surl))


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)