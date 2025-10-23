from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory='templates')
app.add_middleware(SessionMiddleware, secret_key="your_secret_key")

@app.get('/')
def pide(rpta: Request):
    return templates.TemplateResponse('sesion.html', {'request': rpta})

@app.get("/set_session/")
async def set_session(request: Request):
    request.session["user_id"] = "12345"
    return {"message": "Session data set!"}

@app.get("/get_session/")
async def get_session(request: Request):
    user_id = request.session.get("user_id", "Not set")
    return {"user_id": user_id}



if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)