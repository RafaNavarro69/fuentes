# -*- coding: utf-8 -*-
import logging
import cx_Oracle

rootDir = '/mnt/fd/system/000-tmp-cache/'
rutaLog = '/mnt/fd/system/000-tmp-log/'

try:

	logging.basicConfig(filename=rutaLog+"tera.log", level=logging.INFO, format='%(asctime)s %(message)s')

except:

	rootDir = 'C://Users//ranavang//Downloads//'
	rutaLog = 'C://Users//ranavang//Downloads//'
	logging.basicConfig(filename=rutaLog+"isbilya.log", level=logging.INFO, format='%(asctime)s %(message)s')


def crearPool():
    try:
        ip = "proalba11.ayuntamiento.svq"
        port = 1556
        sid = "proalb11"
        usuario =  "alba"
        password = "proalb11"
        dsn_tns = cx_Oracle.makedsn(ip, port, sid)
        pool = cx_Oracle.SessionPool(user=usuario, password=password, dsn=dsn_tns,min=2, max=100, increment=1, threaded=True, encoding="UTF-8")

        return pool
    except:
        return None


def conectarAlba(pool):

	db_conn = pool.acquire(purity=cx_Oracle.ATTR_PURITY_NEW)

	return db_conn

def desconectarAlba(db_conn):

	pool.release(db_conn)


pool=crearPool()

if pool is not None:
    db_conn=conectarAlba(pool)
    print("ok")

    liqid=2345345
    s=f"select liqnumerorecliquidacion, liqxestado from liquidaciones where liqid={liqid}"
    cursor=db_conn.cursor()
    cursor.execute(s)
    registros = cursor.fetchall()
    for r in registros:
        entrada=r[1]
        print (entrada)
    cursor.close()

    desconectarAlba(db_conn)
