from fastapi import FastAPI, Form, Request
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



@app.get('/')
def pide(rpta: Request):
    return templates.TemplateResponse('matricula.html', {'request': rpta})

@app.post('/respuesta', response_class=HTMLResponse)
def ppal(mat : str = Form(...)):

    pool=crearPool()

    if pool is not None:
        db_conn=conectarAlba(pool)
        per="Sin dueño"
        try:    
            s=f"select dni_exp(expid, 'SUJETOPASIVO') NIF, nombre_exp(expid, 'SUJETOPASIVO') NOMBRE  from vehiculos_d where vehmatri='{mat}'"
            cursor=db_conn.cursor()
            cursor.execute(s)
            registros = cursor.fetchall()
            for r in registros:
                per=r[0]
                s = f'<h1>El dueño de la matrícula {mat} es {r[1]}</h1>'

        except:
            return ('No pude encontrar datos')

        s2="""Insert into PERSONAS
                (PERID, PERVERSION, TPEID, FIAID, PERUNICO, 
                PERNOMBRE, PERPART1, PERAPELL1, PERPART2, PERAPELL2, 
                PERRAZON, PERANAGRAMA, PERNOMVAL, PERIDEN, PERIDENEXT, 
                PERXTIPOIDEN, PERIDENVAL, PERXORIGEN, PERFHORAMOD, USUIDMOD, 
                PERMOTIVO, PERFVIGENCIA, PERMIGRAPERIDEN, PERMIGRAPERAPELNOMCORTO, TCOID, 
                PERFALLIDO, PERORIGENDEP, PERCATEGORIA, PERXSEXO, PERVALIDADA, 
                RDIID_FIS, PERFFALLECIDO, PERFFALLIDO, PERFACREEDORES, PERTDOMI, 
                RDIID_PAD, PERESTFALLECIDO)
                Values
                (PERSONAS_sq.nextval, 1, 2, 5, '1', 
                'ADRIANA', NULL, 'A DE SAAVEDRA', NULL, 'LOPEZ', 
                NULL, NULL, NULL, '28471900Q', NULL, 
                144, 'S', 3630, TO_DATE('08/01/2025 14:35:24', 'DD/MM/YYYY HH24:MI:SS'), 117242, 
                'Carga Direcciones Padrón', NULL, '28471900Q', 'A DE SAAVEDRA LOPEZ ADRIANA', NULL, 
                'N', 'P', 'P', 12531, NULL, 
                NULL, NULL, NULL, NULL, NULL, 
                27278718, NULL)"""

#        s3="Insert into depuracion.rnapeticiones values('" + mat + "','" + r[0] + "')" También vale
#        s3=f'Insert into depuracion.rnapeticiones values (\'{mat}\',\'{per}\')'

#        cursor.execute(s3)
#        cursor.close()

        db_conn.commit() # se podría db_conn.autocommit = True
#        db_conn.rollback()

        desconectarAlba(pool, db_conn)

        return (s)
        

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)