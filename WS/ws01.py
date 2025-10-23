from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
import uvicorn
import requests as req
import xml.etree.ElementTree as xml

app = FastAPI()
templates = Jinja2Templates(directory='templates')

@app.get('/')
def pideNombre(rpta: Request):
    return templates.TemplateResponse('nombre.html', {'request': rpta})

@app.post('/accion')
def daNombre(nombre: str = Form(...)):

    url = 'http://10.70.19.47:8080/alba2WS-tasas/ATSE/ATSE_WS'

    req_headers = {"content-type": "text/xml"}
    req_body  = "<soap:Envelope xmlns:soap='http://schemas.xmlsoap.org/soap/envelope/' xmlns:atse='http://www.sevilla.org/ATSE_WS'>"
    req_body += "<soap:Header></soap:Header>"
    req_body += "<soap:Body>"
    req_body += "<atse:TitularDeRefCatastral>"
    req_body += "<atse:refCat>6220001TG3462S0331AD</atse:refCat>"
    req_body += "<atse:nif>28905503T</atse:nif>"
    req_body += "</atse:TitularDeRefCatastral>"
    req_body += "</soap:Body>"
    req_body += "</soap:Envelope>"

    response = req.post  (
                                url,
                                data=req_body,
                                headers=req_headers
                         )
    
#    return f'{response.text}'  Así veo todo lo que devuelve


    print (response.content)

    arbol=xml.fromstring(response.text) #igual si response.content
    
    for child in arbol.iter('{http://www.sevilla.org/ATSE_WS}Descripcion'):
        print(child.tag, child.text)


    txt = "<xml>            <title>Info</title>            <foo>aldfj</foo>            <data>Text I want to count</data>        </xml>"
    arbol=xml.fromstring(txt)

    for child in arbol.iter('*'):
        print(child.tag, child.text)


    arbol  = xml.parse("xml\\ws01.xml")
    
    for child in arbol.iter('{http://www.sevilla.org/alba2WS-tasas}codExaccion'):
        print(child.tag)
        print(child.text)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)