import requests
from colorama import init, Fore, Style

init(autoreset=True)

def obtener_dns(domain):
    print(f"\n{Fore.CYAN}--- Registros DNS (vía dns.google) ---{Fore.RESET}")
    for tipo in ["A", "MX", "NS", "TXT"]:
        url = f"https://dns.google/resolve?name={domain}&type={tipo}"
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                datos = resp.json()
                answer = datos.get("Answer", [])
                if answer:
                    print(f"{Fore.GREEN}{tipo} Records:{Fore.RESET}")
                    for ans in answer:
                        data = ans.get("data")
                        ttl = ans.get("TTL")
                        print(f"  - {Fore.LIGHTWHITE_EX}{data}{Fore.LIGHTBLACK_EX} (TTL: {ttl})")
                else:
                    print(f"{Fore.YELLOW}{tipo} Records: No se encontraron registros.{Fore.RESET}")
            else:
                print(f"{Fore.RED}Error al consultar DNS {tipo}: Código {resp.status_code}{Fore.RESET}")
        except requests.RequestException as e:
            print(f"{Fore.RED}Error de red al obtener DNS {tipo}: {e}{Fore.RESET}")

def obtener_whois(domain):
    print(f"\n{Fore.CYAN}--- Información WHOIS / RDAP ---{Fore.RESET}")
    url = f"https://rdap.org/domain/{domain}"
    try:
        resp = requests.get(url, allow_redirects=True, timeout=10)
        if resp.status_code == 200:
            datos = resp.json()
            
            # 1. Registrar
            registrar = "N/A"
            for entity in datos.get("entities", []):
                if "registrar" in entity.get("roles", []):
                    vcard = entity.get("vcardArray", [])
                    if len(vcard) > 1:
                        for item in vcard[1]:
                            if item[0] == "fn":
                                registrar = item[3]
                                break
                    if registrar != "N/A":
                        break
            print(f"{Fore.GREEN}Registrador:{Fore.RESET} {registrar}")
            
            # 2. Fechas Importantes (events)
            events = datos.get("events", [])
            for ev in events:
                action = ev.get("eventAction")
                date = ev.get("eventDate")
                if action == "registration":
                    print(f"{Fore.GREEN}Fecha de Registro:{Fore.RESET} {date}")
                elif action == "expiration":
                    print(f"{Fore.GREEN}Fecha de Expiración:{Fore.RESET} {date}")
                elif action == "last changed":
                    print(f"{Fore.GREEN}Última Modificación:{Fore.RESET} {date}")

            # 3. Servidores de Nombres (nameservers)
            ns_list = datos.get("nameservers", [])
            if ns_list:
                print(f"{Fore.GREEN}Servidores de Nombres (NS):{Fore.RESET}")
                for ns in ns_list:
                    print(f"  - {ns.get('ldhName')}")
            else:
                print(f"{Fore.YELLOW}No se encontraron servidores de nombres en RDAP.{Fore.RESET}")
                
        elif resp.status_code == 404:
            print(f"{Fore.YELLOW}El dominio no está registrado o no se encontró en la base de datos de RDAP.{Fore.RESET}")
        else:
            print(f"{Fore.RED}Error al consultar RDAP: Código {resp.status_code}{Fore.RESET}")
    except requests.RequestException as e:
        print(f"{Fore.RED}Error de red al consultar RDAP: {e}{Fore.RESET}")

def check_domain():
    while True:
        print(f"\n{Fore.CYAN}=== COMPROBAR UN DOMINIO ==={Fore.RESET}")
        domain = input(f"{Fore.YELLOW}Ingrese un dominio (ej: google.com, o 'salir' para volver): {Fore.RESET}").strip()
        if not domain:
            continue
        if domain.lower() == 'salir':
            break
        
        # Limpieza básica de input por si ponen http o https o www
        if domain.startswith("http://"):
            domain = domain[7:]
        elif domain.startswith("https://"):
            domain = domain[8:]
        if domain.startswith("www."):
            domain = domain[4:]
        # Quitar rutas o parámetros
        domain = domain.split("/")[0]

        print(f"\n{Fore.CYAN}Analizando dominio: {Fore.YELLOW}{domain}...")
        
        obtener_dns(domain)
        obtener_whois(domain)
        
        continuar = input(f"\n{Fore.YELLOW}¿Desea comprobar otro dominio? (s/n): {Fore.RESET}")
        if continuar.lower() != 's':
            print(f"{Fore.GREEN}Saliendo del comprobador de dominio...{Fore.RESET}")
            break

if __name__ == "__main__":
    check_domain()
