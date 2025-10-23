from suds.client import Client
import base64
import uvicorn
from fastapi import FastAPI, Response, Request, Form
from fastapi.templating import Jinja2Templates

app = FastAPI()

@app.get('/')
def pideNombre(rpta: Request):
    templates = Jinja2Templates(directory='templates')
    return templates.TemplateResponse('PideLiquidacion.html', {'request': rpta})

@app.post('/salida')
def ppal(liq : str = Form()):

    consulta = Client('http://10.70.19.36:8080/alba2WS-tasas/tasasServices/alba2WS-tasas?wsdl')
    print (consulta)

    #liq=consulta.factory.create('string') 'No es un tipo a definir; es un string. No hay que hacer nada
    respuesta=consulta.service.impresionPago(liq)
    print (respuesta)

    return Response(content=base64.b64decode(respuesta.Pdf), media_type="application/pdf")


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)