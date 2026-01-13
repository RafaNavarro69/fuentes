import uvicorn
import requests as req
import xml.etree.ElementTree as xml
from fastapi.responses import Response
from fastapi import FastAPI
import base64

app = FastAPI()

@app.get('/')
def ppal():
   try:

    #Quitar el header de lo que traigho de ITAS------------------------------------    
    req_body="""
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
  <s:Body xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
<altaExpedienteTasas xmlns="http://www.sevilla.org/alba2WS-tasas"> 
      <Exaccion>TALLERES</Exaccion> 
      <FechaAlta>29102025</FechaAlta> 
      <Nif>28698447J</Nif> 
      <NombreRazon>MANUEL JESUS</NombreRazon> 
      <Apellido1>GALLARDO</Apellido1> 
      <Apellido2>BARCO</Apellido2> 
      <Observaciones>Inscripción de MANUEL JESUS GALLARDO BARCO en el taller 109 SEVILLANAS (TARDES MARTES Y JUEVES) del
distrito Casco Antiguo (1) 
. Esta liquidación deberá ser abonada antes de la matriculación en el taller.</Observaciones> 
      <Registro>CASCO ANTIGUO#109-SEVILLANAS (TARDES MARTES Y JUEVES)</Registro> 
      <DirObjeto> 
        <TipoVia>CALLE</TipoVia> 
        <ViaDes>MURO DE LOS NAVARROS</ViaDes> 
        <Numero>0038</Numero> 
        <RestoDir>BAJO PUERTA 3</RestoDir> 
        <CodPostal>41003</CodPostal> 
        <Poblacion>41091</Poblacion> 
        <Pais>108</Pais> 
        <ProvinciaDes>SEVILLA</ProvinciaDes> 
        <PoblacionDes>SEVILLA</PoblacionDes> 
        <PaisDes>ESPAÑA</PaisDes> 
      </DirObjeto> 
      <DirNotificacion> 
        <TipoVia>CALLE</TipoVia> 
        <ViaDes>MURO DE LOS NAVARROS</ViaDes> 
        <Numero>0038</Numero> 
        <RestoDir>BAJO PUERTA 3</RestoDir> 
        <CodPostal>41003</CodPostal> 
        <Poblacion>41091</Poblacion> 
        <Pais>108</Pais> 
        <ProvinciaDes>SEVILLA</ProvinciaDes> 
        <PoblacionDes>SEVILLA</PoblacionDes> 
        <PaisDes>ESPAÑA</PaisDes> 
      </DirNotificacion> 
      <Tarifa> 
        <Codigo>010101</Codigo> 
      </Tarifa> 
    </altaExpedienteTasas> 
  </s:Body> 
</s:Envelope> 
"""

    response = req.post  (
                                url='http://10.70.26.36:8080/alba2WS-tasas/tasasServices/alba2WS-tasas',
                                headers={"content-type": "text/xml; charset=utf-8"},
                                data=req_body.encode("utf-8")
                         )
    
    print (response.text)
    arbol=xml.fromstring(response.text)

    for child in arbol.iter('*'):
        print ([e.tag for e in arbol.findall('.//'+child.tag)])

    for child in arbol.iter('{http://www.sevilla.org/alba2WS-tasas}Pdf'):
        fic = open("c:\Rafa\ej11.pdf", 'wb')
        fic.write(base64.b64decode(child.text))
        fic.close()

        return Response(content=base64.b64decode(child.text), media_type="application/pdf")
   
   except:
        return ("Sin pdf")  

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)