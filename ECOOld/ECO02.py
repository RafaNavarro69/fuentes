from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader
import uvicorn
import cx_Oracle


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

@app.get('/', response_class=HTMLResponse)
async def ensena (): 
    pool=crearPool()
    
    if pool is not None:
        db_conn=conectarAlba(pool)
        cursor=db_conn.cursor()

        try:   
            entorno = Environment(loader=FileSystemLoader('templates'))

            template = entorno.get_template('tempECO02.html')

            s=f"select * from ecorecursos_tmp"
            cursor.execute(s)
            registros = cursor.fetchall()

            recursos = [] 

            for r in registros:            
                recurso = {
                            'nig':r[0],
                            'num_procedimiento':r[2]
                          }  

                recursos.append(recurso)

            contenido={"recursos" : recursos}
            
            html = template.render(contenido)

            print (html)
        except:
            cursor.close()
            desconectarAlba(pool, db_conn)

    
    cursor.close()
    desconectarAlba(pool, db_conn)

    return (html)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)