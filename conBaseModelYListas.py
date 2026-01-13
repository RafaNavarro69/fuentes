import json


class Direccion (BaseModel):
    Via: str | None = None
    TipoVia: str | None = None
    ViaDes: str 
    Numero: str | None = None
    Km: str | None = None
    Escalera: str | None = None
    Bloque: str | None = None
    Portal: str | None = None
    Planta: str | None = None
    Puerta: str | None = None
    RestoDir: str | None = None
    CodPostal: str | None = None
    Poblacion: str | None = None
    Pais: str | None = None
    ProvinciaDes: str | None = None
    PoblacionDes: str | None = None
    PaisDes: str | None = None

class Tarifa (BaseModel):
    Codigo: str
    Tarifa: float | None = None


class SP(BaseModel):
    nif: str
    nombre_razon: str
    apellido1: str | None = None
    apellido2: str | None = None


class Expediente(BaseModel):
    Exaccion : str 
    FechaAlta : date | None = None
    SujPasivo : SP
    DirObj : Direccion 
    DirNot : Direccion | None = None
    Observaciones : str | None = None
    Tarifa : Tarifa
    CodExencion : str | None = None
    CodBonif : str | None = None




def llamadaUrbanismo():

    usu='urbanismo'
    contra=json.loads(open('varglob_pre.json').read())['users_db']['urbanismo']['password']

    expdte="""
    {
      "Exaccion": "OCTEDIUS",
      "FechaAlta": "2025-11-26",
      "SujPasivo": {
        "nif": "28905503T",
        "nombre_razon": "Rafael",
        "apellido1": "Navarro",
        "apellido2": "Angel"
      },
      "DirObj": {
        "Via": "A",
        "TipoVia": "string",
        "ViaDes": "San Eloy",
        "Numero": "2",
        "Km": "string",
        "Escalera": "string",
        "Bloque": "string",
        "Portal": "8",
        "Planta": "2",
        "Puerta": "28",
        "RestoDir": "string",
        "CodPostal": "41011",
        "Poblacion": "Sevilla",
        "Pais": "string",
        "ProvinciaDes": "string",
        "PoblacionDes": "Sevilla",
        "PaisDes": "string"
      },
      "DirNot": {
        "Via": "Sierpes",
        "TipoVia": "Calle",
        "ViaDes": "Sierpes",
        "Numero": "72",
        "Km": "string",
        "Escalera": "string",
        "Bloque": "string",
        "Portal": "83",
        "Planta": "6",
        "RestoDir": "string",
        "CodPostal": "string",
        "Poblacion": "string",
        "Pais": "string",
        "ProvinciaDes": "string",
        "PoblacionDes": "Sevilla",
        "PaisDes": "string"
      },
      "Observaciones": "string",
      "Tarifa": {
        "Codigo": "120101",
        "Tarifa": 0
      }
    }"""


    
    exp=(Expediente)   #Definirlo como tipo clase
    exp.Exaccion = "OCTEDIUS"
    exp.FechaAlta = "2025-11-26"
    
    sj=(SP)
    sj.nif = "28905503T"
    sj.nombre_razon = "Rafael"
    sj.apellido1 = "Navarro"
    sj.apellido2 = "Suarez"
    exp.SujPasivo=sj

    dirobj=(Direccion)
    dirobj.TipoVia= "string"
    dirobj.ViaDes= "San Eloy"
    dirobj.Numero= "2"
    dirobj.Portal= "8"
    dirobj.Planta= "2"
    dirobj.Puerta= "28"
    dirobj.CodPostal= "41011"
    dirobj.Poblacion= "Sevilla"
    dirobj.PoblacionDes= "Sevilla"
    exp.DirObj=dirobj

    dirnot=dirobj
    exp.DirNot=dirnot

    tar=(Tarifa)
    tar.Codigo="120101"
    exp.Tarifa=tar

    print(exp.model_dump_json())


