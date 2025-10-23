import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI()

@app.get("/")
def raiz():
    return(RedirectResponse(url='/items/pepe'))

@app.get("/items/{elto}", response_class=HTMLResponse)
def masqueraiz(elto):
    return ("<h1>Hola " + str(elto) + "!</h1>")

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)

