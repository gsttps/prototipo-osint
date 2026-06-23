import requests
from colorama import init, Fore, Style

init(autoreset=True) #necesario para los colores en la terminal

try:
    from modulos.reporter import guardar_reporte
except ImportError:
    from reporter import guardar_reporte

def check_ip():
    while True:
        print(f"\n{Fore.CYAN}=== VER DATOS DE UNA IP ==={Fore.RESET}")   
        ip = input(f"{Fore.YELLOW}Ingrese una IP (o 'salir' para volver): {Fore.RESET}").strip()
        if ip.lower() == 'salir':
            break
        if not ip:
            continue
        url = f"https://ipinfo.io/{ip}/json?token=a1d4c88db9e5fe"
        report_lines = []
        try:
            response = requests.get(url)
            if response.status_code == 200:
                datos = response.json()
                
                # Construir y guardar cada línea de información
                def add_info(label, key):
                    val = datos.get(key, 'N/A')
                    line = f"{label}: {val}"
                    print(f"{Fore.CYAN}{label}: {Fore.GREEN}{val}")
                    report_lines.append(line)
                
                print("")
                add_info("IP", "ip")
                add_info("País", "country")
                add_info("Ciudad", "city")
                add_info("ISP/ORG", "org")
                add_info("Lat/Lon", "loc")
                add_info("Código Postal", "postal")
                add_info("Hostname", "hostname")
                add_info("Anycast", "anycast")
                
                # Preguntar por reporte
                guardar = input(f"\n{Fore.YELLOW}¿Desea generar un reporte en TXT? (s/n): {Fore.RESET}").strip().lower()
                if guardar == 's':
                    guardar_reporte("ipinfo", ip, report_lines)
            else:
                print(f"{Fore.RED}No se pudo obtener información de la IP.{Fore.RESET}")
        except requests.RequestException as e:
            print(f"{Fore.RED}Error al consultar la API: {e}{Fore.RESET}")
        
        continuar = input(f"\n{Fore.YELLOW}¿Desea consultar otra IP? (s/n): {Fore.RESET}")
        if continuar.lower() != 's':
            print(f"{Fore.GREEN}Saliendo del módulo de IP...{Fore.RESET}")
            break

if __name__ == "__main__":
    check_ip()
# 
