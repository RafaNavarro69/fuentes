from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
import cx_Oracle

app = FastAPI()
templates = Jinja2Templates(directory='templates')

def crearPool():
    try:
        dsn_tns = cx_Oracle.makedsn("prealba11.ayuntamiento.svq", 1556, "prealb11") # ip, port, sid

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


@app.get('/', response_class=HTMLResponse)  # No me lo ponía en html hasta que no he puesto esto último !!!!!!!!!!!!!!!!!!!!!!!
def ppal():

    pool=crearPool()

    if pool is not None:
        db_conn=conectarAlba(pool)

        try:    
            cursor=db_conn.cursor()
            cursor.execute("""
                    begin
                        execute immediate
                                'alter session set nls_date_format = ''DD-MM-YYYY'' nls_language = SPANISH';
                    end;""")            
            
            cursor.execute("select sysdate from dual")
            regs = cursor.fetchall()
            for r in regs:
                s= f'<h1>Son las {r[0]}</h1>'
        except:
            return ('No pude encontrar datos')

        cursor.close()

        desconectarAlba(pool, db_conn)

        return (s)
        

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)