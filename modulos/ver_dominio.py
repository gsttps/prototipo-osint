import requests
import socket
import re
from colorama import init, Fore, Style

init(autoreset=True)

try:
    from modulos.reporter import guardar_reporte
except ImportError:
    from reporter import guardar_reporte

def obtener_dns(domain, report_lines):
    print(f"\n{Fore.CYAN}--- Registros DNS (vía dns.google) ---{Fore.RESET}")
    report_lines.append("\n--- REGISTROS DNS ---")
    for tipo in ["A", "MX", "NS", "TXT"]:
        url = f"https://dns.google/resolve?name={domain}&type={tipo}"
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                datos = resp.json()
                answer = datos.get("Answer", [])
                if answer:
                    print(f"{Fore.GREEN}{tipo} Records:{Fore.RESET}")
                    report_lines.append(f"{tipo} Records:")
                    for ans in answer:
                        data = ans.get("data")
                        ttl = ans.get("TTL")
                        print(f"  - {Fore.LIGHTWHITE_EX}{data}{Fore.LIGHTBLACK_EX} (TTL: {ttl})")
                        report_lines.append(f"  - {data} (TTL: {ttl})")
                else:
                    print(f"{Fore.YELLOW}{tipo} Records: No se encontraron registros.{Fore.RESET}")
                    report_lines.append(f"{tipo} Records: No se encontraron registros.")
            else:
                msg = f"Error al consultar DNS {tipo}: Código {resp.status_code}"
                print(f"{Fore.RED}{msg}{Fore.RESET}")
                report_lines.append(msg)
        except requests.RequestException as e:
            msg = f"Error de red al obtener DNS {tipo}: {e}"
            print(f"{Fore.RED}{msg}{Fore.RESET}")
            report_lines.append(msg)

def whois_raw_query(server, query):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5.0)
        s.connect((server, 43))
        s.send((query + "\r\n").encode("utf-8"))
        response = b""
        while True:
            data = s.recv(4096)
            if not data:
                break
            response += data
        s.close()
        return response.decode("utf-8", errors="ignore")
    except Exception as e:
        return f"Error: {e}"

def whois_socket_fallback(domain):
    # 1. Consultar IANA para ver el servidor WHOIS de referencia
    iana_res = whois_raw_query("whois.iana.org", domain)
    refer_server = None
    for line in iana_res.splitlines():
        if line.strip().lower().startswith("refer:"):
            refer_server = line.split(":", 1)[1].strip()
            break
            
    # 2. Consultar el servidor específico
    if refer_server and refer_server != "whois.iana.org":
        return whois_raw_query(refer_server, domain)
    return iana_res

def parse_raw_whois(raw_text):
    registrar = "Desconocido"
    created = "Desconocido"
    expires = "Desconocido"
    ns = []
    
    # Extraer Registrar
    reg_match = re.search(r'(?:Registrar Name|Registrar|registrar name|Registrar name|registrar):\s*(.*)', raw_text, re.IGNORECASE)
    if reg_match:
        registrar = reg_match.group(1).strip()
        
    # Extraer Fechas
    created_match = re.search(r'(?:Creation date|Creation Date|Created on|Created|Registered on|Fecha de registro|registered):\s*(.*)', raw_text, re.IGNORECASE)
    if created_match:
        created = created_match.group(1).strip()
        
    exp_match = re.search(r'(?:Expiration date|Expiration Date|Registry Expiry Date|Expires on|Expires|Fecha de vencimiento|expire):\s*(.*)', raw_text, re.IGNORECASE)
    if exp_match:
        expires = exp_match.group(1).strip()
        
    # Extraer NS
    ns_matches = re.findall(r'(?:Name server|Name Server|nserver|nservers|nameserver):\s*(.*)', raw_text, re.IGNORECASE)
    for match in ns_matches:
        # Limpieza de ip o datos extras entre paréntesis
        cleaned = re.sub(r'\s*\(.*\)', '', match).strip()
        ns.append(cleaned)
        
    return registrar, created, expires, ns

