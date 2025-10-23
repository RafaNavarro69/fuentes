from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
import uvicorn
import requests as req
from fastapi.responses import HTMLResponse
import xml.etree.ElementTree as xml

app = FastAPI()
templates = Jinja2Templates(directory='templates')

@app.get('/')
def pide(rpta: Request, ):
    return templates.TemplateResponse('Exaccion.html', {'request': rpta})

@app.post('/accion', response_class=HTMLResponse)
def daNombre(exac: str = Form(...)):

    url = 'http://10.70.19.47:8080/alba2WS-tasas/tasasServices/alba2WS-tasas'

    req_headers = {"content-type": "text/xml"}
    f = open("xml\\ws02.xml",'rt')

    req_body = f.read()
    f.close()

    req_body = req_body.replace("&exac", exac.upper())

    print (req_body)

    response = req.post  (
                                url,
                                data=req_body,
                                headers=req_headers
                         )
    
    arbol=xml.fromstring(response.text) 
   
   # return response.text  'No escrib elo mismo si response_class=HTMLResponse en post'

    s=""
    for child in arbol.iter('{http://www.sevilla.org/alba2WS-tasas}Descripcion'):
        print (child.text)
        s = s + child.text + '<br>'

    return ('<h4>' + s + '</h4>')


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)