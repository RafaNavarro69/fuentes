import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()

@app.get("/documentacion")
def main():
    return FileResponse(path="C:\Rafa\Manuales\Building Applications.pdf", filename="Ejemplo.pdf", media_type="application/pdf")

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=1111)