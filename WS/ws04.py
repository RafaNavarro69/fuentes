import uvicorn
import requests as req
import xml.etree.ElementTree as xml
from fastapi.responses import HTMLResponse
from fastapi import FastAPI

app = FastAPI()

@app.get('/', response_class=HTMLResponse)
def ppal():

    txt = """
            <xml>
                <libro>
                    <title>Uno</title><data>aaaaaaaaaaaaaaaaaaaa</data>        
                </libro>
                <libro>
                    <title>Dos</title><data>bbbbbbbbbbbbbbbbbbbbb</data>        
                </libro>
                <libro>
                    <title>tres</title><data>ccccccccccccccccccc</data>        
                </libro>
                <libro>
                    <title>Cuatro</title><data>dddddddddddddddddddd</data>        
                </libro>
            </xml>
          """            

    arbol=xml.fromstring(txt)

    print ("-------------")
    for child in arbol.iter('*'):
        print ([e.text for e in arbol.findall('.//'+child.tag)])
    print ("-------------")

    rtdo = [e.text for e in arbol.findall('.//data')]
    print(rtdo)

    for ch in arbol.findall('.//data'):
        print (ch.text)

    print ("===")
    for child in arbol.findall('.//libro/data'):
            print (child.text)

    print ("=======")
    for child in arbol.findall('.//libro'):
        titulo=child.find('title')
        datos=child.find('data')
        print (titulo.text, datos.text)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)