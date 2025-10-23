from flask import Flask, render_template, url_for, redirect, make_response

app = Flask(__name__,static_folder='../static',template_folder='../templates2')
app.config.from_object(__name__)

@app.route('/test', methods=['GET', 'POST'])
def test():

			response = make_response('<h2>☹ Expediente no generado</h2>')
			response.mimetype = 'text/html'
			return response

@app.route('/exp', methods=['GET', 'POST'])
def exp():
    contenido = {
				'barra':'barra',
				'cambio':'cambio',
				'nombre':'Rafa',
				'entrada':'entrada',
				'salida':'salida',
				'mcontexto':'mcontexto',
				'mopcion':'mopcion',
				'metiqueta':'metiqueta',
				'contexto':'contexto',
				'opcion':'opcion',
				'pagina':'pagina',
				'mplaceholder':'mplaceholder',
				'titulopage':'titulopage'
                }


    rendered_html =  render_template("root.html", barra='barra',
				cambio='cambio',
				nombre='Rafa',
				entrada='entrada',
				salida='salida',
				mcontexto='mcontexto',
				mopcion='mopcion',
				metiqueta='metiqueta',
				contexto='contexto',
				opcion='opcion',
				pagina='pagina',
				mplaceholder='mplaceholder',
				titulopage='titulopage')

    return (rendered_html)

if __name__ == "__main__":

    app.run(host='0.0.0.0')
    #app.run(host='0.0.0.0',ssl_context=('cert.pem', 'key.pem'))
