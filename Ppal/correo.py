from fastapi import FastAPI, Request,Query, Form
from starlette.responses import JSONResponse, HTMLResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
from typing import List
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import uvicorn

class EmailSchema(BaseModel):
    email: List[EmailStr]

conf = ConnectionConfig(
    MAIL_USERNAME = "rnavarroa@sevilla.org",
    MAIL_PASSWORD = "Hiniesta_&05",
    MAIL_FROM = "rnavarroa@sevilla.org",
    MAIL_PORT = 25,
    MAIL_SERVER = "smtp.sevilla.org",
    MAIL_FROM_NAME="rnavarroa@sevilla.org",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

app = FastAPI()
templates = Jinja2Templates(directory='templates')

@app.get('/1')
def pide():
    return (RedirectResponse (url='/email?emails=rnavarroa@sevilla.org&emails=rafa@isbilia.es'))

@app.get('/2')
def pide(rpta: Request):
    return templates.TemplateResponse('listaCorreos.html', {'request': rpta})

@app.get("/email")
async def simple_send(emails: List = Query(...)):
    print (emails)

    message = MessageSchema(
        subject="Probando",
        recipients=emails,
        body= """<p>Ahí va la primera prueba</p> """,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "Correo enviado"})

@app.post("/email2")
async def simple_send(emails: str = Form(...), asunto : str= Form(...), cuerpo : str= Form(...)):
    print (emails)

    message = MessageSchema(
        subject=asunto,
        recipients=emails.split(','),
        body= cuerpo,
        subtype=MessageType.plain)

    fm = FastMail(conf)
    await fm.send_message(message)
    return HTMLResponse("<h3>Correo enviado</h3>")


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)