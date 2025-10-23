from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse, Response
from fastapi.templating import Jinja2Templates
from typing import Union, List
import uvicorn
import base64, io
import cx_Oracle
from pathlib import Path


app = FastAPI()
templates = Jinja2Templates(directory='templates')

def crearPool():
    try:
        dsn_tns = cx_Oracle.makedsn("prealba11.ayuntamiento.svq", 1556, "prealb11") # ip, port, sid
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
    return templates.TemplateResponse('ConTodo.html', {'request': rpta})

@app.post('/persona', response_class=HTMLResponse)
async def ppal ( 
        nombre : str = Form(...), 
        lenguaje : str = Form(...), 
        Dep: Union[str, None] = Form(None),
        docDeUpload : UploadFile = File(...)
       ):
    

    pool=crearPool()

    if pool is not None:
        db_conn=conectarAlba(pool)
        cursor=db_conn.cursor() 

        if Dep=="on": 
            depor = "S"
        else:    
            depor = "N"

        #return base64.b64decode(codecs.encode("SGVsbG8sIHdvcmxkIQ=="))  Esto devuelve hello world!


        file_path = f"C:\\Rafa\\Cosas\\def.jpg"
        rv = open(file_path,'rb').read()

        cursor.execute("insert into rnadatos values (:nomb, :leng, :dep, :nombreDoc, :blobdata)",
        nomb=nombre, leng=lenguaje, dep=depor, nombreDoc='def.jpg', blobdata=rv)


        datos = await docDeUpload.read()
        
        cursor.execute("insert into rnadatos values (:nomb, :leng, :dep, :nombreDoc, :blobdata)",
        nomb='Kk', leng=lenguaje, dep=depor, nombreDoc=docDeUpload.filename[:25], blobdata=datos)

        db_conn.commit()

        cursor.execute("select doc from rnadatos where nombre='Paco'")
        reg = cursor.fetchone()
        imageBlob = reg[0]
        blob= imageBlob.read()

        cursor.close()

        desconectarAlba(pool, db_conn)


        file_path = f"C:\\Rafa\\Cosas\\copiaDe{docDeUpload.filename}"
        with open(file_path, "wb") as f:
            f.write(docDeUpload.file.read())
    #        return "Guardado!"                  # Me devolvía  File at path Guardado! does not exist. Y era porque esperaba un fileresponse


        return Response(content=blob, media_type="image/jpeg")  # Funciona así


    else:    
        return "Sin acceso"

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)

