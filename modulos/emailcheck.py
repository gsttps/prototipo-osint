import requests
from colorama import init, Fore, Style

init(autoreset=True)

try:
    from modulos.reporter import guardar_reporte
except ImportError:
    from reporter import guardar_reporte

def emailbuscar(email):
    url = "https://leakcheck.io/api/public"
    params = {"check": email}
    report_lines = []
    try:
        msg_start = f"Consultando LeakCheck API para: {email}..."
        print(f"{Fore.CYAN}{msg_start}{Fore.RESET}")
        report_lines.append(msg_start)
        
        resp = requests.get(url, params=params)
        if resp.status_code == 200:
            datos = resp.json()
            if datos.get("success"):
                found_count = datos.get("found", 0)
                if found_count > 0:
                    msg_found = f"[+] ¡ATENCIÓN! El email {email} aparece en {found_count} filtraciones de datos."
                    print(f"\n{Fore.GREEN}{msg_found}{Fore.RESET}")
                    report_lines.append(msg_found)
                    
                    # Mostrar campos filtrados
                    fields = datos.get("fields", [])
                    if fields:
                        msg_fields = f"Campos expuestos: {', '.join(fields)}"
                        print(f"{Fore.CYAN}{msg_fields}{Fore.RESET}")
                        report_lines.append(msg_fields)
                    
                    # Mostrar fuentes/filtraciones (limitado a las primeras 15 en pantalla, pero guardamos todas en el reporte!)
                    sources = datos.get("sources", [])
                    if sources:
                        print(f"\n{Fore.CYAN}Fuentes de filtración (mostrando hasta 15 en pantalla):{Fore.RESET}")
                        report_lines.append("\nFUENTES DE FILTRACIÓN COMPLETAS:")
                        
                        limit = 15
                        for i, src in enumerate(sources):
                            name = src.get("name", "Desconocido")
                            date = src.get("date", "Fecha no disponible")
                            date_str = f" ({date})" if date else ""
                            line_content = f" - {name}{date_str}"
                            
                            # Imprimir en consola hasta el límite
                            if i < limit:
                                print(f" {Fore.RED}- {name}{Fore.LIGHTBLACK_EX}{date_str}{Fore.RESET}")
                            
                            # Guardar todo en el reporte
                            report_lines.append(line_content)
                        
                        if len(sources) > limit:
                            print(f" {Fore.YELLOW}... y {len(sources) - limit} fuentes más.{Fore.RESET}")
                            report_lines.append(f"... y {len(sources) - limit} fuentes más.")
                else:
                    msg_not = f"[-] El email {email} NO aparece en ninguna filtración conocida."
                    print(f"{Fore.GREEN}{msg_not}{Fore.RESET}")
                    report_lines.append(msg_not)
            else:
                msg_err = f"LeakCheck reportó un problema: {datos.get('error', 'Error desconocido')}"
                print(f"{Fore.RED}{msg_err}{Fore.RESET}")
                report_lines.append(msg_err)
        else:
            msg_err = f"Error al consultar LeakCheck API. Código: {resp.status_code}"
            print(f"{Fore.RED}{msg_err}{Fore.RESET}")
            report_lines.append(msg_err)
    except requests.RequestException as e:
        msg_err = f"Error de red: {e}"
        print(f"{Fore.RED}{msg_err}{Fore.RESET}")
        report_lines.append(msg_err)
        
    return report_lines

def check_email():
    while True:
        print(f"\n{Fore.CYAN}=== COMPROBACIÓN DE CORREO E-MAIL ==={Fore.RESET}")
        email = input(f"{Fore.YELLOW}Ingrese un email a buscar (o 'salir' para volver): {Fore.RESET}").strip()
        if not email:
            continue
        if email.lower() == 'salir':
            break
        report_lines = emailbuscar(email)
        
        if report_lines:
            guardar = input(f"\n{Fore.YELLOW}¿Desea guardar un reporte en TXT? (s/n): {Fore.RESET}").strip().lower()
            if guardar == 's':
                guardar_reporte("emailcheck", email, report_lines)

if __name__ == "__main__":
    check_email()
