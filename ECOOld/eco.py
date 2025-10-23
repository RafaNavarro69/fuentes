from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
import uvicorn
from typing import Union, List
import cx_Oracle
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
import base64

app = FastAPI()

templates = Jinja2Templates(directory='templates')

atras = "<br><button onclick='history.back();'>Atrás</button>"

def crearPool():
    try:
        dsn_tns = cx_Oracle.makedsn("proalba11.ayuntamiento.svq", 1556, "proalb11") # ip, port, sid

#        pool = cx_Oracle.SessionPool(user="alba", password="prealb11", dsn=dsn_tns,min=2, max=100, increment=1, threaded=True, encoding="UTF-8")
        pool = cx_Oracle.SessionPool(user="depuracion", password="depuracion", dsn=dsn_tns,min=2, max=100, increment=1, threaded=True, encoding="UTF-8")

        return pool
    except:
        return None

def conectarAlba(pool):
	db_conn = pool.acquire(purity=cx_Oracle.ATTR_PURITY_NEW)
	return db_conn

def desconectarAlba(pool, db_conn):
    pool.release(db_conn)


@app.get('/pideDatos')
def pide(rpta: Request):
    return templates.TemplateResponse('ecoPide.html', {'request': rpta})

@app.post('/AceptaDatos', response_class=HTMLResponse)
async def da ( 
               nig : Union[str, None] = Form(None),
               nif : Union[str, None] = Form(None),
           numproc : Union[str, None] = Form(None), 
          anyoproc : Union[str, None] = Form(None), 
           juzgado : Union[str, None] = Form(None),
         negociado : Union[str, None] = Form(None),
          tipoproc : str = Form(),
               gin : Union[str, None] = Form(None),
                san: Union[str, None] = Form(None),
                ajm: Union[str, None] = Form(None),
                tea: Union[str, None] = Form(None),
                gpr: Union[str, None] = Form(None),
                rec: Union[str, None] = Form(None),
            fvista : Union[str, None] = Form(None), 
          observac : Union[str, None] = Form(None),
              docs : List[UploadFile] = File(...)
            ):

    dep=""
    if gin=="on": 
        dep = dep + ",gin"
    if san=="on": 
        dep = dep + ",san"
    if ajm=="on": 
        dep = dep + ",ajm"
    if tea=="on": 
        dep = dep + ",ajm"
    if gpr=="on": 
        dep = dep + ",gpr"
    if rec=="on": 
        dep = dep + ",rec"
        
    if len(dep)>0:
        dep=dep[2:] 


    factual = datetime.now().strftime('%Y-%m-%d')
    fact = datetime.now().strftime('%d-%m-%y')

    pool=crearPool()

    if pool is not None:
        db_conn=conectarAlba(pool)
        cursor=db_conn.cursor()

        try:   
            fechavista = datetime.strptime(fvista, '%Y-%m-%d').date()
        
            s=f"select perid from personas where periden='{nif}'"
            cursor.execute(s)
            registros = cursor.fetchall()
            for r in registros:
                perid=r[0]

            print ('Nif '+ nif)

            s=f"""INSERT INTO ECORECURSOS_TMP (
                    AÑO_PROCEDIMIENTO, CESTADO, DEPARTAMENTO, 
                    ESTADO, FHORAMOD, FVISTA, 
                    NEGOCIADO, NIG, NUM_JUZGADO, 
                    NUM_PROCEDIMIENTO, OBSERVACIONES, PERID, 
                    TIPO_PROCEDIMIENTO, USUIDMOD) 
                VALUES (
                    '{anyoproc}',
                    '1',
                    '{dep}',
                    'Recibido',
                    to_date('{factual}','yyyy-mm-dd'),
                    to_date('{fechavista}','yyyy-mm-dd'),
                    '{negociado}',
                    '{nig}',
                    '{juzgado}',
                    '{numproc}',
                    '{observac}',
                     {perid},
                    '{tipoproc}',
                    0)"""
            print (s)
            cursor.execute(s)
            
            i=0
            fact = datetime.now().strftime('%d-%m-%y')
            
            print (fact)
            for docum in docs:
                i=i+1    
                datos = await docum.read()

                cursor.execute("INSERT INTO ECODOCUMENTOS_TMP (AÑO_ENTRADA, BDOC, NIG, NUM_ENTRADA, PROCEDENCIA, TIPO_DOC, FDOC, NOM_DOC) VALUES (:anyo, :bl, :nig, :nume, :proc, :tipo, :fec, :nomdoc)", 
                anyo='2024', bl=datos, nig=nig, nume=i, proc='PR', tipo='I', fec=fact, nomdoc=docum.filename)

                salida="Insertado el nig" + nig
                db_conn.commit() 
        except:
                db_conn.rollback() 
                salida="Hubo errores. Inténtalo de nuevo"

    cursor.close()
    desconectarAlba(pool, db_conn)
    
    return (salida + atras)

