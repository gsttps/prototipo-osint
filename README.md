# osint_rancio

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![MIT](https://img.shields.io/badge/Windows-Linux-success)

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![MIT](https://img.shields.io/badge/Windows-Linux-success)

# OSINT RANCIO

**OSINT RANCIO** es una herramienta de código abierto desarrollada en Python, diseñada para facilitar investigaciones de código abierto (OSINT). Con una interfaz sencilla basada en terminal, permite recopilar información valiosa sobre dominios, direcciones IP, correos electrónicos y nombres de usuario.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![MIT](https://img.shields.io/badge/Windows-Linux-success)

## 📋 Características Principales

*   **📊 Análisis de Dominios**:
    *   Obtiene información WHOIS y RDAP.
    *   Muestra registros DNS (A, MX, NS, TXT).
    *   Detecta servidores de nombres.
*   **📧 Verificación de Correo**:
    *   Comprueba si existe un buzón de correo electrónico.
    *   Verifica si el dominio tiene registros MX (indicando capacidad de recibir correos).
*   **🔢 Consultas de IP**:
    *   Recupera información geográfica (país, región, ciudad).
    *   Muestra el nombre del proveedor de Internet (ISP).
    *   Realiza pruebas de ping básicas para verificar conectividad.
*   **👤 Búsqueda de Usuarios**:
    *   Busca un nombre de usuario en múltiples plataformas sociales (GitHub, Instagram, TikTok, etc.).
    *   Proporciona enlaces directos a los perfiles encontrados.
*   **🚪 Escaneo de Puertos**:
    *   Escaneo básico de puertos TCP.
    *   Identifica puertos abiertos y servicios asociados.

---

## 🚀 Instalación y Uso

### Requisitos Previos

*   **Python 3.8** o superior.
*   **Git** (recomendado para clonar el repositorio).

### Pasos de Instalación

1.  **Clona el repositorio** (o descarga el código fuente):
    ```bash
    git clone https://github.com/tu_usuario/osint_rancio.git
    cd osint_rancio
    ```

2.  **Instala las dependencias**:
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

Se mostrará el menú principal donde podrás seleccionar la herramienta que deseas utilizar.

---

## 🛠️ Desarrollo

Si deseas contribuir al proyecto o entender su estructura:

*   **Estructura de Carpetas**:
    *   `main.py`: Punto de entrada principal y gestor del menú.
    *   `modulos/`: Contiene cada herramienta como un módulo independiente.
        *   `emailcheck.py`: Verificación de correos electrónicos.
        *   `IP.py`: Consultas de direcciones IP.
        *   `userfinder.py`: Búsqueda de nombres de usuario.
        *   `ver_dominio.py`: Análisis de dominios y DNS.
        *   `portscanner.py`: Escaneo de puertos.
*   **Dependencias**:
    *   `colorama`: Para coloración en terminal.
    *   `requests`: Para peticiones HTTP (APIs, RDAP).
    *   `socket`: Para consultas WHOIS directas.

---

## 📝 Licencia

Este proyecto está licenciado bajo la **Licencia MIT**. Siéntete libre de usarlo, modificarlo y distribuirlo.

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, crea un *fork* del proyecto y abre un *Pull Request* con tu propuesta.

---

## 📞 Contacto / Creador

*   **Creador**: [Tu Nombre o Nick]
*   **GitHub**: [Enlace a tu GitHub]

---

*Este proyecto está en desarrollo continuo. ¡Gracias por usar OSINT RANCIO!* 🚀