#########
    exp2={}
    exp2['Exaccion'] = "OCTEDIUS"
    exp2['FechaAlta'] = "2025-11-26"
    
    sj={}
    sj['nif'] = "28905503T"
    sj['nombre_razon'] = "Rafael"
    sj['apellido1'] = "Navarro"
    sj['apellido2'] = "Suarez"
    exp2['SujPasivo']=sj

    dirobj={}
    dirobj['TipoVia']= "string"
    dirobj['ViaDes']= "San Eloy"
    dirobj['Numero']= "2"
    dirobj['Portal']= "8"
    dirobj['Planta']= "2"
    dirobj['Puerta']= "28"
    dirobj['CodPostal']= "41011"
    dirobj['Poblacion']= "Sevilla"
    dirobj['PoblacionDes']= "Sevilla"
    exp2['DirObj']=dirobj

    dirnot=dirobj
    exp2['DirNot']=dirnot

    tar={}
    tar['Codigo']="120101"
    exp2['Tarifa']=tar


    access_token=None

# Un for si voy a llamarlo varias veces. Reupero el access-token sólo la primera vez

    headers_items = {
      'accept': 'application/json',
      'Content-type': 'application/json',
      'Authorization': 'Bearer ' + access_token
      }  


    
    """    response = requests.post(api_url + "altaexpedienteUrb", headers=headers_items, json=json.loads(expdte))
    print('---------------')
    print(response.json()); 
    print(response.json()['expediente'])
    print (response.json()['mensaje'])

    response = requests.post(api_url + "altaexpedienteUrb", headers=headers_items, json=exp2)
    print('---------------')
    print(response.json()); 
  """

    """    response = requests.post(api_url + "altaexpedienteUrb", headers=headers_items, json=exp.toJSON())
    print('---------------')
    print(response.json()); 
    print(response.json()['expediente'])
    print (response.json()['mensaje'])
"""



#########################

#    print(json.dumps({1:1, 2:2, 3:3}))  #Serializar convierte un string en un json


from pydantic import RootModel, BaseModel

"""
listaper = RootModel[list[cl.SP]]
personas = listaper(
    [
        cl.SP(
            nif='28147396L',
            nombre_razon='Rafael',
            apellido2='Suarez'
        ),
        cl.SP(
            nif='28905503T',
            nombre_razon='Rafael',
            apellido1='Navarro'
        ),
        cl.SP(
            nif='28325025L',
            nombre_razon='Angeles',
            apellido1='Angel',
            apellido2='Gordillo'
        )
    ]
)


print('-----')
print(personas.model_dump_json(indent=1))  #Probar con distintos indents o nada
class User(BaseModel):
    id: int
    name: str
    age: int
    dept: str


user = User(id=1, name="Test user", age = 12, dept="Information Technology")
print(user.model_dump_json())
print ('---------')


EsquemaDeClase = cl.Expediente.model_json_schema()  
print(json.dumps(EsquemaDeClase))
from pydantic import BaseModel, TypeAdapter
print ('---------')
ta = TypeAdapter(exp)
expi=ta.json_schema()
print(json.dumps(expi))
"""


exp=(Expediente)   #Definirlo como tipo clase
exp.Exaccion = "OCTEDIUS"
exp.FechaAlta = "2025-11-26"

sj=(SP)
sj.nif = "28905503T"
sj.nombre_razon = "Rafael"
sj.apellido1 = "Navarro"
sj.apellido2 = "Suarez"
exp.SujPasivo=sj

dirobj=(Direccion)
dirobj.ViaDes= "San Eloy"
dirobj.Numero= "2"
dirobj.Portal= "8"
dirobj.Planta= "2"
dirobj.Puerta= "28"
dirobj.CodPostal= "41011"
dirobj.Poblacion= "Sevilla"
dirobj.PoblacionDes= "Sevilla"
exp.DirObj=dirobj

dirnot=dirobj
exp.DirNot=dirnot

tar=(Tarifa)
tar.Codigo="120101"
exp.Tarifa=tar

#print (exp.to_dict())



class Modelo(BaseModel):
    x: str

m = Modelo(x='1')
js=m.model_dump_json()
j=m.model_dump()
print(j)
#print(js.json()['x']) 

m =Expediente(exp)
js=m.model_dump()
#print(m.model_dump_json())

#js=jsoniza(exp)
#print (json.loads(js.replace("'",'"')))


api_url = "http://teraws.ayuntamiento.svq:5000/"
#llamadaUrbanismo()






from pydantic import RootModel, BaseModel

