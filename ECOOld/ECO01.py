from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from typing import Union, List
import cx_Oracle
from datetime import datetime

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
    return templates.TemplateResponse('eco01.html', {'request': rpta})

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
            s=f"select * from ecorecursos_tmp"
            cursor.execute(s)
            registros = cursor.fetchall()
            s = f"Nig/Número de procedimiento<br>"

            for r in registros:
                print (r)
                nig=r[0]
                num_procedimiento=r[2]
                s = f"{s}{nig}/{num_procedimiento}<br>"

        except:
            cursor.close()
            desconectarAlba(pool, db_conn)

    cursor.close()
    desconectarAlba(pool, db_conn)

    return ('<h2>'+s+'</h2>'+atras)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)