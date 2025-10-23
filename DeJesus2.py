# -*- coding: utf-8 -*-
from flask import Flask, request, session, render_template, url_for, redirect, make_response, send_file
from bd import alba, invesdoc, invesicres
from ldap3 import Server, Connection, ALL, NTLM
import io
import datetime as dt


app = Flask(__name__,static_folder='static',template_folder='templates')
app.config.from_object(__name__)
app.secret_key = 'k123j4hkljehrfqw897e69021yqwiehjfweiluy9213yijhfr'
app.config['SESSION_PERMANENT'] = True


def usuarioldap(username,passw):

	try:

		#dccra01.ayuntamiento.svq 10.70.17.180
		#dccra02.ayuntamiento.svq 10.70.24.190
		#dcran01.ayuntamiento.svq 10.70.24.180
		server = Server('ldap://10.70.17.180:389', get_info=ALL)
		conn = Connection(server, user="ayuntamiento.svq\\"+username, password=passw, authentication=NTLM)
		salida=conn.bind()
		conn.closed

		return salida

	except:

		return False


@app.route('/', methods=['GET', 'POST'])
def login():

	barra=''
	entrada=''
	contexto='root'	
	opcion='root'	
	pagina=0
	cambio='0'

	parametros={}

	if 'usuario' in session:

		usuario = session['usuario']
		nombre = session['nombre']

		barra = request.form.get('barra')
		if barra is None: barra=''
		cambio = request.form.get('cambio')
		if cambio is None: cambio='0'		
		entrada = request.form.get('entrada')
		if entrada is None: entrada=''
		contexto = request.form.get('contexto')
		if contexto is None: contexto='root'	
		opcion = request.form.get('opcion')
		if opcion is None: opcion='root'
		pagina = request.form.get('pagina')
		if pagina is None:
			pagina=0
		else:
			pagina=int(pagina)
		parametros=request.form.to_dict()
		if parametros is None: parametros={}
		if cambio=='1': 
			parametros={}
			cambio='0'
		
		#recupera petición anterior
		volver=session['volver']
		indice=len(volver)

		if session['origen']=='volver' and indice>1:
			anterior=volver.pop()
			anterior=volver.pop()

			barra=anterior.get('barra')
			session['barra']=barra
			entrada=anterior.get('entrada')
			session['entrada']=entrada
			contexto=anterior.get('contexto')
			session['contexto']=contexto
			opcion=anterior.get('opcion')
			session['opcion']=opcion
			pagina=anterior.get('pagina')
			session['pagina']=pagina
			parametros=anterior.get('parametros')
			session['parametros']=parametros

			session['origen']='ir'

		#genera menus
		mcontexto=alba.menuContexto(usuario)
		metiqueta=alba.menuEtiqueta(usuario,contexto,opcion)
		mopcion=alba.menuOpcion(usuario,contexto,metiqueta)
		mplaceholder=alba.menuPlaceholder(usuario,contexto,opcion)			

		salida=alba.procesarEntrada(usuario,entrada,contexto,opcion,pagina,parametros)

		#guarda petición anterior
		if opcion!='root':
			seleccion=({'entrada':entrada,'contexto':contexto,'opcion': opcion,'pagina': pagina,'barra': barra,'parametros': parametros})
			if len(volver)>0:
				if seleccion!=volver[len(volver)-1]:
					volver.append(seleccion)
			else:
					volver.append(seleccion)

		#máximo retroceso
		if len(volver)>40:
			volver.pop(0)

		session['volver']=volver

		try:
			if metiqueta!='':
				titulopage=(metiqueta.rsplit(' > ',1)[1] + ' ' + entrada).strip()
			else:
				titulopage='TERA'
		except:
			titulopage='TERA'
			pass

		metiqueta=metiqueta.replace('>','/')
		return render_template("root.html",barra=barra,cambio=cambio,usuario=nombre,entrada=entrada,salida=salida,
			 mcontexto=mcontexto,mopcion=mopcion,metiqueta=metiqueta,
			 contexto=contexto,opcion=opcion,pagina=pagina,
			 mplaceholder=mplaceholder,titulopage=titulopage)
		
	elif request.method == 'POST': 
		
		usuario = request.form.get('usuario')
		usuario=usuario.lower()
		password = request.form.get('password')

		if usuarioldap(usuario,password):
		#if 1==1:

			session.permanent = True
			session['usuario'] = usuario
			nombre=usuario
			#nombre=alba.nombreUsuario(usuario)
			session['nombre'] = nombre

			volver=[]
			session['volver']=volver
			session['origen']='ir'

			mcontexto=alba.menuContexto(usuario)
			metiqueta=alba.menuEtiqueta(usuario,contexto,opcion)
			mopcion=alba.menuOpcion(usuario,contexto,metiqueta)
			mplaceholder=alba.menuPlaceholder(usuario,contexto,opcion)

			#Buscar deshabilitado
			#salida='<script type="text/javascript">ocultarBusqueda();</script>'
			salida=''

			try:
				if metiqueta!='':
					titulopage=(metiqueta.rsplit(' > ',1)[1] + ' ' + entrada).strip()
				else:
					titulopage='TERA'
			except:
				titulopage='TERA'
				pass

			metiqueta=metiqueta.replace('>','/')
			return render_template("root.html",barra=barra,cambio=cambio,usuario=nombre,salida=salida,
			  mcontexto=mcontexto,mopcion=mopcion,metiqueta=metiqueta,
			  contexto=contexto,opcion=opcion,pagina=pagina,
			  mplaceholder=mplaceholder,titulopage=titulopage)

		else:

			mensaje='Usuario o password incorrecto'
			return render_template("login.html",mensaje=mensaje,usuario=usuario,password=password)

	else:

		return render_template("login.html")