def obtener_whois(domain, report_lines):
    print(f"\n{Fore.CYAN}--- Información WHOIS / RDAP ---{Fore.RESET}")
    report_lines.append("\n--- INFORMACIÓN WHOIS / RDAP ---")
    
    # Intentar RDAP primero
    url = f"https://rdap.org/domain/{domain}"
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        resp = requests.get(url, headers=headers, allow_redirects=True, timeout=10)
        
        if resp.status_code == 200:
            datos = resp.json()
            
            # Registrar
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
            report_lines.append(f"Registrador: {registrar}")
            
            # Fechas Importantes
            events = datos.get("events", [])
            for ev in events:
                action = ev.get("eventAction")
                date = ev.get("eventDate")
                if action == "registration":
                    print(f"{Fore.GREEN}Fecha de Registro:{Fore.RESET} {date}")
                    report_lines.append(f"Fecha de Registro: {date}")
                elif action == "expiration":
                    print(f"{Fore.GREEN}Fecha de Expiración:{Fore.RESET} {date}")
                    report_lines.append(f"Fecha de Expiración: {date}")
                elif action == "last changed":
                    print(f"{Fore.GREEN}Última Modificación:{Fore.RESET} {date}")
                    report_lines.append(f"Última Modificación: {date}")

            # Servidores de Nombres
            ns_list = datos.get("nameservers", [])
            if ns_list:
                print(f"{Fore.GREEN}Servidores de Nombres (NS):{Fore.RESET}")
                report_lines.append("Servidores de Nombres (NS):")
                for ns in ns_list:
                    ns_name = ns.get('ldhName')
                    print(f"  - {ns_name}")
                    report_lines.append(f"  - {ns_name}")
            else:
                print(f"{Fore.YELLOW}No se encontraron servidores de nombres en RDAP.{Fore.RESET}")
                report_lines.append("No se encontraron servidores de nombres en RDAP.")
            return
            
        else:
            # RDAP falló (por ejemplo, código 403 o 404)
            msg_fail = f"RDAP reportó estado {resp.status_code} (TLD no soportado o bloqueado)."
            if resp.status_code == 403:
                try:
                    err_msg = resp.json().get("message", "")
                    if err_msg:
                        msg_fail = f"RDAP no disponible para este TLD: {err_msg}"
                except Exception:
                    pass
            print(f"{Fore.YELLOW}[!] {msg_fail} Intentando WHOIS vía socket port 43...{Fore.RESET}")
            report_lines.append(f"RDAP falló: {msg_fail}. Usando fallback socket WHOIS.")
            
    except requests.RequestException as e:
        print(f"{Fore.YELLOW}[!] Error al consultar RDAP ({e}). Intentando WHOIS vía socket port 43...{Fore.RESET}")
        report_lines.append(f"Error RDAP: {e}. Usando fallback socket WHOIS.")

    # Fallback: Query WHOIS server via socket port 43
    raw_whois = whois_socket_fallback(domain)
    
    # Validar si fuimos bloqueados
    if "blocked" in raw_whois.lower() or "overload" in raw_whois.lower() or "limit exceeded" in raw_whois.lower():
        msg_block = "El servidor WHOIS port 43 de la TLD bloqueó la conexión por límite de consultas (rate-limit)."
        print(f"{Fore.RED}[-] {msg_block}{Fore.RESET}")
        report_lines.append(msg_block)
        report_lines.append("\nRespuesta raw del servidor:")
        report_lines.append(raw_whois)
        return
        
    if raw_whois.strip().startswith("Error:"):
        msg_err = f"No se pudo conectar a los servidores WHOIS port 43 ({raw_whois.strip()})."
        print(f"{Fore.RED}[-] {msg_err}{Fore.RESET}")
        report_lines.append(msg_err)
        return

    # Parsear respuesta socket
    registrar, created, expires, ns = parse_raw_whois(raw_whois)
    
    print(f"{Fore.GREEN}Registrador (WHOIS):{Fore.RESET} {registrar}")
    report_lines.append(f"Registrador (WHOIS): {registrar}")
    
    print(f"{Fore.GREEN}Fecha de Registro (WHOIS):{Fore.RESET} {created}")
    report_lines.append(f"Fecha de Registro (WHOIS): {created}")
    
    print(f"{Fore.GREEN}Fecha de Expiración (WHOIS):{Fore.RESET} {expires}")
    report_lines.append(f"Fecha de Expiración (WHOIS): {expires}")
    
    if ns:
        print(f"{Fore.GREEN}Servidores de Nombres (NS - WHOIS):{Fore.RESET}")
        report_lines.append("Servidores de Nombres (NS - WHOIS):")
        for n in ns:
            print(f"  - {n}")
            report_lines.append(f"  - {n}")
    else:
        print(f"{Fore.YELLOW}No se encontraron servidores de nombres en WHOIS.{Fore.RESET}")
        report_lines.append("No se encontraron servidores de nombres en WHOIS.")

    # Guardar la respuesta raw completa en el reporte de texto por seguridad/utilidad
    report_lines.append("\n--- RESPUESTA RAW COMPLETA DE WHOIS ---")
    report_lines.append(raw_whois)

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
        
        report_lines = []
        report_lines.append(f"Dominio analizado: {domain}")
        
        obtener_dns(domain, report_lines)
        obtener_whois(domain, report_lines)
        
        # Preguntar por reporte
        guardar = input(f"\n{Fore.YELLOW}¿Desea guardar un reporte en TXT? (s/n): {Fore.RESET}").strip().lower()
        if guardar == 's':
            guardar_reporte("dominio", domain, report_lines)
            
        continuar = input(f"\n{Fore.YELLOW}¿Desea comprobar otro dominio? (s/n): {Fore.RESET}")
        if continuar.lower() != 's':
            print(f"{Fore.GREEN}Saliendo del comprobador de dominio...{Fore.RESET}")
            break

if __name__ == "__main__":
    check_domain()
