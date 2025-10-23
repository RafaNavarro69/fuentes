from fastapi import FastAPI, Request, Cookie
from fastapi.responses import  RedirectResponse
from typing import Optional
import uvicorn

app = FastAPI()

@app.get("/login")
async def login(request:Request):
     response = RedirectResponse(url="/main", status_code=302)
     response.set_cookie(key="cookie",value="key-value")
     return response

@app.get("/main")
async def root(request:Request, cookie: Optional[str] = Cookie(None)):
     if cookie:
        answer = "set to %s" % cookie
     else:
          answer = "not set"

     return {"value": answer}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)