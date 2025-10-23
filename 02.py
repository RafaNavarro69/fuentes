# Llamada de un endpint a otro

import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def raiz():
     return ("<h1>Hola mundo, soy yo, sí!</h1>")


@app.get("/items/{elto}")
def masqueraiz(elto):
    return ("Introdujiste " + str(elto))

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)