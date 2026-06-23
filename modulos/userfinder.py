import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import init, Fore
import threading

init(autoreset=True)

try:
    from modulos.reporter import guardar_reporte
except ImportError:
    from reporter import guardar_reporte

# Diccionario de plataformas
PLATAFORMAS = {
    "GitHub": "https://github.com/{}",
    "Twitter": "https://twitter.com/{}",
    "Instagram": "https://www.instagram.com/{}/",
    "Reddit": "https://www.reddit.com/user/{}",
    "TikTok": "https://www.tiktok.com/@{}",
    "Steam": "https://steamcommunity.com/id/{}",
    "Canva": "https://www.canva.com/{}/",
    "Xbox": "https://account.xbox.com/en-us/profile?gamertag={}",
    "PlayStation": "https://my.playstation.com/profile/{}",
    "Twitch": "https://www.twitch.tv/{}",
    "Facebook": "https://www.facebook.com/{}",
}

# Bloqueo para imprimir de forma ordenada en hilos
print_lock = threading.Lock()

def escanear_plataforma(plataforma, url_patron, user, report_lines, found_list):
    url = url_patron.format(user)
    try:
        # User-agent para evitar que algunas redes bloqueen la petición básica
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=5)
        
        with print_lock:
            if response.status_code == 200:
                msg = f"[+] Usuario encontrado en {plataforma}: {url}"
                print(f"{Fore.GREEN}{msg}{Fore.RESET}")
                report_lines.append(msg)
                found_list.append((plataforma, url))
            elif response.status_code == 404:
                msg = f"[-] Usuario no encontrado en {plataforma}"
                print(f"{Fore.RED}{msg}{Fore.RESET}")
                report_lines.append(f"{msg}: {url}")
            else:
                msg = f"[!] Error en {plataforma}: Código {response.status_code}"
                print(f"{Fore.YELLOW}{msg}{Fore.RESET}")
                report_lines.append(f"{msg}: {url}")
    except requests.RequestException as e:
        with print_lock:
            msg = f"[!] {plataforma}: Error de conexión ({e})"
            print(f"{Fore.MAGENTA}{msg}{Fore.RESET}")
            report_lines.append(f"{msg}: {url}")

def check_username():
    while True:
        print(f"\n{Fore.CYAN}=== BUSCAR NOMBRE DE USUARIO ==={Fore.RESET}")
        user = input(f'{Fore.YELLOW}Ingrese usuario a buscar (o \'salir\' para volver): {Fore.RESET}').strip()
        if user.lower() == 'salir':
            break
        if not user:
            continue
        
        print(f'{Fore.CYAN}\nBuscando usuario "{user}" de manera concurrente en {len(PLATAFORMAS)} plataformas...\n{Fore.RESET}')
        
        report_lines = []
        found_list = []
        
        # Uso de ThreadPoolExecutor para escaneo concurrente rápido
        with ThreadPoolExecutor(max_workers=len(PLATAFORMAS)) as executor:
            futures = [
                executor.submit(escanear_plataforma, plat, url_pat, user, report_lines, found_list)
                for plat, url_pat in PLATAFORMAS.items()
            ]
            # Esperar a que terminen todos
            for future in as_completed(futures):
                pass
                
        print(f"\n{Fore.CYAN}--- Resumen de Búsqueda ---{Fore.RESET}")
        if found_list:
            print(f"{Fore.GREEN}[+] Encontrado en {len(found_list)} sitios:{Fore.RESET}")
            for plat, url in found_list:
                print(f"  - {Fore.GREEN}{plat}:{Fore.RESET} {url}")
        else:
            print(f"{Fore.RED}[-] No se encontró el usuario en ninguna plataforma.{Fore.RESET}")
            
        # Preguntar por reporte
        guardar = input(f"\n{Fore.YELLOW}¿Desea generar un reporte en TXT? (s/n): {Fore.RESET}").strip().lower()
        if guardar == 's':
            # Agregar el resumen al reporte
            report_final = []
            report_final.append("RESUMEN:")
            if found_list:
                report_final.append(f"Encontrado en {len(found_list)} de {len(PLATAFORMAS)} plataformas.\n")
                for plat, url in found_list:
                    report_final.append(f"  - {plat}: {url}")
            else:
                report_final.append("No se encontró el usuario en ninguna plataforma.\n")
            report_final.append("\nDETALLES DEL ESCANEO:")
            report_final.extend(report_lines)
            
            guardar_reporte("username", user, report_final)
            
        continuar = input(f'\n{Fore.YELLOW}¿Desea buscar otro usuario? (s/n): {Fore.RESET}')
        if continuar.lower() != 's':
            print(f'{Fore.GREEN}Saliendo del buscador de usuario...{Fore.RESET}')
            break

if __name__ == "__main__":
    check_username()
# 
