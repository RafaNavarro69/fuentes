from fastapi import FastAPI
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
from typing import List
from fastapi.responses import Response
import uvicorn
from openpyxl import Workbook


class EmailSchema(BaseModel):
    email: List[EmailStr]

conf = ConnectionConfig(
    MAIL_USERNAME = "rnavarroa@sevilla.org",
    MAIL_PASSWORD = "Hiniesta_&05",
    MAIL_FROM = "rnavarroa@sevilla.org",
    MAIL_PORT = 25,
    MAIL_SERVER = "smtp.sevilla.org",
    MAIL_FROM_NAME="Rafa",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)


app = FastAPI()

@app.get('/')
async def pide():


    wb = Workbook()
    ws = wb.active
    ws['A1'] = 42
    ws.append([1, 2, 3])
    wb.save("ejemplo.xlsx")

    emails=['rafa@isbilia.es']

    fm = FastMail(conf)

    message = MessageSchema(
        subject="Probando",
        recipients=emails,
        body= "Hola",
        attachments=["ejemplo.xlsx"],
        subtype=MessageType.plain)

    print(fm.config)

    await fm.send_message(message)

    return Response("Correo Enviado")
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=4000)