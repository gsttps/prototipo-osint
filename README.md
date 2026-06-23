# herramienta de prototipo

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![OS](https://img.shields.io/badge/Windows-Linux-success)

Herramienta desarrollada en Python, diseñada para facilitar investigaciones de fuentes abiertas (OSINT). Con una interfaz sencilla basada en terminal, permite recopilar información valiosa sobre dominios, direcciones IP, correos electrónicos y nombres de usuario.

---

## 📋 Características Principales

* **📊 Análisis de Dominios**:
  * Obtiene información WHOIS y RDAP.
  * Soporte de fallback automático para consultas WHOIS vía socket (puerto 43) en caso de errores en RDAP (como el error 403 en TLDs tipo `.cl`).
  * Muestra registros DNS (A, MX, NS, TXT) vía Google DNS API.
* **📧 Verificación de Correo (Leaks)**:
  * Comprueba si un correo electrónico aparece en filtraciones de datos conocidas mediante la API pública de LeakCheck.
  * Muestra el conteo de filtraciones, campos de datos expuestos (contraseñas, nombres) y las bases de datos origen.
* **🔢 Consultas de IP**:
  * Recupera información geográfica (país, región, ciudad, coordenadas) y proveedor de Internet (ISP) usando IPInfo.
* **👤 Búsqueda Concurrente de Usuarios**:
  * Escanea de manera ultra rápida en paralelo (usando multithreading) si un nombre de usuario existe en 11 plataformas populares (GitHub, Instagram, Twitter, TikTok, Steam, etc.).
* **🚪 Escaneo de Puertos Concurrente**:
  * Escanea puertos TCP en paralelo con 100 hilos.
  * Soporta escaneo de puertos comunes, rangos personalizados o listas específicas.
* **📄 Generador de Reportes**:
  * Permite exportar los resultados de cualquier módulo a archivos de reporte organizados en la carpeta `reportes/`.
  * Limpia de manera automática las secuencias de colores ANSI para que los archivos TXT sean legibles en cualquier editor de texto básico (como el Bloc de Notas).

---

## 🚀 Instalación y Uso

### Pasos de Instalación

1. **Clona el repositorio** (o descarga el código fuente):

   ```bash
   git clone https://github.com/tu_usuario/osint_rancio.git
   cd osint_rancio
   ```

2. **Instala las dependencias**:
   Se recomienda usar un entorno virtual:

   ```bash
   python -m venv venv
   # En Windows
   venv\Scripts\activate
   # En Linux/Mac
   source venv/bin/activate
   ```

   Luego instala las librerías necesarias:

   ```bash
   pip install -r requirements.txt
   ```

### Ejecución

Una vez instalado, ejecuta la herramienta desde la terminal:

```bash
python main.py
```

---

## 🛠️ Desarrollo

Si deseas contribuir al proyecto o entender su estructura:

* **Estructura de Carpetas**:
  * `main.py`: Punto de entrada principal y gestor del menú de la terminal.
  * `reportes/`: Directorio autogenerado donde se guardan los reportes TXT.
  * `modulos/`: Contiene las herramientas modulares:
    * `emailcheck.py`: Comprobador de filtraciones de correos electrónicos.
    * `IP.py`: Consultas de direcciones IP.
    * `userfinder.py`: Buscador de usuarios multihilo.
    * `ver_dominio.py`: Análisis de dominios, DNS y WHOIS con socket fallback.
    * `portscanner.py`: Escáner de puertos TCP multihilo.
    * `reporter.py`: Generador de reportes en TXT limpios.
* **Dependencias externas**:
  * `colorama`: Para dar formato y colores al texto en la consola.
  * `requests`: Para interactuar con las APIs HTTP.
* **Dependencias integradas (Python Standard Library)**:
  * `socket`, `concurrent.futures`, `re`, `os`, `threading`.