@app.post('/EnsenaDatos', response_class=HTMLResponse)
async def ensena (): 

    pool=crearPool()
    
    if pool is not None:
        db_conn=conectarAlba(pool)
        cursor=db_conn.cursor()

        try:   
            entorno = Environment(loader=FileSystemLoader('templates'))

            template = entorno.get_template('ecoMuestra.html')

            s=f"select * from ecorecursos_tmp"
            cursor.execute(s)
            registros = cursor.fetchall()

            recursos = [] 

            for r in registros:   
                print (r)    
                s=f"select periden nif, nvl(perrazon,pernombre||' '|| perapell1||' '||perapell2) nom from personas where perid={r[1]}"
                cursor.execute(s)
                reg = cursor.fetchone()
                print (reg)
                nif=reg[0]
                nom=reg[1]

                s=f"select nom_doc from ecodocumentos_tmp where nig='{r[0]}'"
                cursor.execute(s)
                reg2 = cursor.fetchall()

                docs=[]

                for r2 in reg2:
                    docto = {
                            'nomdoc':r2[0]
                            }

                    docs.append(docto)

                docs = {'documentos':docs}

                recurso = {
                            'nif':nif,
                            'nom':nom,
                            'nig':r[0],
                            'numpr':r[2],
                            'docs':docs
                          }  

                recursos.append(recurso)

            contenido={"recursos" : recursos}

            html = template.render(contenido)

#            print (html)
        except:
            cursor.close()
            desconectarAlba(pool, db_conn)

    
    cursor.close()
    desconectarAlba(pool, db_conn)

    return (html + atras)

@app.get('/MuestraDoc/{documento}/{nig}')
def muestra (documento:str,nig:str):
    pool=crearPool()
    
    if pool is not None:
    
        try:   
            db_conn=conectarAlba(pool)
            cursor=db_conn.cursor()
            s=f"select bdoc from ecodocumentos_tmp where nig='{nig}' and nom_doc='{documento}'"
            print (s)
            cursor.execute(s)
            reg = cursor.fetchone()
            archivo=reg[0].read()
        except:
            cursor.close()
            desconectarAlba(pool, db_conn)
    
    cursor.close()
    desconectarAlba(pool, db_conn)
                
    match documento[-3:].upper():
       case 'XML':
        return Response(content=archivo, media_type="application/xml")
       case 'PDF':
        return Response(content=archivo, media_type="application/pdf")
       case 'PNG':
        return Response(content=archivo, media_type="image/png ")
       case 'JPG':
        return Response(content=archivo, media_type="image/jpeg")
       case 'JPEG':
        return Response(content=archivo, media_type="image/jpeg")
       case 'GIF':
        return Response(content=archivo, media_type="application/gif")
       case 'ZIP':
        return Response(content=archivo, media_type="application/zip")
       case 'XLS':
        return Response(content=archivo, media_type="application/vnd.ms-excel")
       case 'TXT':
        return Response(content=archivo, media_type="text/html")
#        return HTMLResponse("<h1>"+base64.b64decode(archivo).encode()+"/h1>")    
       case _:
            return HTMLResponse("<h1>Extensión no contemplada</h1>"+atras)    


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)