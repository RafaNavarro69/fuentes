import uvicorn
import requests as req
import xml.etree.ElementTree as xml
from fastapi.responses import Response
from fastapi import FastAPI
import base64
import cx_Oracle

app = FastAPI()

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
def ppal():
    try:
        pool=crearPool()
        if pool is not None:
            db_conn=conectarAlba(pool)

            cursor=db_conn.cursor()
            sql="""
                select C3, C10, C4, C5, C6,  C7, C8, C9, NIF, TOTAL, EXPEDIENTE, TOTALSIN, YA, LIQ 
                  from RNASEG25 where ya is null
                   """
            print (sql)
            cursor.execute(sql)            
            
            regs = cursor.fetchall()
            for r in regs:
                print (r[0])

                req_body="""
                        <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
                          <s:Body xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
                          <altaExpedienteTasas xmlns="http://www.sevilla.org/alba2WS-tasas">
                          <Exaccion>MANSEREMER</Exaccion>
                          <FechaAlta>02072025</FechaAlta>
                          <Nif>"""+r[8]+"""</Nif>
                          <NombreRazon>"""+r[1]+"""</NombreRazon>
                          <Observaciones>La cuota resulta del 5% de las primas recaudadas por los seguros de incendios, y/o del 2,5% de las primas recaudadas por los seguros multirriesgo</Observaciones>
                          <Registro>"""+r[0]+"""</Registro>
                          <DirObjeto>
                            <TipoVia>****</TipoVia>
                            <ViaDes>Mantenimiento de los servicios de emergencia que presta el Ayuntamiento de Sevilla</ViaDes>
                            <Numero> </Numero>
                            <CodPostal>41091</CodPostal>
                            <Poblacion>41091</Poblacion>
                            <Pais>108</Pais>
                            <ProvinciaDes>SEVILLA</ProvinciaDes>
                            <PoblacionDes>SEVILLA</PoblacionDes>
                            <PaisDes>ESPAÑA</PaisDes>
                          </DirObjeto>
                          <DirNotificacion>
                            <TipoVia>****</TipoVia>
                            <ViaDes>Ciudad de Sevilla</ViaDes>
                            <Numero> </Numero>
                            <CodPostal>41091</CodPostal>
                            <Poblacion>41091</Poblacion>
                            <Pais>108</Pais>
                            <ProvinciaDes>SEVILLA</ProvinciaDes>
                            <PoblacionDes>SEVILLA</PoblacionDes>
                            <PaisDes>ESPAÑA</PaisDes>
                          </DirNotificacion>
                          <Tarifa>
                            <Codigo>010201</Codigo>
                            <CantidadSpecified>true</CantidadSpecified>
                            <Cantidad>"""+str(r[9])+"""</Cantidad>
                          </Tarifa>
                        </altaExpedienteTasas>
                      </s:Body>
                    </s:Envelope>"""

                response = req.post  (
                                            url='http://192.168.52.172:8080/alba2WS-tasas/tasasServices/alba2WS-tasas',
                                            headers={"content-type": "text/xml; charset=utf-8"},
                                            data=req_body.encode("utf-8")
                                    )
                
                print (response.text)
                arbol=xml.fromstring(response.text)

                for child in arbol.iter('*'):
                    print ([e.tag for e in arbol.findall('.//'+child.tag)])

                for child in arbol.iter('{http://www.sevilla.org/alba2WS-tasas}Pdf'):
                  fic = open("c:\\Rafa\\Seguros\\" + r[0] + ".pdf", 'wb')
                  fic.write(base64.b64decode(child.text))
                  fic.close()

        cursor.close()

        desconectarAlba(pool, db_conn)

        return ("En C:\\Rafa\\Seguros")
   
    except:
        return ("Sin pdfs")  

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)

