import requests
from colorama import init, Fore, Style

init(autoreset=True)

def emailbuscar(email):
    url = "https://leakcheck.io/api/public"
    params = {"check": email}
    try:
        print(f"{Fore.CYAN}Consultando LeakCheck API para: {Fore.YELLOW}{email}...")
        resp = requests.get(url, params=params)
        if resp.status_code == 200:
            datos = resp.json()
            if datos.get("success"):
                found_count = datos.get("found", 0)
                if found_count > 0:
                    print(f"\n{Fore.GREEN}[+] ¡ATENCIÓN! El email {email} aparece en {found_count} filtraciones de datos.{Fore.RESET}")
                    
                    # Mostrar campos filtrados
                    fields = datos.get("fields", [])
                    if fields:
                        print(f"{Fore.CYAN}Campos expuestos: {Fore.RED}{', '.join(fields)}{Fore.RESET}")
                    
                    # Mostrar fuentes/filtraciones (limitado a las primeras 15 para no saturar)
                    sources = datos.get("sources", [])
                    if sources:
                        print(f"\n{Fore.CYAN}Fuentes de filtración (mostrando hasta 15):{Fore.RESET}")
                        limit = 15
                        for src in sources[:limit]:
                            name = src.get("name", "Desconocido")
                            date = src.get("date", "Fecha no disponible")
                            date_str = f" ({date})" if date else ""
                            print(f" {Fore.RED}- {name}{Fore.LIGHTBLACK_EX}{date_str}{Fore.RESET}")
                        
                        if len(sources) > limit:
                            print(f" {Fore.YELLOW}... y {len(sources) - limit} fuentes más.{Fore.RESET}")
                else:
                    print(f"{Fore.GREEN}[-] El email {email} NO aparece en ninguna filtración conocida.{Fore.RESET}")
            else:
                print(f"{Fore.RED}LeakCheck reportó un problema: {datos.get('error', 'Error desconocido')}{Fore.RESET}")
        else:
            print(f"{Fore.RED}Error al consultar LeakCheck API. Código: {resp.status_code}{Fore.RESET}")
    except requests.RequestException as e:
        print(f"{Fore.RED}Error de red: {e}{Fore.RESET}")

def check_email():
    while True:
        print(f"\n{Fore.CYAN}=== COMPROBACIÓN DE CORREO E-MAIL ==={Fore.RESET}")
        email = input(f"{Fore.YELLOW}Ingrese un email a buscar (o 'salir' para volver): {Fore.RESET}").strip()
        if not email:
            continue
        if email.lower() == 'salir':
            break
        emailbuscar(email)

if __name__ == "__main__":
    check_email()

