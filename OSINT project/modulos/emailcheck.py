import requests
from colorama import init, Fore, Style

init(autoreset=True)

API_KEY = "d78efc77513878de2402730333c89dde09d91622"

def emailbuscar(email):
    url = "https://leakcheck.io/api/public"
    params = {"key": API_KEY, "check": email}
    try:
        resp = requests.get(url, params=params)
        if resp.status_code == 200:
            datos = resp.json()
            if datos.get("found"):
                print(f"{Fore.GREEN}[+] El email {email} aparece en brechas.{Fore.RESET}")
            else:
                print(f"{Fore.YELLOW}[-] El email {email} NO aparece en brechas.{Fore.RESET}")
        else:
            print(f"{Fore.RED}Error al consultar LeakCheck API. Código: {resp.status_code}{Fore.RESET}")
    except requests.RequestException as e:
        print(f"{Fore.RED}Error de red: {e}{Fore.RESET}")

if __name__ == "__main__":
    email = input(f"{Fore.YELLOW}Ingrese un email: {Fore.RESET}")
    emailbuscar(email)
