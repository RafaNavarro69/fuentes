from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from uuid import uuid4
import sqlalchemy
from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.orm import sessionmaker
from ldap3 import Server, Connection, ALL
from datetime import datetime, timedelta

def LDAP_AUTH(usuario, password):
    didConnect = False

    try:
        ldap_ip='10.70.17.180' 
        ldap_port=389
        ldap_root='ayuntamiento.svq'

        print (usuario + ' ' + password)

        serv = Server(host=f'ldap://{ldap_ip}', port=ldap_port, use_ssl=True, get_info=ALL)

        conn = Connection(serv, user=f'{usuario}@{ldap_root}', password=password, check_names=True, lazy=False, raise_exceptions=True)
        conn.open()
        conn.bind()

        print (conn.result)

        if conn.result['result'] == 0:
            didConnect = True
    except:
        didConnect = False

    conn.unbind()
    return didConnect

app = FastAPI()

templates = Jinja2Templates(directory="templates")

Base = sqlalchemy.orm.declarative_base()
engine = create_engine('sqlite:///:memory:', echo=True)
SesionLocal = sessionmaker(bind=engine)

# Define a Session model
class Sesion(Base):
    __tablename__ = 'sesion'
    id = Column(String(36), primary_key=True)
    usuario = Column(String, nullable=True)
    caducidad = Column(DateTime, nullable=True)

db = SesionLocal ()
    
def autorizacion (usuario, password, url):
    if LDAP_AUTH(usuario, password):
#        app.mount("/templates", StaticFiles(directory="templates"), name="static")

        Base.metadata.create_all(engine)

        # Generate a unique session ID
        sesion_id = str(uuid4())
        caducidad=datetime.now() + timedelta(minutes=1)
        
#        db = SesionLocal ()
        # Store the session information in the database with the correct username
        sesion = Sesion(id=sesion_id, usuario=usuario, caducidad=caducidad)
        db.add(sesion)
        db.commit()
        db.close()
        print('added:', sesion_id, usuario)

        response = RedirectResponse(url=url)
        response.set_cookie(key='sesion_id', value=sesion_id)
        response.set_cookie(key='usuario', value=usuario)

        return response
    else:
        return None


def peticionAcceso (galleta):
    sesion_id = galleta.cookies.get('sesion_id')
    usuario = galleta.cookies.get('usuario')
    print ('En peticionAcceso con ' + usuario)

    if sesion_id and usuario:
#        Base.metadata.create_all(engine)

#        db = SesionLocal ()

        print(Sesion.caducidad)

        sesion = db.query(Sesion).filter
        (
            Sesion.id == sesion_id,
            Sesion.usuario == usuario,
            Sesion.caducidad > datetime.now()
        )

        db.close()
    else:
       sesion = None     

    print ('Sesión: ' )
    print (sesion)
    return sesion
    

