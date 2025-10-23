from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory='templates')

@app.get('/')
def pide(rpta: Request):
    return templates.TemplateResponse('radio2.html', {'request': rpta})

@app.post('/docs', response_class=HTMLResponse)
def da(fic : int = Form(...)):
    match fic:
        case 1:
            return FileResponse(path="C:\Rafa\Manuales\Building Applications.pdf", media_type="application/pdf")
        case 2:
            return FileResponse(path="C:\Rafa\Manuales\Common Built ins.pdf", media_type="application/pdf")
        case 3:
            return FileResponse(path="C:\Rafa\Manuales\Common Mistakes At First Certificate Cambridge.pdf", media_type="application/pdf")
        case 4:
            return FileResponse(path="C:\Rafa\Manuales\Forms to the Web.pdf", media_type="application/pdf")


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)