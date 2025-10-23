from fastapi import FastAPI, Form
from typing import Annotated
import uvicorn
import autenticacion
import alba
import logging

app = FastAPI()
pool=alba.crearPool()

db_conn=alba.conectarAlba(pool)

logging.info("por aquí estoy")

print("ok")

liqid=2345345
s=f"select liqid from liquidaciones where liqid={liqid}"
cursor=db_conn.cursor()
cursor.execute(s)
registros = cursor.fetchall()
for r in registros:
    entrada=r[0]#liqid
cursor.close()

#desconectarAlba(db_conn)

@app.post("/login")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    
    if autenticacion.usuarioldap (username, password):
        return {"username": username}
    else:
        return {"error":"no existe"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)

