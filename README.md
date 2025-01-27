# 🎥 YT Downloader 

## ✨ Características principales

- **Interfaz moderna y responsive**
- **Modo oscuro/claro**
- **Previsualización de metadatos y miniatura**
- **Barra de progreso en tiempo real**
- **Descarga automática al completarse**
- **Soporte para múltiples formatos y calidades**
- **Integración con Docker**

---

## 🚀 Instalación rápida

### Requisitos previos

- Python 3.8+
- FFmpeg
- Docker (opcional)

---

### Método 1: Usando Docker (recomendado)

```bash
# Clona el repositorio
git clone https://github.com/N3Y-C/Youtube-Downloader.git
cd Youtube-Downloader

# Construye y ejecuta la imagen de Docker
docker build -t youtube-downloader .
docker run -d -p 5000:5000 --name youtube-downloader youtube-downloader
```

Accede a la aplicación en tu navegador:
```
http://localhost:5000
```

---

### Método 2: Instalación manual

```bash
# Clona el repositorio
git clone https://github.com/N3Y-C/Youtube-Downloader.git
cd Youtube-Downloader

# Crea un entorno virtual e instala las dependencias
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Instala FFmpeg
# Para macOS
brew install ffmpeg

# Para Linux (Debian/Ubuntu)
sudo apt install ffmpeg

# Para Windows (usando Chocolatey)
choco install ffmpeg

# Ejecuta la aplicación
python app.py
```

Accede a la aplicación en tu navegador:
```
http://localhost:5000
```

---

## 🛠️ Uso

1. Ingresa la URL del video de YouTube en el campo de texto.
2. Haz clic en "Analizar" para ver los metadatos del video.
3. Haz clic en "Descargar" para iniciar la descarga.
4. ¡Listo! El video se descargará automáticamente cuando esté listo.

---

## 🐳 Dockerfile

El proyecto incluye un Dockerfile para facilitar la implementación. Aquí está el contenido:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

---

## 🧑‍💻 Estructura del proyecto

```
yt-downloader-pro/
├── app.py                  # Backend principal (Flask)
├── requirements.txt        # Dependencias de Python
├── Dockerfile              # Configuración de Docker
├── README.md               # Este archivo
├── LICENSE                 # Licencia del proyecto
├── static/
│   ├── style.css           # Estilos CSS
│   └── script.js           # Lógica del frontend
└── templates/
    └── index.html          # Plantilla HTML principal
```

---

## 🤝 Contribución

¡Las contribuciones son bienvenidas! Si deseas mejorar este proyecto, sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza tus cambios y haz commit (`git commit -am 'Añade nueva funcionalidad'`).
4. Haz push a la rama (`git push origin feature/nueva-funcionalidad`).
5. Abre un Pull Request.

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---

Hecho con ❤️ por [NEY-C](https://github.com/N3Y-C) | [¡Dame una estrella! ⭐]