@app.route('/logout', methods=['GET', 'POST'])
def logout():

	session.clear()
	return redirect(url_for('login'))



@app.route('/an', methods=['GET', 'POST'])
def an():

	session['origen']='volver'

	return redirect(url_for('login'))

@app.route('/test/<tipo>', methods=['GET', 'POST'])
def test(tipo):

	salida=alba.test(tipo)

	response = make_response(salida)
	response.mimetype = 'text/html'
	return response

@app.route('/exp', methods=['POST'])
def exp():
	
	try:
		sql=request.form.get('sql')
		fnombre=request.form.get('fnombre')

		tiempo = dt.datetime.now()
		#print(tiempo.strftime("%d%m%Y %H%M%S%f"))

		nombre=fnombre + ' ' + session['usuario'] + ' ' + tiempo.strftime("%d%m%Y %H%M%S%f") + '.xlsx'
		fichero=alba.exportarFichero(sql,nombre)

		nombre=fnombre + ' ' + tiempo.strftime("%d-%m-%Y %H%M%S") + '.xlsx'

		return send_file(io.BytesIO(fichero), as_attachment=True,attachment_filename=nombre)
	
	except:
		
		return render_template("salida.html",salida='<h2>☹ Error de proceso</h2>',titulopage='Exportar')


@app.route('/doc/<identificador>', methods=['GET', 'POST'])
def doc(identificador):

	try:
		doc,error=invesdoc.consultarDocumento(identificador)

		if doc is not None:

			response = make_response(doc)
			#response.headers['Content-Disposition'] = "attachment; filename='sakulaci.pdf"
			response.mimetype = 'application/pdf'
			return response

		else:

			response = make_response(error)
			response.mimetype = 'text/html'
			return response
	except:
		
		return render_template("salida.html",salida='<h2>☹ Error de proceso</h2>',titulopage='Invesdoc')


@app.route('/expte/<expediente>', methods=['GET', 'POST'])
def expte(expediente):

	doc=None

	try:
		doc=alba.expte(expediente)

		if doc is not None:

			response = make_response(doc)
			response.mimetype = 'application/pdf'
			return response

		else:

			response = make_response('<h2>☹ Expediente no generado</h2>')
			response.mimetype = 'text/html'
			return response
	except:
		
		return render_template("salida.html",salida='<h2>☹ Error de proceso</h2>',titulopage='Expediente')	


@app.route('/reg/<numeroRegistro>/<secuenciaIdentificador>/<extension>', methods=['GET', 'POST'])
def reg(numeroRegistro,secuenciaIdentificador,extension):

	try:	
		doc=invesicres.consultarDocumento(numeroRegistro,secuenciaIdentificador,extension)

		if doc is not None:

			response = make_response(doc)
			#response.headers['Content-Disposition'] = "attachment; filename='sakulaci.pdf"
			response.mimetype = 'application/pdf'
			return response

		else:

			response = make_response('<h2>☹ Documento No Encontrado</h2>')
			response.mimetype = 'text/html'
			return response
	except:
		
		return render_template("salida.html",salida='<h2>☹ Error de proceso</h2>',titulopage='Registro')


@app.route('/fir/<identificador>', methods=['GET', 'POST'])
def fir(identificador):

	try:	
		doc=alba.obtenerFirma(identificador)

		if doc is not None:

			response = make_response(doc)
			response.mimetype = 'application/pdf'
			return response

		else:

			return render_template("salida.html",salida='<h2>☹ Documento no encontrado</h2>',titulopage='firma')
	except:

		return render_template("salida.html",salida='<h2>☹ Error de proceso</h2>',titulopage='Firma')
	

