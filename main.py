from colorama import init, Fore
init(autoreset=True)

def menu():
    print(Fore.CYAN + "----------------------------------------")
    print(Fore.CYAN + "Prototipo de herramienta basica de OSINT")
    print(Fore.CYAN + "----------------------------------------")
    print(Fore.LIGHTCYAN_EX + '1. Comprobar correo e-mail')
    print(Fore.LIGHTCYAN_EX + '2. Ver datos de una IP')
    print(Fore.LIGHTCYAN_EX + '3. Buscar nombre de usuario')
    print(Fore.LIGHTCYAN_EX + '4. Comprobar un dominio') #PENDIENTEEEEEE 
    print(Fore.LIGHTCYAN_EX + '5. Salir')
    
def main():
    while True:
        opcion = input(Fore.YELLOW + 'Selecciona una opcion: ')
        if opcion == '1':
            from modulos import emailcheck
        elif opcion == '2':
            from modulos import IP
        elif opcion == '3':
            from modulos import userfinder
        elif opcion == '4':
            print(Fore.RED + 'Esta opcion esta pendiente de implementacion')
        elif opcion == '5':
            print(Fore.GREEN + 'Saliendo...')
            break

menu()
if __name__ == "__main__":
    main()