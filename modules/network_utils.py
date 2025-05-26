import requests
from colorama import Fore, Style, init
init(autoreset=True)

# Constantes de couleurs
SUCCESS_COLOR = Fore.GREEN + Style.BRIGHT
INFO_COLOR = Fore.BLUE + Style.BRIGHT
WARNING_COLOR = Fore.YELLOW + Style.BRIGHT
ERROR_COLOR = Fore.RED + Style.BRIGHT
NORMAL_TEXT_COLOR = Fore.WHITE + Style.NORMAL

def print_colored(message, color=INFO_COLOR):
    """Affiche un message coloré dans la console."""
    print(color + message + Style.RESET_ALL)

class NetworkUtils:
    def make_get_request(self, url, params=None, headers=None):
        """Exécute une requête GET et affiche la réponse."""
        print_colored(f"\n[GET] Requête à : {url}", INFO_COLOR)
        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)
            print_colored(f"Statut : {response.status_code}", INFO_COLOR)
            print_colored(f"Taille de la réponse : {len(response.text)} octets", INFO_COLOR)
            print_colored("Contenu de la réponse (premiers 500 caractères) :", NORMAL_TEXT_COLOR)
            print_colored(response.text[:500] + "...", NORMAL_TEXT_COLOR)
            return response
        except requests.exceptions.RequestException as e:
            print_colored(f"Erreur réseau ou requête : {e}", ERROR_COLOR)
            return None
        except Exception as e:
            print_colored(f"Une erreur inattendue est survenue : {e}", ERROR_COLOR)
            return None

    def make_post_request(self, url, data=None, json_data=None, headers=None):
        """Exécute une requête POST et affiche la réponse."""
        print_colored(f"\n[POST] Requête à : {url}", INFO_COLOR)
        try:
            response = requests.post(url, data=data, json=json_data, headers=headers, timeout=10)
            print_colored(f"Statut : {response.status_code}", INFO_COLOR)
            print_colored(f"Taille de la réponse : {len(response.text)} octets", INFO_COLOR)
            print_colored("Contenu de la réponse (premiers 500 caractères) :", NORMAL_TEXT_COLOR)
            print_colored(response.text[:500] + "...", NORMAL_TEXT_COLOR)
            return response
        except requests.exceptions.RequestException as e:
            print_colored(f"Erreur réseau ou requête : {e}", ERROR_COLOR)
            return None
        except Exception as e:
            print_colored(f"Une erreur inattendue est survenue : {e}", ERROR_COLOR)
            return None

    def download_file(self, url, destination_path):
        """Télécharge un fichier depuis une URL vers un chemin de destination."""
        print_colored(f"\n[DOWNLOAD] Téléchargement de '{url}' vers '{destination_path}'...", INFO_COLOR)
        try:
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()  # Lève une exception pour les codes d'état HTTP erreurs
            with open(destination_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print_colored(f"Fichier téléchargé et sauvegardé avec succès dans '{destination_path}'.", SUCCESS_COLOR)
            return True
        except requests.exceptions.RequestException as e:
            print_colored(f"Erreur lors du téléchargement : {e}", ERROR_COLOR)
            return False
        except Exception as e:
            print_colored(f"Une erreur inattendue est survenue lors du téléchargement : {e}", ERROR_COLOR)
            return False

    def scan_ports(self, target_host, ports):
        """Scanne une liste de ports sur un hôte cible."""
        print_colored(f"Scan de ports sur {target_host}...", INFO_COLOR)
        open_ports = []
        try:
            # Importation locale pour éviter les dépendances circulaires au niveau global si NetworkUtils est importé ailleurs
            import socket 
            
            for port in ports:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1) # Timeout de 1 seconde
                result = sock.connect_ex((target_host, port))
                if result == 0:
                    print_colored(f"  Port {port}: Ouvert", SUCCESS_COLOR)
                    open_ports.append(port)
                else:
                    # print_colored(f"  Port {port}: Fermé/Filtré", NORMAL_TEXT_COLOR) # Optionnel: afficher les ports fermés
                    pass
                sock.close()
            
            if open_ports:
                print_colored(f"\nPorts ouverts trouvés sur {target_host}: {open_ports}", SUCCESS_COLOR)
            else:
                print_colored(f"Aucun port ouvert trouvé sur {target_host} dans la plage spécifiée.", WARNING_COLOR)
            return open_ports

        except socket.gaierror:
            print_colored(f"Erreur: Nom d'hôte impossible à résoudre : '{target_host}'.", ERROR_COLOR)
            return None
        except socket.error as e:
            print_colored(f"Erreur de socket : {e}", ERROR_COLOR)
            return None
        except Exception as e:
            print_colored(f"Une erreur inattendue est survenue lors du scan de ports : {e}", ERROR_COLOR)
            return None