@app.route('/mud/<identificador>', methods=['GET', 'POST'])
def mud(identificador):

	try:
		doc,extension,nombre=alba.obtenerPrueba(identificador)

		if doc is not None:

			response = make_response(doc)
			#response.headers['Content-Disposition'] = "attachment; filename='sakulaci.pdf"
			#response.headers['Content-Disposition'] = "filename=" + identificador + '.' + extension.lower()
			if extension=='JPG':
				response.mimetype = 'image/jpeg'
			elif extension=='JPEG':
				response.mimetype = 'image/jpeg'			
			elif extension=='MP4':
				response.headers['Content-Disposition'] = "attachment; filename=" + nombre
				response.mimetype = 'video/mp4'
			elif extension=='PDF':
				response.mimetype = 'application/pdf'			
			return response

		else:

			response = make_response('<h2>☹ Documento No Encontrado</h2>')
			response.mimetype = 'text/html'
			return response
	except:

		return render_template("salida.html",salida='<h2>☹ Error de proceso</h2>',titulopage='Imagen')
	

@app.route('/informe/<tipo>/<id>', methods=['GET', 'POST'])
def informe(tipo,id):

	try:
		doc=alba.informe(tipo,id)

		if doc is not None:

			response = make_response(doc)
			response.mimetype = 'application/pdf'
			return response

		else:

			response = make_response('<h2>☹ Error la generación del documento</h2>')
			response.mimetype = 'text/html'
			return response
	except:

		return render_template("salida.html",salida='<h2>☹ Error de proceso</h2>',titulopage='Informe')
	

@app.route('/documento/<tipo>/<id>', methods=['GET', 'POST'])
@app.route('/documento/<tipo>/<id>/<nombredoc>', methods=['GET', 'POST'])
def documento(tipo,id,nombredoc=''):

	try:
		if tipo!='5':
			nombredoc=nombredoc.split('¬')[0]
		doc=alba.documento(tipo,id,nombredoc)

		if doc is not None:

			response = make_response(doc)
			if tipo=='4' or (id[-3:].upper()=='XML'):
				response.mimetype = 'application/xml'
			else:
				response.mimetype = 'application/pdf'

			if tipo=='7':
				match nombredoc[-4:].upper():
					case '.PDF':
						response.mimetype = "application/pdf"
					case '.XML':
						response.mimetype = "application/xml"
					case '.RTF':
						response.mimetype = "application/rtf"
					case '.JPG':
						response.mimetype = "image/jpeg"					
					case 'JPEG':
						response.mimetype = "image/jpeg"
					case '.PNG':
						response.mimetype = "image/png"
					case '.GIF':
						response.mimetype = "application/gif"
					case '.ZIP':
						response.mimetype = "application/zip"
					case '.SVG':
						response.mimetype = "svg+xml"
					case 'XSIG':
						response.mimetype = "application/xml"
					case '.XLS':
						response.mimetype = "application/vnd.ms-excel"			
					case 'XLSX':
						response.mimetype = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"													

			return response

		else:	

			response = make_response('<h2>☹ No existe el documento</h2>')
			response.mimetype = 'text/html'
			return response
	except:

		return render_template("salida.html",salida='<h2>☹ Error de proceso</h2>',titulopage='Documento')


@app.route('/firma/<esmid>', methods=['GET', 'POST'])		
@app.route('/firma/<esmid>/<nif>', methods=['GET', 'POST'])
def firma(esmid='',nif=''):

	try:
		if request.method == 'POST': 
			esmid=request.form.get('esmid')
			nif=request.form.get("nif")

		if esmid != '' and esmid is not None:
			estado,destado,doc=alba.firma(esmid,nif)
			match estado:
				case '4': #Firmado
					if doc is not None:
						response = make_response(doc)		
						response.mimetype = 'application/pdf'		
						return response
					else:
						return render_template("salida.html",salida='Estado: ' + estado + 'Descripción: ' + destado,titulopage='firma')
				case '3':
					return render_template("salida.html",salida=destado,titulopage='firma')
				case '2':
					return render_template("salida.html",salida=destado,titulopage='firma')
				case '1':
					if doc is not None:
						response = make_response(doc)
						response.mimetype = 'application/pdf'		
						return response
					else:
						return render_template("salida.html",salida=destado,titulopage='firma')
				case '0':
					return render_template("salida.html",salida='<h2>☹ Identificador de documento no encontrado</h2>',titulopage='firma')
		else:
			return render_template("salida.html",salida='<h2>☹ Identificador de documento vacío</h2>',titulopage='firma')
	
	except:

		return render_template("salida.html",salida='<h2>☹ Error en el proceso de firma</h2>',titulopage='Firma')



if __name__ == "__main__":

    app.run(host='0.0.0.0')
    #app.run(host='0.0.0.0',ssl_context=('cert.pem', 'key.pem'))
