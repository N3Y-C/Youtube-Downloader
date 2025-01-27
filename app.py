from flask import Flask, render_template, request, send_file, jsonify
from flask_cors import CORS
import yt_dlp
import os
import time
import threading
import re
from pathlib import Path

app = Flask(__name__)
CORS(app)
app.config['DOWNLOAD_FOLDER'] = 'downloads'
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'

progress = {'porcentaje': '0%', 'estado': 'inactivo', 'archivo': None}

if not os.path.exists(app.config['DOWNLOAD_FOLDER']):
    os.makedirs(app.config['DOWNLOAD_FOLDER'])

class ProgressLogger:
    def __init__(self):
        self.progress = 0
        
    def debug(self, msg):
        pass
        
    def warning(self, msg):
        pass
        
    def error(self, msg):
        print(msg)
        
    def hook(self, d):
        global progress
        if d['status'] == 'downloading':
            progress['porcentaje'] = self.limpiar_ansi(d['_percent_str'])
            progress['velocidad'] = self.limpiar_ansi(d['_speed_str'])
            progress['tiempo'] = self.limpiar_ansi(d['_eta_str'])
        elif d['status'] == 'finished':
            progress['estado'] = 'completado'
    
    def limpiar_ansi(self, texto):
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', texto).strip()

@app.route('/progreso')
def obtener_progreso():
    return jsonify(progress)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/metadatos', methods=['POST'])
def obtener_metadatos():
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({'error': 'URL no proporcionada'}), 400

        ydl = yt_dlp.YoutubeDL({'quiet': True})
        info = ydl.extract_info(url, download=False)
        
        return jsonify({
            'titulo': info.get('title', ''),
            'duracion': time.strftime('%H:%M:%S', time.gmtime(info.get('duration', 0))),
            'resolucion': f"{info.get('width', 0)}x{info.get('height', 0)}",
            'thumbnail': info.get('thumbnail', '')
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/descargar', methods=['POST'])
def descargar():
    global progress
    progress = {'porcentaje': '0%', 'estado': 'descargando', 'archivo': None}
    
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({'error': 'URL no proporcionada'}), 400

        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
            'outtmpl': os.path.join(app.config['DOWNLOAD_FOLDER'], '%(title)s.%(ext)s'),
            'noplaylist': True,
            'progress_hooks': [ProgressLogger().hook],
            'keepvideo': True,
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4'
            }]
        }

        def descarga_asincrona():
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                global progress
                final_filename = re.sub(r'\.f\d+', '', ydl.prepare_filename(info))
                progress['archivo'] = os.path.abspath(final_filename)
                progress['estado'] = 'completado'
                
        thread = threading.Thread(target=descarga_asincrona)
        thread.start()
        
        return jsonify({'mensaje': 'Descarga iniciada'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/descargar-archivo')
def descargar_archivo():
    global progress
    if progress['estado'] != 'completado' or not progress['archivo']:
        return jsonify({'error': 'Descarga no completada'}), 404
        
    filename = progress['archivo']
    if not os.path.exists(filename):
        return jsonify({'error': 'Archivo no encontrado'}), 404
        
    try:
        return send_file(filename, as_attachment=True)
    finally:
        # Limpiar después de enviar el archivo
        if os.path.exists(filename):
            os.remove(filename)
        progress['estado'] = 'inactivo'
        progress['archivo'] = None

if __name__ == '__main__':
    app.run(debug=True)