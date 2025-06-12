'''
esta wea ira mejorando con el tiempo
la idea es llegar a hacerlo funcional y que sea util para ejecutar en windows y linux
los import los puse en los if pq si los ponia junto con el import de la libreria del colorama (o la q se agregue despues) queda la caga y no aparece el menu (sera un bug? pero funciona asi q btw)
'''
#se usa ''' para encerrar comentarios mas largos, muy bueno

from colorama import init, Fore
init(autoreset=True)  #este init es para que funcionen los colores, en resumen

def menu():
    print(Fore.CYAN + "Prototipo de herramienta basica de OSINT")
    print(Fore.LIGHTCYAN_EX + '1. Comprobar correo e-mail') #el del email funciona como las weas, pendiente arreglar
    print(Fore.LIGHTCYAN_EX + '2. Ver datos de una IP')
    print(Fore.LIGHTCYAN_EX + '3. Buscar nombre de usuario')
    print(Fore.LIGHTCYAN_EX + '4. Comprobar un dominio') #PENDIENTEEEEEE
    print(Fore.LIGHTCYAN_EX + '4. Escaneo de puertos') #pendente
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
