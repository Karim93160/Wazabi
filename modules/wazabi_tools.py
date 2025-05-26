import os
import time
import string
import random
import sys
from colorama import Fore, Style, init
init(autoreset=True)

# Constantes de couleurs
SUCCESS_COLOR = Fore.GREEN + Style.BRIGHT
INFO_COLOR = Fore.BLUE + Style.BRIGHT
WARNING_COLOR = Fore.YELLOW + Style.BRIGHT
ERROR_COLOR = Fore.RED + Style.BRIGHT
WAZABI_COLOR = Fore.MAGENTA + Style.BRIGHT
NORMAL_TEXT_COLOR = Fore.WHITE + Style.NORMAL

def print_colored(message, color=INFO_COLOR):
    """Affiche un message coloré dans la console."""
    print(color + message + Style.RESET_ALL)

class WazabiTools:
    def __init__(self, network_utils, file_manager):
        self.network_utils = network_utils
        self.file_manager = file_manager
        # Import local pour éviter les dépendances circulaires au niveau global si security_utils importe WazabiTools
        from .security_utils import SecurityUtils
        self.security_utils = SecurityUtils()

    def port_scan_wrapper(self, host, ports_str):
        """Wrapper pour appeler le scan de ports depuis NetworkUtils, avec gestion des arguments."""
        # Les ports peuvent être une liste (80,443) ou une plage (1-100)
        ports = []
        if '-' in str(ports_str):
            start, end = map(int, ports_str.split('-'))
            ports = list(range(start, end + 1))
        elif ',' in str(ports_str):
            ports = [int(p) for p in ports_str.split(',') if p.strip().isdigit()]
        elif str(ports_str).strip().isdigit():
            ports = [int(ports_str)]
        
        if not ports:
            print_colored("Erreur: Format de ports invalide. Utilisez '80,443' ou '1-100'.", ERROR_COLOR)
            return

        print_colored(f"\n[Wazabi] Démarrage du scan de ports sur {host} pour les ports {ports_str}...", WAZABI_COLOR)
        self.network_utils.scan_ports(host, ports)
        print_colored(f"[Wazabi] Scan de ports terminé pour {host}.", WAZABI_COLOR)

    def analyze_dir_deep(self, directory, sensitive_extensions=None, min_size_mb=10, output_file=None):
        """
        Analyse un répertoire pour trouver des fichiers sensibles, grands ou spécifiques.
        """
        print_colored(f"\n[Wazabi] Démarrage de l'analyse approfondie du répertoire : {directory}", WAZABI_COLOR)
        if not os.path.isdir(directory):
            print_colored(f"Erreur: Le répertoire '{directory}' n'existe pas ou n'est pas accessible.", ERROR_COLOR)
            return

        results = {
            "large_files": [],
            "sensitive_files": [],
            "total_files": 0,
            "total_size_mb": 0.0
        }

        min_size_bytes = min_size_mb * 1024 * 1024

        for root, _, files in os.walk(directory):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                results["total_files"] += 1
                try:
                    file_size = os.path.getsize(file_path)
                    results["total_size_mb"] += file_size / (1024 * 1024)

                    if file_size > min_size_bytes:
                        results["large_files"].append({"path": file_path, "size_mb": file_size / (1024 * 1024)})
                    
                    if sensitive_extensions:
                        _, ext = os.path.splitext(file_name)
                        if ext.lower() in [s.lower() for s in sensitive_extensions]:
                            results["sensitive_files"].append({"path": file_path, "extension": ext})

                except Exception as e:
                    print_colored(f"Avertissement: Impossible d'accéder à {file_path} ({e})", WARNING_COLOR)

        print_colored(f"Analyse terminée. Total fichiers: {results['total_files']}, Taille totale: {results['total_size_mb']:.2f} MB", INFO_COLOR)
        
        if results['large_files']:
            print_colored("--- Fichiers volumineux trouvés (taille > %.2f MB) ---" % min_size_mb, WAZABI_COLOR)
            for f in results['large_files']:
                print_colored(f"  - {f['path']} ({f['size_mb']:.2f} MB)", NORMAL_TEXT_COLOR)
        
        if results['sensitive_files']:
            print_colored("--- Fichiers sensibles trouvés ---", WAZABI_COLOR)
            for f in results['sensitive_files']:
                print_colored(f"  - {f['path']} (Extension: {f['extension']})", NORMAL_TEXT_COLOR)

        if output_file:
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(f"Analyse du répertoire : {directory}\n")
                    f.write(f"Total fichiers : {results['total_files']}\n")
                    f.write(f"Taille totale : {results['total_size_mb']:.2f} MB\n\n")
                    if results['large_files']:
                        f.write("Fichiers volumineux (taille > %.2f MB) :\n" % min_size_mb)
                        for f in results['large_files']:
                            f.write(f"  - {f['path']} ({f['size_mb']:.2f} MB)\n")
                        f.write("\n")
                    if results['sensitive_files']:
                        f.write("Fichiers sensibles :\n")
                        for f in results['sensitive_files']:
                            f.write(f"  - {f['path']} (Extension: {f['extension']})\n")
                        f.write("\n")
                print_colored(f"Résultats de l'analyse sauvegardés dans '{output_file}'.", SUCCESS_COLOR)
            except Exception as e:
                print_colored(f"Erreur lors de la sauvegarde des résultats dans '{output_file}': {e}", ERROR_COLOR)

    def generate_payload_text(self, length=16, charset='alphanum_special', num_lines=1, prefix='', suffix=''):
        """Génère des payloads textuels pour des tests de fuzzing ou d'injection."""
        charsets = {
            'alphanum_special': string.ascii_letters + string.digits + string.punctuation,
            'alpha': string.ascii_letters,
            'num': string.digits,
            'special': string.punctuation,
            'whitespace': string.whitespace
        }
        
        if charset not in charsets:
            print_colored(f"Erreur: Le jeu de caractères '{charset}' n'est pas valide. Utilisez un des suivants: {', '.join(charsets.keys())}.", ERROR_COLOR)
            return None
        
        generated_payloads = []
        for _ in range(num_lines):
            payload = ''.join(random.choice(charsets[charset]) for _ in range(length))
            generated_payloads.append(prefix + payload + suffix)
        
        if num_lines == 1:
            print_colored(f"Payload généré: {generated_payloads[0]}", SUCCESS_COLOR)
            return generated_payloads[0]
        else:
            print_colored(f"Génération de {num_lines} payloads:", SUCCESS_COLOR)
            for p in generated_payloads:
                print_colored(f"  - {p}", NORMAL_TEXT_COLOR)
            return generated_payloads

    def dictionary_attack(self, target_hash, wordlist_path, hash_algorithm='sha256'):
        """
        Tente de trouver le mot de passe original d'un hachage en utilisant une attaque par dictionnaire.
        """
        print_colored(f"\n[Wazabi] Démarrage de l'attaque par dictionnaire sur le hachage '{target_hash}' avec la wordlist '{wordlist_path}'...", WAZABI_COLOR)
        print_colored(f"[Wazabi] Algorithme de hachage ciblé : {hash_algorithm}", WAZABI_COLOR)

        if not os.path.isfile(wordlist_path):
            print_colored(f"Erreur: Le fichier de wordlist '{wordlist_path}' est introuvable. Veuillez vérifier le chemin.", ERROR_COLOR)
            return None

        found_password = None
        start_time = time.time()
        attempt_count = 0

        try:
            with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    attempt_count += 1
                    word = line.strip()
                    if not word: # Skip empty lines
                        continue
                    
                    if self.security_utils.check_hash(word, target_hash, hash_algorithm):
                        found_password = word
                        break
                    
                    if attempt_count % 10000 == 0:
                        sys.stdout.write(f"\r{WARNING_COLOR}[Wazabi] Testé {attempt_count} mots...{Style.RESET_ALL}")
                        sys.stdout.flush()

            end_time = time.time()
            elapsed_time = end_time - start_time

            sys.stdout.write(f"\r{INFO_COLOR}[Wazabi] Attaque par dictionnaire terminée. {attempt_count} mots testés en {elapsed_time:.2f} secondes.{Style.RESET_ALL}\n")
            sys.stdout.flush()

            if found_password:
                print_colored(f"{SUCCESS_COLOR}[Wazabi] Mot de passe trouvé : '{found_password}'", SUCCESS_COLOR)
                return found_password
            else:
                print_colored(f"{WARNING_COLOR}[Wazabi] Mot de passe non trouvé dans la wordlist. Persévérez !", WARNING_COLOR)
                return None

        except Exception as e:
            print_colored(f"Erreur inattendue lors de l'attaque par dictionnaire: {e}", ERROR_COLOR)
            return None


