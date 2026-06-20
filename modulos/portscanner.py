import socket
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import init, Fore, Style

init(autoreset=True)

COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    115: "SFTP",
    135: "RPC",
    139: "NetBIOS",
    143: "IMAP",
    443: "HTTPS",
    445: "Microsoft-DS (SMB)",
    993: "IMAPS",
    995: "POP3S",
    1433: "MSSQL",
    3306: "MySQL",
    3389: "RDP",
    5900: "VNC",
    8080: "HTTP-Alt",
    8443: "HTTPS-Alt"
}

def scan_single_port(ip, port):
    try:
        # Usar AF_INET (IPv4) y SOCK_STREAM (TCP)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.6)  # Timeout corto pero razonable para evitar falsos negativos
        result = s.connect_ex((ip, port))
        s.close()
        if result == 0:
            # Intentar obtener nombre de servicio
            service = COMMON_PORTS.get(port)
            if not service:
                try:
                    service = socket.getservbyport(port, "tcp").upper()
                except OSError:
                    service = "Desconocido"
            return port, True, service
        return port, False, None
    except Exception:
        return port, False, None

def run_port_scan(target_ip, ports_to_scan):
    print(f"\n{Fore.CYAN}Iniciando escaneo de {len(ports_to_scan)} puertos en {Fore.YELLOW}{target_ip}{Fore.CYAN} con 100 hilos paralelos...{Fore.RESET}")
    open_ports = []
    
    # ThreadPoolExecutor para escaneo super rápido y concurrente
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = {executor.submit(scan_single_port, target_ip, port): port for port in ports_to_scan}
        for future in as_completed(futures):
            port, is_open, service = future.result()
            if is_open:
                open_ports.append((port, service))
                print(f" {Fore.GREEN}[+] Puerto {port:5d} - Abierto: {Fore.YELLOW}{service}{Fore.RESET}")
                
    print(f"\n{Fore.CYAN}Escaneo completado.{Fore.RESET}")
    if open_ports:
        print(f"{Fore.GREEN}Puertos abiertos encontrados ({len(open_ports)}): {', '.join(str(p[0]) for p in sorted(open_ports))}{Fore.RESET}")
    else:
        print(f"{Fore.YELLOW}No se encontraron puertos abiertos en el rango escaneado.{Fore.RESET}")

def scan_ports():
    while True:
        print(f"\n{Fore.CYAN}=== ESCANEO DE PUERTOS ==={Fore.RESET}")
        target = input(f"{Fore.YELLOW}Ingrese IP o dominio a escanear (o 'salir' para volver): {Fore.RESET}").strip()
        if not target:
            continue
        if target.lower() == 'salir':
            break
        
        # Limpieza básica por si ponen http/https/www
        if target.startswith("http://"):
            target = target[7:]
        elif target.startswith("https://"):
            target = target[8:]
        if target.startswith("www."):
            target = target[4:]
        target = target.split("/")[0]

        # Resolver host a IP
        try:
            print(f"{Fore.CYAN}Resolviendo host: {Fore.YELLOW}{target}...")
            target_ip = socket.gethostbyname(target)
            print(f"{Fore.GREEN}[+] Host resuelto con éxito: {Fore.YELLOW}{target_ip}{Fore.RESET}")
        except socket.gaierror:
            print(f"{Fore.RED}Error: No se pudo resolver el host '{target}'{Fore.RESET}")
            continue

        print(f"\n{Fore.CYAN}Seleccione puertos a escanear:")
        print(f"1. Puertos comunes ({len(COMMON_PORTS)} puertos de servicios estándar)")
        print(f"2. Rango de puertos personalizado (ej: 1-1024)")
        print(f"3. Lista de puertos específicos (ej: 80, 443, 8080)")
        
        opc = input(f"{Fore.YELLOW}Seleccione opción (1/2/3): {Fore.RESET}").strip()
        
        ports_to_scan = []
        if opc == '1':
            ports_to_scan = sorted(list(COMMON_PORTS.keys()))
        elif opc == '2':
            rango = input(f"{Fore.YELLOW}Ingrese rango (ej: 1-1024): {Fore.RESET}").strip()
            try:
                start, end = map(int, rango.split("-"))
                if start < 1 or end > 65535 or start > end:
                    raise ValueError
                ports_to_scan = list(range(start, end + 1))
            except ValueError:
                print(f"{Fore.RED}Rango inválido. Se cancela el escaneo.{Fore.RESET}")
                continue
        elif opc == '3':
            lista_str = input(f"{Fore.YELLOW}Ingrese puertos separados por coma (ej: 80,443,8080): {Fore.RESET}").strip()
            try:
                ports_to_scan = [int(p.strip()) for p in lista_str.split(",") if p.strip()]
                # Filtrar puertos inválidos
                ports_to_scan = [p for p in ports_to_scan if 1 <= p <= 65535]
                if not ports_to_scan:
                    raise ValueError
            except ValueError:
                print(f"{Fore.RED}Lista de puertos inválida. Se cancela el escaneo.{Fore.RESET}")
                continue
        else:
            print(f"{Fore.RED}Opción inválida. Se cancela el escaneo.{Fore.RESET}")
            continue

        run_port_scan(target_ip, ports_to_scan)
        
        continuar = input(f"\n{Fore.YELLOW}¿Desea escanear otro host? (s/n): {Fore.RESET}")
        if continuar.lower() != 's':
            print(f"{Fore.GREEN}Saliendo del escáner de puertos...{Fore.RESET}")
            break

if __name__ == "__main__":
    scan_ports()
