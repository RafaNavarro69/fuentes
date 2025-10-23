from fastapi import FastAPI
from fastapi.responses import HTMLResponse,HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
import cx_Oracle
import requests

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


@app.get('/pp')
def pp():
     return ("Pasé por el pp de get")

@app.post('/')
def f1():
    pool=crearPool()

    if pool is not None:
        db_conn=conectarAlba(pool)

        try:    
            cursor=db_conn.cursor()
            
            cursor.execute("select sysdate from dual")
            regs = cursor.fetchall()
            for r in regs:
                s= f'Son las {r[0]}'

        except:
            return ('No pude encontrar datos')

        cursor.close()

        desconectarAlba(pool, db_conn)

        return s

@app.get('/', response_class=HTMLResponse)
def ppal():
        rpta=requests.post('http://localhost:5000')
        rpta2=requests.get('http://localhost:5000/pp')

        return(f'<h1>{rpta.text[1:len(rpta.text)-1]}</h1><h2>{rpta2.text[1:len(rpta2.text)-1]}</h2>')

        

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)