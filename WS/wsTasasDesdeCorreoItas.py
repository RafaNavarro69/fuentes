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
      <FechaAlta>03102025</FechaAlta> 
      <FechaLimPago>18102025</FechaLimPago> 
      <Nif>00000001R</Nif> 
      <NombreRazon>FERNANDO</NombreRazon> 
      <Apellido1>HISPALENSE</Apellido1> 
      <Apellido2>SEVILLANO</Apellido2> 
      <Observaciones>PRUEBA - NO VALIDA Generado como prueba.</Observaciones> 
      <Registro>Reg. prueba</Registro> 
      <DirObjeto> 
        <TipoVia>CALLE</TipoVia> 
        <ViaDes>ABADES</ViaDes> 
        <Numero>0002</Numero> 
        <RestoDir>1-A</RestoDir> 
        <CodPostal>41003</CodPostal> 
        <Poblacion>41091</Poblacion> 
        <Pais>108</Pais> 
        <ProvinciaDes>SEVILLA</ProvinciaDes> 
        <PoblacionDes>SEVILLA</PoblacionDes> 
        <PaisDes>ESPAÑA</PaisDes> 
      </DirObjeto> 
      <DirNotificacion> 
        <TipoVia>CALLE</TipoVia> 
        <ViaDes>ABADES</ViaDes> 
        <Numero>0002</Numero> 
        <RestoDir>1-A</RestoDir> 
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
      <EXENCIONES> 
        <CONCEPTO>TALL65</CONCEPTO> 
      </EXENCIONES> 
          </altaExpedienteTasas> 
  </s:Body> 
</s:Envelope>  """

    response = req.post  (
                                url='http://10.70.26.48:8070/alba2WS-tasas/tasasServices/alba2WS-tasas',
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