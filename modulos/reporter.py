import os
import re
from datetime import datetime
from colorama import Fore

def strip_ansi(text):
    # Regex para quitar códigos de color ANSI/VT100
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def guardar_reporte(modulo, target, lineas):
    # Crear carpeta 'reportes' en la raíz del proyecto si no existe
    # El archivo main.py se ejecuta desde la raíz, por lo que 'reportes/' es relativo a ella
    dir_reportes = "reportes"
    if not os.path.exists(dir_reportes):
        try:
            os.makedirs(dir_reportes)
        except Exception as e:
            print(f"{Fore.RED}Error al crear el directorio de reportes: {e}{Fore.RESET}")
            return False

    # Sanitizar el target para que sea un nombre de archivo válido
    target_clean = re.sub(r'[\\/*?:"<>| ]', '_', str(target))
    
    # Formatear la fecha
    fecha_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"reporte_{modulo}_{target_clean}_{fecha_str}.txt"
    filepath = os.path.join(dir_reportes, filename)
    
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            # Encabezado del reporte
            f.write("=" * 60 + "\n")
            f.write(f"REPORTE OSINT - MÓDULO: {modulo.upper()}\n")
            f.write(f"Objetivo: {target}\n")
            f.write(f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")
            
            # Escribir contenido limpio de colores ANSI
            for linea in lineas:
                f.write(strip_ansi(linea) + "\n")
                
        print(f"\n{Fore.GREEN}[+] Reporte guardado con éxito en: {Fore.YELLOW}{filepath}{Fore.RESET}")
        return True
    except Exception as e:
        print(f"{Fore.RED}Error al escribir el archivo de reporte: {e}{Fore.RESET}")
        return False
# 
