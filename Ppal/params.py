from fastapi import FastAPI, Query
from typing import List
import uvicorn
from fastapi.responses import RedirectResponse

app = FastAPI()

@app.get('/')
def pide():
    return (RedirectResponse (url='/items?q=thethner&q=hgfd&a=1&a=2'))

@app.get("/items")
def read_items(q: List = Query(...), a:str=Query(...)):
    print(q)
    query_items = {"eltos": q}
    print(query_items)
    print(q)
    print(a)  #Nota que sólo se ha qwuedado con la última
    return query_items

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)