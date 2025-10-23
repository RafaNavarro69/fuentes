from datetime import datetime, timedelta, date
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
import uvicorn
import time
import cx_Oracle

app = FastAPI()

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



def ppal():

    pool=crearPool()

    factual = datetime.now().strftime('%Y-%m-%d')

    if pool is not None:
        db_conn=conectarAlba(pool)
        print("Conexion a Oracle establecida exitosamente")
        print(factual)
        time.sleep(10)
        print("ok2")
        desconectarAlba(pool, db_conn)
        print("fin")


ppal()
