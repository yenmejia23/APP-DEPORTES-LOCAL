import os
from flask import Flask, render_template, request, redirect
app = Flask(__name__)

# --- TU CÓDIGO ORIGINAL (Base de datos de equipos) ---
equipos_registrados = []

# --- NUEVA BASE DE DATOS PARA JORNADAS Y ROLES ---
roles_deportes = {
    'softball': {
        'nombre_pantalla': 'Softball (Sábados)',
        'jornada': 'SIN JORNADA PROGRAMADA',
        'partidos': [],
        'descansa': ''
    },
    'beisbol': {
        'nombre_pantalla': 'Béisbol (Domingos)',
        'jornada': 'SIN JORNADA PROGRAMADA',
        'partidos': [],
        'descansa': ''
    },
    'basquetbol': {
        'nombre_pantalla': 'Básquetbol (Sábados)',
        'jornada': 'SIN JORNADA PROGRAMADA',
        'partidos': [],
        'descansa': ''
    },
    'futbol': {
        'nombre_pantalla': 'Fútbol (Domingos)',
        'jornada': 'SIN JORNADA PROGRAMADA',
        'partidos': [],
        'descansa': ''
    }
}

# 1. RUTA PRINCIPAL: Muestra el menú con los 4 botones grandes
@app.route('/')
def home():
    return render_template('menu.html')

# 2. TU RUTA ORIGINAL: Tu pantalla verde de registro de equipos sigue viva aquí
# Para entrar a ella, solo tendrás que ir a tu-enlace.com/registro
@app.route('/registro', methods=['GET', 'POST'])
def registro_equipos():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        deporte = request.form.get('deporte')
        if nombre and deporte:
            equipos_registrados.append({'nombre': nombre.upper(), 'deporte': deporte})
        return redirect('/registro')
    return render_template('index.html', equipos=equipos_registrados)

# 3. RUTA PÚBLICA: Muestra la tabla del deporte seleccionado
@app.route('/deporte/<tipo_deporte>')
def ver_deporte(tipo_deporte):
    if tipo_deporte in roles_deportes:
        datos = roles_deportes[tipo_deporte]
        return render_template(
            'rol.html', 
            deporte_nombre=datos['nombre_pantalla'],
            jornada_info=datos['jornada'],
            partidos=datos['partidos'],
            equipo_descansa=datos['descansa']
        )
    return redirect('/')

# 4. RUTA DEL PANEL: Abre el formulario para que tú lo llenes
@app.route('/admin')
def admin_panel():
    return render_template('admin.html')

# 5. RUTA DE PROCESAMIENTO: Recibe los datos del formulario y los guarda
@app.route('/guardar_rol', methods=['POST'])
def guardar_rol():
    deporte = request.form.get('deporte')
    
    if deporte in roles_deportes:
        roles_deportes[deporte]['jornada'] = request.form.get('jornada').upper()
        roles_deportes[deporte]['descansa'] = request.form.get('descansa').upper()
        roles_deportes[deporte]['partidos'] = []
        
        for i in range(1, 6):
            local = request.form.get(f'local{i}')
            campo = request.form.get(f'campo{i}')
            visita = request.form.get(f'visita{i}')
            
            if local and campo and visita:
                roles_deportes[deporte]['partidos'].append({
                    'local': local.upper(),
                    'campo': campo.upper(),
                    'visita': visita.upper()
                })
                
    return redirect(f'/deporte/{deporte}')

if __name__ == '__main__':
    # Esto lee el puerto que Render necesita de forma automática
    puerto = int(os.environ.get("PORT", 5000))
    # Arranca la app en el host público 0.0.0.0
    app.run(host='0.0.0.0', port=puerto, debug=True)