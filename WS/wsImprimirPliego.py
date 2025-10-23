import uvicorn
import requests as req
import xml.etree.ElementTree as xml
from fastapi import FastAPI, Request, Form
import base64
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader
import os
import cx_Oracle
from typing import Union

app = FastAPI()

templates = Jinja2Templates(directory='templates')

def crearPool():
    try:
        dsn_tns = cx_Oracle.makedsn("proalba11.ayuntamiento.svq", 1556, "proalb11") # ip, port, sid

#        pool = cx_Oracle.SessionPool(user="alba", password="proalb11", dsn=dsn_tns,min=2, max=100, increment=1, threaded=True, encoding="UTF-8")
        pool = cx_Oracle.SessionPool(user="depuracion", password="depuracion", dsn=dsn_tns,min=2, max=100, increment=1, threaded=True, encoding="UTF-8")

        return pool
    except:
        return None

def conectarAlba(pool):
	db_conn = pool.acquire(purity=cx_Oracle.ATTR_PURITY_NEW)
	return db_conn

def desconectarAlba(pool, db_conn):
    pool.release(db_conn)


@app.get('/')
def pide(rpta: Request):

    entorno = Environment(loader=FileSystemLoader('templates'))

    template = entorno.get_template('PideUnDato.html')

    contenido = {
                    'titulo': 'Impresión de pliego completo de feria',
                    'peticion': 'Dame pliego a imprimir: ',
                    'dato': 'pliego',
                    'otroDato' : "<br><br>Cuántas liquidaciones imprimo? <input type='text' name='cuantas' size='3' maxlength='3'><br><br>"
                }

    PideUnDatoRendered = template.render(contenido)

    fic = open('templates\\PideUnDatoRendered.html', 'w', encoding='utf-8')
    fic.write(PideUnDatoRendered)
    fic.close()

    return templates.TemplateResponse('PideUnDatoRendered.html', {'request': rpta})

@app.post('/salida')
def ppal(pliego : str = Form(), cuantas : Union[str, None] = Form(None)):
    try:
        if os.path.exists("templates\\PideUnDatoRendered.html"):
            os.remove("templates\\PideUnDatoRendered.html")

        if cuantas=="": cuantas=5
        if cuantas=="999": cuantas=99999999

        pool=crearPool()
        if pool is not None:
            db_conn=conectarAlba(pool)

            cursor=db_conn.cursor()
            sql="""
                select liqnumerorecliquidacion, dni_exp(l.expid, 'SUJETOPASIVO') info 
                  from albaadm.pliegosfacturas p, albaadm.detallepliegosfras d, albaadm.liquidaciones l
                 where pyfnumcargo='""" + pliego + """' and pyftipodocu='P' and pyfsubtipo='P'
                   and p.pyfid=d.pyfid 
                   and d.liqid=l.liqid
                   and rownum<="""  + str(cuantas)
            sql="select liq,c3 from RNASEG25"
            print (sql)
            cursor.execute(sql)            
            
            regs = cursor.fetchall()
            for r in regs:
                liq=r[0]    
                print (liq)

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
                response = req.post  (
                                            url='http://10.70.19.36:8080/alba2WS-tasas/tasasServices/alba2WS-tasas',
                                            headers={"content-type": "text/xml; charset=utf-8"},
                                            data=req_body.encode("utf-8")
                                        )

                print (response.text)
                arbol=xml.fromstring(response.text)

                for child in arbol.iter('{http://www.sevilla.org/alba2WS-tasas}Pdf'):
                    fic = open("c:\\Rafa\\Seguros\\" + r[1] + ".pdf", 'wb')
                    fic.write(base64.b64decode(child.text))
                    fic.close()

            cursor.close()

            desconectarAlba(pool, db_conn)

            return ("En C:\\Rafa\\Seguros")

    except:
        return ("Hubo error")  

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)