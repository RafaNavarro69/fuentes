import os
import uvicorn

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import File, UploadFile
from typing import List

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def health():
    return {"message": "Hello World!"}


@app.get("/upload", response_class=HTMLResponse)
async def upload_page(request: Request):

    return templates.TemplateResponse("fichero.html", {"request": request})

@app.post("/upload")
def upload(files: List[UploadFile] = File(...)):
    for file in files:
        try:
            contents = file.file.read()
            with open(file.filename, 'wb') as f:
                f.write(contents)
        except Exception:
            return {"message": "There was an error uploading the file(s)"}
        finally:
            file.file.close()

    return {"message": "Successfully uploaded"}  



if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)

