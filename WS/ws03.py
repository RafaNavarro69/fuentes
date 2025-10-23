import uvicorn
import requests as req
import xml.etree.ElementTree as xml
from fastapi.responses import HTMLResponse
from fastapi import FastAPI

app = FastAPI()

@app.get('/', response_class=HTMLResponse)
def ppal():

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

    xm = "http://www.sevilla.org/ICIO_WS"
    xm1 = "{"+xm+"}"
    url = 'http://192.168.52.172:8080/alba2WS-tasas/ICIO/ICIO_WS'

    req_headers = {"content-type": "text/xml"}
    req_body = "<soapenv:Envelope xmlns:soapenv='http://schemas.xmlsoap.org/soap/envelope/' xmlns:icio='" + xm + "'>"
    req_body = req_body + """
                        <soapenv:Header/>
                        <soapenv:Body>
                            <icio:ExisteExpedienteICIO>
                                <icio:NumLicencia>000200052624</icio:NumLicencia>
                                <icio:NumDocumento>1111</icio:NumDocumento>
                            </icio:ExisteExpedienteICIO>
                        </soapenv:Body>
                    </soapenv:Envelope>
               """

    response = req.post  (
                                url,
                                data=req_body,
                                headers=req_headers
                         )
    
    print (response.content)

    arbol=xml.fromstring(response.text) #igual si response.content
    
    for child in arbol.iter('*'):
        print (child.tag, child.text)

    nodo=f".//{xm1}Descripcion"   # Atento al ppio ---------------
    print (nodo)

    rtdo = [e.text for e in arbol.findall(nodo)]
    print(rtdo)

    for ch in arbol.findall(nodo):
        print (ch.text)

    s=""
    ensenya=False
    for child in arbol.iter('*'):
        if child.tag==f"{xm1}Resultado":
            if child.text=="1":
                ensenya=True
            else:    
                ensenya=False
        elif ensenya and child.tag==f"{xm1}Descripcion":
            s=f'{s}{child.text}'


    return f'<h2>{s}</h2>'

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)