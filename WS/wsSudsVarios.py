from suds.client import Client

consulta = Client('http://10.70.19.36:8080/alba2WS-tasas/tasasServices/alba2WS-tasas?wsdl')
print (consulta)

#liq=consulta.factory.create('string') 'No es un tipo a definir; es un string. No hay que hacer nada

respuesta=consulta.service.impresionPago('202501849020')
#print (respuesta)
print (respuesta.Resultado,respuesta.Descripcion)

respuesta=consulta.service.TarifasExaccion('RECOBASU')
print ('----')
print (respuesta)
print ('----')
for elto in respuesta.Tarifas:
    print (elto.Descripcion, elto.Tarifa)


