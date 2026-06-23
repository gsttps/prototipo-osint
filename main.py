"""
esta wea ira mejorando con el tiempo
la idea es llegar a hacerlo funcional y que sea util para ejecutar en windows y linux
los import los puse en los if pq si los ponia junto con el import de la libreria del colorama (o la q se agregue despues) queda la caga y no aparece el menu (sera un bug? pero funciona asi q btw)
"""

from colorama import init, Fore
from modulos.emailcheck import check_email
from modulos.IP import check_ip
from modulos.userfinder import check_username
from modulos.ver_dominio import check_domain
from modulos.portscanner import scan_ports

init(autoreset=True)  # este init es para que funcionen los colores


def menu():
    print(Fore.CYAN + "----------------------------------------")
    print(Fore.CYAN + "Prototipo de herramienta basica de OSINT")
    print(Fore.CYAN + "----------------------------------------")
    print(Fore.LIGHTCYAN_EX + "1. Comprobar correo e-mail")
    print(Fore.LIGHTCYAN_EX + "2. Ver datos de una IP")
    print(Fore.LIGHTCYAN_EX + "3. Buscar nombre de usuario")
    print(Fore.LIGHTCYAN_EX + "4. Comprobar un dominio")
    print(Fore.LIGHTCYAN_EX + "5. Escaneo de puertos")
    print(Fore.LIGHTCYAN_EX + "6. Salir")


def main():
    while True:
        menu()
        opcion = input(Fore.YELLOW + "Selecciona una opcion: ")
        if opcion == "1":
            check_email()
        elif opcion == "2":
            check_ip()
        elif opcion == "3":
            check_username()
        elif opcion == "4":
            check_domain()
        elif opcion == "5":
            scan_ports()
        elif opcion == "6":
            print(Fore.GREEN + "Saliendo...")
            break
        else:
            print(Fore.RED + "Opcion no valida, intente nuevamente.")


if __name__ == "__main__":
    main()
# 
