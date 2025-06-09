import requests
from colorama import init, Fore, Style

init(autoreset=True) #necesario para los colores en la terminal

def ipinfo():
    print(f"{Fore.CYAN}Ver datos de una ip{Fore.RESET}")   
    ip = input(f"{Fore.YELLOW}Ingrese una IP: {Fore.RESET}")
    url = f"https://ipinfo.io/{ip}/json?token=a1d4c88db9e5fe"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            datos = response.json()
            print(f"{Fore.CYAN}IP: {Fore.GREEN}{datos.get('ip', 'N/A')}")
            print(f"{Fore.CYAN}País: {Fore.GREEN}{datos.get('country', 'N/A')}")
            print(f"{Fore.CYAN}Ciudad: {Fore.GREEN}{datos.get('city', 'N/A')}")
            print(f"{Fore.CYAN}ISP/ORG: {Fore.GREEN}{datos.get('org', 'N/A')}")
            print(f"{Fore.CYAN}Lat/Lon: {Fore.GREEN}{datos.get('loc', 'N/A')}")
        else:
            print(f"{Fore.RED}No se pudo obtener información de la IP.{Fore.RESET}")
    except requests.RequestException as e:
        print(f"{Fore.RED}Error al consultar la API: {e}{Fore.RESET}")

ipinfo()

if __name__ == "__main__":
    ipinfo()