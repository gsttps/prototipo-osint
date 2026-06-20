import requests
from colorama import init, Fore #para colorear la salida en consola

init(autoreset=True)

#diccionario rancio de las plataformas donde buscar el user
PLATAFORMAS = {
    "GitHub": "https://github.com/{}",
    "Twitter": "https://twitter.com/{}",
    "Instagram": "https://www.instagram.com/{}/",
    "Reddit": "https://www.reddit.com/user/{}",
    "TikTok": "https://www.tiktok.com/@{}",
    "Steam": "https://steamcommunity.com/id/{}",
    "Canva": "https://www.canva.com/{}/",
    "Xbox": "https://account.xbox.com/en-us/profile?gamertag={}",
    "PlayStation": "https://my.playstation.com/profile/{}",
    "Twitch": "https://www.twitch.tv/{}",
    "Facebook": "https://www.facebook.com/{}",
    #se pueden agregar mas plataformas, no se me ocurrieron mas xd
}

def check_username():
    while True:
        print(f"\n{Fore.CYAN}=== BUSCAR NOMBRE DE USUARIO ==={Fore.RESET}")
        user = input(f'{Fore.YELLOW}Ingrese usuario a buscar (o \'salir\' para volver): {Fore.RESET}').strip()
        if user.lower() == 'salir':
            break
        if not user:
            continue
        print(f'{Fore.CYAN}\nBuscando usuario: {user}\n{Fore.RESET}')
        
        for plataforma, url_patron in PLATAFORMAS.items():
            try:
                url = url_patron.format(user)
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    print(f'{Fore.GREEN}Usuario encontrado en {plataforma}: {url}{Fore.RESET}')
                elif response.status_code == 404:
                    print(f'{Fore.RED}Usuario no encontrado en {plataforma}: {url}{Fore.RESET}')
                else:
                    print(f'{Fore.YELLOW}Error al buscar en {plataforma}: {url} (Status code: {response.status_code}){Fore.RESET}')
            except requests.RequestException as e:
                print(f"{Fore.MAGENTA}[!] {plataforma}: Error → {e}")
        
        continuar = input(f'{Fore.YELLOW}¿Desea buscar otro usuario? (s/n): {Fore.RESET}')
        if continuar.lower() != 's':
            print(f'{Fore.GREEN}Saliendo del buscador de usuario...{Fore.RESET}')
            break

if __name__ == "__main__":
    check_username()