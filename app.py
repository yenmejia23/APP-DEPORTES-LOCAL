from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Aquí creamos una lista vacía para guardar los equipos que se vayan registrando
lista_equipos = []

# 1. RUTA PRINCIPAL: Muestra la página de inicio con el formulario y los standings
@app.route('/')
def inicio():
    return render_template('index.html', equipos=lista_equipos)

# 2. RUTA DE REGISTRO: Recibe los datos del formulario y los guarda
@app.route('/registrar', methods=['POST'])
def registrar_equipo():
    nombre_equipo = request.form.get('nombre')
    deporte = request.form.get('deporte')
    
    # Si el usuario escribió un nombre, lo guardamos como un equipo nuevo con 0 puntos para empezar
    if nombre_equipo:
        nuevo_equipo = {
            'nombre': nombre_equipo,
            'deporte': deporte,
            'puntos': 0
        }
        lista_equipos.append(nuevo_equipo)
        
    return redirect(url_for('inicio'))

if __name__ == '__main__':
    app.run(debug=True)