"""
listaper = RootModel[list[cl.SP]]
personas = listaper(
    [
        cl.SP(
            nif='28147396L',
            nombre_razon='Rafael',
            apellido2='Suarez'
        ),
        cl.SP(
            nif='28905503T',
            nombre_razon='Rafael',
            apellido1='Navarro'
        ),
        cl.SP(
            nif='28325025L',
            nombre_razon='Angeles',
            apellido1='Angel',
            apellido2='Gordillo'
        )
    ]
)


print('-----')
print(personas.model_dump_json(indent=1))  #Probar con distintos indents o nada
class User(BaseModel):
    id: int
    name: str
    age: int
    dept: str


user = User(id=1, name="Test user", age = 12, dept="Information Technology")
print(user.model_dump_json())
print ('---------')


EsquemaDeClase = cl.Expediente.model_json_schema()  
print(json.dumps(EsquemaDeClase))
from pydantic import BaseModel, TypeAdapter
print ('---------')
ta = TypeAdapter(exp)
expi=ta.json_schema()
print(json.dumps(expi))
"""



exp=(Expediente)   #Definirlo como tipo clase
exp.Exaccion = "OCTEDIUS";exp.FechaAlta = "2025-11-26"

sj=(SP)
sj.nif = "28905503T";sj.nombre_razon = "Rafael";sj.apellido1 = "Navarro";sj.apellido2 = "Suarez";exp.SujPasivo=sj

dirobj=(Direccion)
dirobj.ViaDes= "San Eloy";dirobj.Numero= "2";dirobj.Portal= "8";dirobj.Planta= "2";dirobj.Puerta= "28";dirobj.CodPostal= "41011";dirobj.Poblacion= "Sevilla";dirobj.PoblacionDes= "Sevilla"
exp.DirObj=dirobj

dirnot=dirobj;exp.DirNot=dirnot

tar=(Tarifa)
tar.Codigo="120101"
exp.Tarifa=tar

"""for i in cl.Expediente.model_fields.keys():
  print (i)
  if i=='DirObj':
    for a in cl.Direccion.model_fields.keys():
      print (a)
  if i=='DirNot':
    for a in cl.Direccion.model_fields.keys():
      print (a)
  if i=='SujPasivo':
    for a in cl.Persona.model_fields.keys():
      print (a)
"""


for i in exp.model_fields.keys():
  print (i,' ',  type(i))
  if i=='DirObj':
    print('----',type(i))
    for a in dirobj.model_fields.keys():
      print (a,  type(i))
  if i=='DirNot':
    for a in clases.Direccion.model_fields.keys():
      print (a,  type(i))
  if i=='SujPasivo':
    for a in clases.Persona.model_fields.keys():
      print (a,  type(i))
  if i=='Tarifa':
    for a in clases.Tarifa.model_fields.keys():
      print (a,  type(i))

print ('1----------------------------')


for i in exp.model_fields.items():
  print (i,' ',  type(i))

print ('2----------------------------')

for i in exp.model_fields.values():
  print (i.annotation)

print ('3----------------------------')


for i in exp.model_fields:
  print (i.title())

print ('4----------------------------')
for i in dirobj.model_construct():
  print (i)


"""
for i in exp.model_construct():
  print (i)
for i in tar.model_construct():
  print (i)
for i in dirnot.model_construct():
  print (i)
"""
"""  if not isinstance(type(i), (int, float, str, list, tuple, dict)):
    for a in i.model_fields.keys():
      if not isinstance(i, (int, float, str, list, tuple, dict)):
        print (a,  type(i))
"""






print ('3----------------------------')


for i in exp.model_fields:
  print (i.title(), i.format())


for i in exp.model_fields.items():
  print (i, i.__class__, i.__format__.__class__)



print ('1----------------------------')


for i in exp.model_fields.items():
  s=str(i)
  desde=2
  hasta=s[desde+1:].find("'")
  CampoNombre=s[desde:hasta+3]
  desde=s.find("=")
  hasta=s[desde+1:].find(",")
  CampoTipo=s[desde+1:desde+hasta+1]
  if CampoTipo.find('Union[')==0:
    CampoTipo=CampoTipo[6:]
#  print (i,'---',CampoNombre, '----', CampoTipo)
  print (CampoNombre, '----', CampoTipo)
  if not CampoTipo in ('str','int','date'):
    print ('Otro')



print ('2----------------------------')

for i in exp.model_fields.values():
  print (type(i.annotation))
  if str(type(i.annotation))=="<class 'types.UnionType'>":
    print ('union')  
