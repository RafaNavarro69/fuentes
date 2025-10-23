from fastapi import FastAPI
from fastapi.responses import RedirectResponse, HTMLResponse
import uvicorn
import logging


app = FastAPI()

@app.get('/')
def ppal():
    try:
        logging.basicConfig(filename="C://Users//ranavang//Downloads//isbilya.log", level=logging.INFO, format='%(asctime)s %(message)s')
        logging.info("Voy a hacer un redirect response")

        return(RedirectResponse(url='/pp2'))
    except:
        logging.info("Error!!")
    

@app.get('/pp', response_class=HTMLResponse)
def pp():
        s2="""<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <title>Am I HTML already?</title>
        </head>
        <body>
        <h1>Hello, World Wide Web!</h1>
        <p>This is my first website.</p>

        <h2>About me</h2>
        <p>I'm a Python programmer and a bug collector.</p>

        <h3>Random facts</h3>
        <p>I don't just <em>like</em> emoji,<br>
        I <strong>love</strong> emoji!</p>
        <p>My most-used emoji are:</p>
        <ol>
            <li>🐞</li>
            <li>🐍</li>
            <li>👍</li>
        </ol>

        <h2>Links</h2>
        <p>My favorite websites are:</p>
        <ul>
            <li>realpython.com</li>
            <li>python.org</li>
            <li>pypi.org</li>
        </ul>
        </body>
        </html>"""

        return s2

        

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)