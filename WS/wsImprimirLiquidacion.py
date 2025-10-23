import uvicorn
import requests as req
import xml.etree.ElementTree as xml
from fastapi.responses import Response, HTMLResponse
from fastapi import FastAPI, Request, Form
import base64
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader
import os

templates = Jinja2Templates(directory='templates')

app = FastAPI()

@app.get('/')
def pide(rpta: Request):

    entorno = Environment(loader=FileSystemLoader('templates'))

    template = entorno.get_template('PideUnDato.html')

    contenido = {
                    'titulo': 'impresión de liquidación',
                    'peticion': 'Dame liquidación a imprimir',
                    'dato': 'liq'
                }

    PideUnDatoRendered = template.render(contenido)

    print(PideUnDatoRendered)

    fic = open('templates\\PideUnDatoRendered.html', 'w', encoding='utf-8')
    fic.write(PideUnDatoRendered)
    fic.close()

#    return templates.TemplateResponse('PideLiquidacion.html', {'request': rpta})
    return templates.TemplateResponse('PideUnDatoRendered.html', {'request': rpta})

@app.post('/salida')
def ppal(liq : str = Form()):
    try:
        if os.path.exists("templates\\PideUnDatoRendered.html"):
            os.remove("templates\\PideUnDatoRendered.html")

        req_body="""
                <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:alb="http://www.sevilla.org/alba2WS-tasas">
                <soapenv:Header/>
                <soapenv:Body>
                    <alb:ImpresionPago>
                        <alb:Liquidacion>""" + liq + """</alb:Liquidacion>
                    </alb:ImpresionPago>
                </soapenv:Body>
                </soapenv:Envelope>    
                """
        
        print (req_body)

        response = req.post (
                                    url='http://10.70.19.36:8080/alba2WS-tasas/tasasServices/alba2WS-tasas',
                                    headers={"content-type": "text/xml; charset=utf-8"},
                                    data=req_body.encode("utf-8")
                            )                            

        arbol=xml.fromstring(response.text)

        for child in arbol.iter('*'):
            print ([e.tag for e in arbol.findall('.//'+child.tag)])

        for child in arbol.iter('{http://www.sevilla.org/alba2WS-tasas}Pdf'):
            fic = open("c:\\Rafa\\" + liq + ".pdf", 'wb')
            fic.write(base64.b64decode(child.text))
            fic.close()

            return Response(content=base64.b64decode(child.text), media_type="application/pdf")

    except:
        return ("Sin pdf")  

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)