#  print (str(i.annotation), type(i.annotation))
#  if str(i.annotation)=="<class 'clases.SP'>":
#    for p in i.annotation.model_fields.values():
#      print ('    '+str(p.annotation))


print ('2----------------------------')


k=0
for i in exp.model_fields:
  k=k+1
  print (i, k)
  l=0
  if i=='DirObj' or i=='Tarifa' or i=='SujPasivo':
    for j in exp.model_fields.values():
        print (j.annotation)


print ('fin----------------------------')


k=0
for i in exp.model_fields:
  k=k+1
  print (i, k)
  l=0
  if i=='DirObj' or i=='Tarifa' or i=='SujPasivo':
    for j in exp.model_fields.values():
      l=l+1
      if l==k:
        print (j.annotation)
        for elto in j.annotation.model_fields:
          print ('   ', elto)
    
      

print ('2----------------------------')

import clases


k=0
for i in exp.model_fields:
  k=k+1
  print (i, k)
  l=0
  if i=='DirObj' or i=='DirNot' or i=='Tarifa' or i=='SujPasivo':
    for j in exp.model_fields.values():
      l=l+1
      if l==k:
        vcv=j.annotation
        print (vcv)
        if i=='DirObj':
          jan=vcv
        if i=='DirNot':
          vcv=jan
          
        for elto in vcv.model_fields:
          print ('   ', elto)
    

k=0
for i in exp.model_fields:
  k=k+1
  print (i, k)
  l=0
  if i=='DirObj' or i=='DirNot' or i=='Tarifa' or i=='SujPasivo':
    for j in exp.model_fields.values():
      l=l+1
      if l==k:
        vcv=j.annotation
        print (vcv)
        if i=='DirObj':
          jan=vcv
        if i=='DirNot':
          vcv=jan
          
        for elto in vcv.model_fields:
          print ('   ', elto)


print ('-----------')

lista=[]
for j in exp.model_fields.values():
      lista.append([str(j.annotation),j.annotation])

#print (lista)    
#print (lista[1])    
#print (lista[1][1])    


for i in range(len(lista)):
  print (lista[i][0], lista[i][1])
  if lista[i][0]=="<class 'clases.Direccion'>": 
    clase=lista[i][1]

print (clase)


print ('....')

lista2=[]
for j in exp.model_fields.values():
   if str(j.annotation).find("<class 'clases.")==0:
     lista2.append([str(j.annotation),j.annotation])


for i in range(len(lista2)):
  print (lista2[i][0], '   ', lista2[i][1])

print (lista2)



"""
print (type(clases.Direccion))

for r in cl.Direccion.model_construct():
  print (r)
"""

k=0
for i in exp.model_fields:
  k=k+1
  print (i, k)
  l=0
  if i=='DirObj' or i=='DirNot' or i=='Tarifa' or i=='SujPasivo':
    for j in exp.model_fields.values():
      l=l+1
      if l==k:
        vcv=j.annotation
        print (vcv)
        if i=='DirObj':
          jan=vcv
        if i=='DirNot':
          vcv=jan
          
        for elto in vcv.model_fields:
          print ('   ', elto)

print ('llllll')

print (lista2)

print ('llsssfsf')

k=0
for i in exp.model_fields:
  k=k+1; l=0
  print (i, k)
  for j in exp.model_fields.values():
    l=l+1
    if l==k:
      print (str(j.annotation) , lista2[0])
      if str(j.annotation) in lista2[0]:
        print (j.annotation)



k=0
for i in exp.model_fields:
  k=k+1; l=0
  for j in exp.model_fields.values():
    l=l+1
    if l==k:
      print ('Anotación', j.annotation)
      for m in range(len(lista2)):
        if str(j.annotation)==lista2[m][0]:
          for elto in j.annotation.model_fields:
            print (i, elto)



print('==================')

lista3=[]
for j in exp.model_fields.values():
   if str(j.annotation).find("<class 'clases.")==0:
     lista3.append(j.annotation)


k=0
for i in exp.model_fields:
  k=k+1; l=0
  for j in exp.model_fields.values():
    a=j.annotation
    print (exp.FechaAlta)
    l=l+1
    if l==k:
      if j.annotation in lista3:
        ya=1
        for elto in j.annotation.model_fields.values():
          print (i, elto.annotation)
        






