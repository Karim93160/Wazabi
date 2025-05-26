import argparse
import sys
import os
import json
import logging
import time
from datetime import datetime
from colorama import init, Fore, Style

# Initialisation de Colorama pour les couleurs dans le terminal
init(autoreset=True)

# --- 1. Configuration de la Journalisation (Logging) ---
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, f"wazabi_shell_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("WazabiShell")

# --- Constantes pour les couleurs du shell ---
SUCCESS_COLOR = Fore.GREEN + Style.BRIGHT
INFO_COLOR = Fore.BLUE + Style.BRIGHT
WARNING_COLOR = Fore.YELLOW + Style.BRIGHT
ERROR_COLOR = Fore.RED + Style.BRIGHT
PROMPT_COLOR = Fore.CYAN + Style.BRIGHT
WAZABI_COLOR = Fore.MAGENTA + Style.BRIGHT
NORMAL_TEXT_COLOR = Fore.WHITE + Style.NORMAL

# --- Fonctions utilitaires génériques ---
def print_colored(message, color=INFO_COLOR):
    """Affiche un message coloré dans la console."""
    print(color + message + Style.RESET_ALL)

def load_banner(banner_path):
    """Charge et retourne le contenu de la bannière."""
    try:
        with open(banner_path, 'r', encoding='utf-8') as f:
            return f.readlines()
    except FileNotFoundError:
        logger.error(f"Fichier de bannière introuvable : {banner_path}")
        return ["--- Wazabi Shell ---", "Banner not found!"]
    except Exception as e:
        logger.exception(f"Erreur lors du chargement de la bannière : {e}")
        return ["--- Wazabi Shell ---", f"Error loading banner: {e}"]


def display_animated_banner(banner_lines):
    """Affiche la bannière avec une animation simple et des couleurs thématiques."""
    # Correction pour effacer l'écran : utiliser des codes ANSI directement pour plus de compatibilité
    # Cela devrait contourner les problèmes de permission avec 'os.system' et les commandes 'clear'/'cls'.
    sys.stdout.write("\033[H\033[J") # Efface l'écran et place le curseur en haut à gauche
    sys.stdout.flush()

    colors = [Fore.GREEN, Fore.CYAN, Fore.MAGENTA, Fore.BLUE, Fore.YELLOW]
    
    # Nous n'avons plus besoin de terminal_width pour tronquer, mais nous la gardons pour la clarté de la ligne.
    # La ligne clear_line est toujours utile pour effacer la ligne avant d'écrire la suivante.
    try:
        terminal_width = os.get_terminal_size().columns
    except OSError:
        terminal_width = 80 # Valeur par défaut si la taille n'est pas détectée

    # La chaîne clear_line doit effacer jusqu'à la fin de la ligne, quelle que soit la longueur de la ligne précédente
    clear_line = "\r" + " " * terminal_width + "\r" 

    print("\n" * 2) # Espace avant la bannière

    for i, line in enumerate(banner_lines):
        colored_line = ""
        for j, char in enumerate(line):
            color = colors[(j + i) % len(colors)] # Cycle les couleurs
            colored_line += color + char
        
        # NE PAS TRONQUER : Affiche la ligne entière, même si elle dépasse la largeur du terminal.
        # Le terminal gérera le retour à la ligne automatiquement si la ligne est trop longue.
        display_line = colored_line.rstrip() 

        # Utilise clear_line pour effacer la ligne avant d'écrire la nouvelle ligne colorée
        sys.stdout.write(clear_line + display_line + Style.RESET_ALL + "\n") # Ajoute un retour chariot pour chaque ligne
        sys.stdout.flush()
        time.sleep(0.02) # Petite pause pour l'effet d'animation
    print("\n" * 2) # Espace après la bannière
    print_colored(f"{WAZABI_COLOR}        L'outil Pimenté pour le Hacker Éthique !", WAZABI_COLOR)
    print_colored(f"{WAZABI_COLOR}        Protection, Connaissance, Innovation.", WAZABI_COLOR)
    print_colored(f"{WAZABI_COLOR}--------------------------------------------------", WAZABI_COLOR)
    time.sleep(0.5)




def show_help():
    """Affiche l'aide globale du shell."""
    print_colored("\n--- Aide de Wazabi Shell ---", PROMPT_COLOR)
    print_colored("Bienvenue, Gardien des Bits Éthiques !", INFO_COLOR)
    print_colored("Naviguez dans les modules avec sagesse et précision :", INFO_COLOR)
    print_colored("  file    - Gestion des flux de données (copy, move, delete, list, find)", NORMAL_TEXT_COLOR)
    print_colored("  network - Maîtrise des échanges réseau (get, post, download, scan_ports)", NORMAL_TEXT_COLOR)
    print_colored("  data    - Traitement et transformation des informations (read_csv, write_csv, read_json, write_json, process_text)", NORMAL_TEXT_COLOR)
    print_colored("  db      - Interaction avec le savoir stocké (add_url, list_urls, execute_sql)", NORMAL_TEXT_COLOR)
    print_colored("  security- Art de la discrétion et de la robustesse (hash, encode_base64, decode_base64, generate_password, check_hash)", NORMAL_TEXT_COLOR)
    print_colored("  wazabi  - Les outils 'Pimentés' pour l'exploration avancée (port_scan, analyze_dir, generate_payload, dict_attack)", WAZABI_COLOR)
    print_colored("  config  - Ajustement des paramètres pour une efficacité optimale (set, get, save, load)", NORMAL_TEXT_COLOR)
    print_colored("  help    - Pour la lumière sur les chemins obscurs (affiche cette aide ou l'aide d'un module).", NORMAL_TEXT_COLOR)
    print_colored("  exit    - Quitter la matrice en toute sécurité.", NORMAL_TEXT_COLOR)
    print_colored("----------------------------", PROMPT_COLOR)

# --- Fonctions d'Orchestration du Shell ---

class WazabiShell:
    def __init__(self):
        # Importation des modules
        from modules.file_manager import FileManager
        from modules.network_utils import NetworkUtils
        from modules.data_processor import DataProcessor
        from modules.db_manager import DBManager
        from modules.security_utils import SecurityUtils
        from modules.wazabi_tools import WazabiTools
        from modules.config_manager import ConfigManager

        # Instanciation des modules importés
        self.file_manager = FileManager()
        self.network_utils = NetworkUtils()
        self.data_processor = DataProcessor()
        self.db_manager = DBManager()
        self.security_utils = SecurityUtils()
        self.config_manager = ConfigManager()
        # WazabiTools dépend de network_utils, file_manager et security_utils
        self.wazabi_tools = WazabiTools(self.network_utils, self.file_manager)

        self.db_manager.connect() # Connexion à la DB au démarrage du shell

        self.commands = {
            "file": {
                "copy": self.file_manager.copy_item,
                "move": self.file_manager.move_item,
                "delete": self.file_manager.delete_item,
                "list": self.file_manager.list_directory,
                "find": self.file_manager.find_files,
            },
            "network": {
                "get": self.network_utils.make_get_request,
                "post": self.network_utils.make_post_request,
                "download": self.network_utils.download_file,
                "scan_ports": self.wazabi_tools.port_scan_wrapper, # Wazabi's port scanner
            },
            "data": {
                "read_csv": self.data_processor.read_csv,
                "write_csv": self.data_processor.write_csv,
                "read_json": self.data_processor.read_json,
                "write_json": self.data_processor.write_json,
                "process_text": self._process_text_file_wrapper, # Wrapper pour la logique fichier/contenu
            },
            "db": {
                "add_url": self.db_manager.add_processed_url,
                "list_urls": self.db_manager.get_processed_urls,
                "execute_sql": self.db_manager.execute_query,
            },
            "security": {
                "hash": self.security_utils.hash_string,
                "encode_base64": self.security_utils.encode_base64,
                "decode_base64": self.security_utils.decode_base64,
                "generate_password": self.security_utils.generate_password,
                "check_hash": self.security_utils.check_hash, # Ajout de la vérification de hash
            },
            "wazabi": {
                "analyze_dir": self.wazabi_tools.analyze_dir_deep,
                "generate_payload": self.wazabi_tools.generate_payload_text,
                "dict_attack": self.wazabi_tools.dictionary_attack,
            },
            "config": {
                "set": self.config_manager.set_setting,
                "get": self.config_manager.get_setting,
                "save": self.config_manager.save_config,
                "load": self.config_manager.load_config,
                "show": lambda: print_colored(json.dumps(self.config_manager.config_data, indent=2), INFO_COLOR)
            }
        }
        logger.info("WazabiShell initialisé avec toutes les commandes.")

    def _process_text_file_wrapper(self, source_path, output_path, operation):
        """Wrapper pour gérer le traitement de fichier texte dans l'interface interactive."""
        if not os.path.isfile(source_path):
            print_colored(f"Erreur: Fichier source '{source_path}' introuvable.", ERROR_COLOR)
            return False
        try:
            with open(source_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            processed_content = self.data_processor.process_text_content(content, operation)
            
            if output_path:
                with open(output_path, 'w', encoding='utf-8') as f_out:
                    f_out.write(processed_content)
                print_colored(f"Contenu traité écrit dans '{output_path}'.", SUCCESS_COLOR)
            else:
                print_colored(f"Contenu traité (pas de fichier de sortie) : \n{processed_content[:500]}...", INFO_COLOR)
            return True
        except Exception as e:
            logger.exception(f"Erreur lors du traitement du fichier texte '{source_path}': {e}")
            print_colored(f"Erreur lors du traitement du fichier texte: {e}", ERROR_COLOR)
            return False



    def run_command(self, command_parts):
        if not command_parts:
            return

        module_name = command_parts[0]
        if module_name == "exit":
            print_colored("Au revoir, Gardien Éthique ! Que tes audits soient fructueux.", SUCCESS_COLOR)
            return "exit"
        elif module_name == "help":
            if len(command_parts) > 1:
                self.show_module_help(command_parts[1])
            else:
                show_help()
            return

        if module_name not in self.commands:
            print_colored(f"Erreur: Module '{module_name}' non reconnu. Le chemin de la sagesse est ailleurs. Tapez 'help'.", ERROR_COLOR)
            return

        if len(command_parts) < 2:
            print_colored(f"Erreur: Commande manquante pour le module '{module_name}'. Cherchez la lumière : 'help {module_name}'.", ERROR_COLOR)
            return

        command_name = command_parts[1]
        if command_name not in self.commands[module_name]:
            print_colored(f"Erreur: Commande '{command_name}' non reconnue pour le module '{module_name}'. Explorez : 'help {module_name}'.", ERROR_COLOR)
            return

        # Tentative de parser les arguments directement pour les fonctions
        args_dict = {}
        i = 2
        while i < len(command_parts):
            arg = command_parts[i]
            if arg.startswith('-') or arg.startswith('--'):
                key = arg.lstrip('-')
                # Gérer les arguments sans valeur (flags comme --recursive)
                if i + 1 < len(command_parts) and not command_parts[i+1].startswith('-'):
                    value = command_parts[i+1]
                    # Tente de convertir en int ou float si possible
                    try:
                        value = int(value)
                    except ValueError:
                        try:
                            value = float(value)
                        except ValueError:
                            pass # Reste une chaîne
                    args_dict[key] = value
                    i += 2
                else: # Argument sans valeur (flag)
                    args_dict[key] = True
                    i += 1
            else:
                # Gérer les arguments positionnels pour 'config set' plus bas, sinon avertissement.
                print_colored(f"Avertissement: Argument inattendu ou mal formaté : '{arg}'. Ignoré. Concentrez-vous sur la syntaxe.", WARNING_COLOR)
                i += 1

        try:
            func = self.commands[module_name][command_name]

            # Gestion spéciale pour les commandes qui nécessitent un mapping spécifique
            if module_name == "file" and command_name == "copy":
                func(args_dict.get('s'), args_dict.get('d')) # -s pour source, -d pour destination
            elif module_name == "file" and command_name == "move":
                func(args_dict.get('s'), args_dict.get('d')) # -s pour source, -d pour destination
            elif module_name == "file" and command_name == "delete":
                func(args_dict.get('p')) # -p pour path
            elif module_name == "file" and command_name == "list":
                func(args_dict.get('p'), args_dict.get('recursive', False)) # -p pour path, --recursive
            elif module_name == "file" and command_name == "find":
                func(args_dict.get('d'), args_dict.get('pattern'), args_dict.get('extension'), args_dict.get('recursive', False)) # -d pour directory
            elif module_name == "network" and command_name == "get":
                func(args_dict.get('u'), args_dict.get('params'), args_dict.get('headers')) # -u pour url
            elif module_name == "network" and command_name == "post":
                func(args_dict.get('u'), args_dict.get('data'), args_dict.get('json'), args_dict.get('headers')) # -u pour url
            elif module_name == "network" and command_name == "download":
                func(args_dict.get('u'), args_dict.get('d')) # -u pour url, -d pour destination
            elif module_name == "network" and command_name == "scan_ports":
                func(args_dict.get('h', self.config_manager.get_setting("default_target_host")), args_dict.get('p', self.config_manager.get_setting("default_scan_ports"))) # -h pour host, -p pour ports
            elif module_name == "data" and command_name == "process_text":
                 func(args_dict.get('s'), args_dict.get('o'), args_dict.get('operation')) # -s pour source, -o pour output, --operation
            elif module_name == "db" and command_name == "add_url":
                func(args_dict.get('u'), args_dict.get('s'), datetime.now().isoformat()) # -u pour url, -s pour status
            elif module_name == "db" and command_name == "list_urls":
                func() # Pas d'arguments
            elif module_name == "db" and command_name == "execute_sql":
                func(args_dict.get('q')) # -q pour query
            elif module_name == "security" and command_name == "hash":
                func(args_dict.get('t'), args_dict.get('a', 'sha256')) # -t pour text, -a pour algorithm
            elif module_name == "security" and command_name == "encode_base64":
                func(args_dict.get('d')) # -d pour data
            elif module_name == "security" and command_name == "decode_base64":
                func(args_dict.get('d')) # -d pour data
            elif module_name == "security" and command_name == "generate_password":
                # 'no-digits' et 'no-special' sont des flags, s'ils existent dans args_dict, leur valeur est True
                # La fonction attend 'include_digits' et 'include_special' qui sont l'inverse.
                func(args_dict.get('l', 16), not args_dict.get('no-digits', False), not args_dict.get('no-special', False)) # -l pour length
            elif module_name == "security" and command_name == "check_hash":
                 func(args_dict.get('c'), args_dict.get('t'), args_dict.get('a', 'sha256')) # -c pour candidate, -t pour target, -a pour algo
            elif module_name == "wazabi" and command_name == "analyze_dir":
                # sensitive_extensions est une chaîne qui doit être splitée en liste
                func(args_dict.get('d'),
                     args_dict.get('sensitive_extensions').split(',') if isinstance(args_dict.get('sensitive_extensions'), str) else None,
                     args_dict.get('min_size_mb', 10),
                     args_dict.get('o')) # -d pour directory, -o pour output_file
            elif module_name == "wazabi" and command_name == "generate_payload":
                func(args_dict.get('l', self.config_manager.get_setting("default_payload_length")),
                     args_dict.get('charset', 'alphanum_special'),
                     args_dict.get('num_lines', 1),
                     args_dict.get('prefix', ''),
                     args_dict.get('suffix', '')) # -l pour length
            elif module_name == "wazabi" and command_name == "dict_attack":
                func(args_dict.get('h'), args_dict.get('w'), args_dict.get('a', 'sha256')) # -h pour hash, -w pour wordlist, -a pour algo
            elif module_name == "config" and command_name == "set":
                # La commande 'set' est un cas particulier où les arguments sont positionnels (clé, valeur)
                # et non des flags comme '-k' ou '--key'.
                if len(command_parts) >= 4 and not command_parts[2].startswith('-'):
                    key_to_set = command_parts[2]
                    value_to_set = ' '.join(command_parts[3:])
                    self.config_manager.set_setting(key_to_set, value_to_set)
                else:
                    print_colored("Erreur: Utilisation: config set <clé> <valeur> (précision requise).", ERROR_COLOR)
            elif module_name == "config" and command_name == "get":
                if len(command_parts) == 3:
                    value = self.config_manager.get_setting(command_parts[2])
                    print_colored(f"Paramètre '{command_parts[2]}' : {value}", INFO_COLOR)
                else:
                    print_colored("Erreur: Utilisation: config get <clé> (clarté nécessaire).", ERROR_COLOR)
            elif module_name == "config" and command_name == "save":
                self.config_manager.save_config()
            elif module_name == "config" and command_name == "load":
                self.config_manager.load_config()
            elif module_name == "config" and command_name == "show":
                # Utilise json.dumps pour afficher le contenu de la configuration de manière lisible
                print_colored(json.dumps(self.config_manager.config_data, indent=2), INFO_COLOR)
            else:
                # Cette branche est un filet de sécurité si une commande n'est pas explicitement mappée.
                print_colored(f"Erreur: Impossible d'exécuter la commande '{command_name}' du module '{module_name}'. Les arguments ne correspondent pas ou la commande n'est pas mappée correctement. Réexaminez votre approche.", ERROR_COLOR)
                logger.error(f"Mapping d'arguments échoué pour {module_name} {command_name} avec args: {args_dict}")

        except TypeError as te:
            print_colored(f"Erreur d'arguments: Vérifiez la syntaxe et les types pour '{module_name} {command_name}'. Le chemin est obscur. Détails: {te}", ERROR_COLOR)
            logger.exception(f"Erreur de type d'arguments pour {module_name} {command_name}")
            self.show_module_help(module_name)
        except Exception as e:
            print_colored(f"Erreur inattendue lors de l'exécution de la commande: {e}. Une force imprévue est intervenue.", ERROR_COLOR)
            logger.exception(f"Erreur inattendue lors de l'exécution de {module_name} {command_name}")







    def show_module_help(self, module_name):
        """Affiche l'aide pour un module spécifique, avec des couleurs thématiques."""
        help_text = {
            "file": f"""
            {NORMAL_TEXT_COLOR}--- Aide du module 'file' (Gestion des Flux) ---
            {NORMAL_TEXT_COLOR}file copy -s <source> -d <destination> : Copie un fichier/dossier, préservant l'intégrité.
            {NORMAL_TEXT_COLOR}file move -s <source> -d <destination> : Déplace un fichier/dossier, modifiant son chemin.
            {NORMAL_TEXT_COLOR}file delete -p <path>                  : Supprime un fichier/dossier, avec prudence.
            {NORMAL_TEXT_COLOR}file list -p <path> [--recursive]      : Catalogue le contenu d'un répertoire, pour la connaissance.
            {NORMAL_TEXT_COLOR}file find -d <directory> [--pattern <p>] [--extension <ext>] [--recursive] : Recherche des artefacts, pour l'investigation.
            """,
            "network": f"""
            {NORMAL_TEXT_COLOR}--- Aide du module 'network' (Maîtrise du Réseau) ---
            {NORMAL_TEXT_COLOR}network get -u <url> [--params '{{}}'] [--headers '{{}}'] : Requête HTTP GET, pour l'information.
            {NORMAL_TEXT_COLOR}network post -u <url> [--data 'key=val'] [--json '{{}}'] [--headers '{{}}'] : Requête HTTP POST, pour l'interaction.
            {NORMAL_TEXT_COLOR}network download -u <url> -d <destination> : Télécharge un fichier, avec permission.
            {WAZABI_COLOR}network scan_ports -h <host> -p <ports> : {WAZABI_COLOR}[Wazabi] Scan de ports, pour cartographier le terrain (ex: '80,443' ou '1-100'). Utilisez avec sagesse.
            """,
            "data": f"""
            {NORMAL_TEXT_COLOR}--- Aide du module 'data' (Traitement des Informations) ---
            {NORMAL_TEXT_COLOR}data read_csv -p <path>             : Lit un fichier CSV, pour la compréhension des données.
            {NORMAL_TEXT_COLOR}data write_csv -p <path> -j '[{{}}]' : Écrit un fichier CSV (JSON de données), pour l'organisation.
            {NORMAL_TEXT_COLOR}data read_json -p <path>            : Lit un fichier JSON, pour la structure.
            {NORMAL_TEXT_COLOR}data write_json -p <path> -d '{{}}' : Écrit un fichier JSON, pour la persistance.
            {NORMAL_TEXT_COLOR}data process_text -s <source_file> [-o <output_file>] [--operation <op>] : Transforme le texte (uppercase, lowercase, reverse, rot13).
            """,
            "db": f"""
            {NORMAL_TEXT_COLOR}--- Aide du module 'db' (Interaction avec le Savoir Stoché) ---
            {NORMAL_TEXT_COLOR}db add_url -u <url> -s <status> : Ajoute/met à jour une URL traitée, pour le suivi.
            {NORMAL_TEXT_COLOR}db list_urls                    : Liste toutes les URLs traitées, pour l'historique.
            {NORMAL_TEXT_COLOR}db execute_sql -q "SELECT * FROM my_table;" : Exécute une requête SQL brute, avec grande prudence !
            """,
            "security": f"""
            {NORMAL_TEXT_COLOR}--- Aide du module 'security' (Art de la Discrétion) ---
            {NORMAL_TEXT_COLOR}security hash -t <text> [-a <algorithm>] : Hache une chaîne (md5, sha256, sha512), pour l'intégrité.
            {NORMAL_TEXT_COLOR}security encode_base64 -d <data>         : Encode en Base64, pour le transport.
            {NORMAL_TEXT_COLOR}security decode_base64 -d <data>         : Décode du Base64, pour la révélation.
            {NORMAL_TEXT_COLOR}security generate_password [-l <length>] [--no-digits] [--no-special] : Génère un mot de passe robuste, pour la sécurité.
            {NORMAL_TEXT_COLOR}security check_hash -c <candidate> -t <target_hash> [-a <algorithm>] : Vérifie si un mot de passe correspond à un hachage cible.
            """,
            "wazabi": f"""
            {WAZABI_COLOR}--- Aide du module 'wazabi' (Piment Wazabi : Exploration Avancée) ---
            {WAZABI_COLOR}wazabi analyze_dir -d <directory> [--sensitive_extensions ".log,.conf"] [--min_size_mb <val>] [-o <output_file>] : Analyse approfondie d'un répertoire, à la recherche de traces.
            {WAZABI_COLOR}wazabi generate_payload -l <length> [--charset <charset>] [--num_lines <num>] [--prefix <pref>] [--suffix <suff>] : Génère des payloads textuels, pour les tests (fuzzing, injection).
                 Charsets: alphanum_special, alpha, num, special, whitespace.
            {WAZABI_COLOR}wazabi dict_attack -h <target_hash> -w <wordlist_path> [--algo <algorithm>] : Tente de craquer un hachage avec une wordlist.
            """,
            "config": f"""
            {NORMAL_TEXT_COLOR}--- Aide du module 'config' (Ajustement des Paramètres) ---
            {NORMAL_TEXT_COLOR}config set <key> <value> : Définit un paramètre de configuration, pour l'adaptation.
            {NORMAL_TEXT_COLOR}config get <key>         : Récupère un paramètre de configuration, pour la clarté.
            {NORMAL_TEXT_COLOR}config save              : Sauvegarde la configuration actuelle, pour la persistance.
            {NORMAL_TEXT_COLOR}config load              : Recharge la configuration, pour l'actualisation.
            {NORMAL_TEXT_COLOR}config show              : Affiche toute la configuration actuelle, pour la transparence.
            """
        }
        
        if module_name in help_text:
            print_colored(help_text[module_name], INFO_COLOR)
        else:
            print_colored(f"Aide non disponible pour le module '{module_name}'. Le chemin reste à explorer.", WARNING_COLOR)


    def start_shell(self):
        banner_lines = load_banner(os.path.join("banner", "banner.txt"))
        display_animated_banner(banner_lines)

        print_colored("Tapez 'help' pour invoquer la sagesse.", INFO_COLOR)
        print_colored("Tapez 'exit' pour vous retirer de la matrice.", INFO_COLOR)

        while True:
            try:
                sys.stdout.write(PROMPT_COLOR + "Wazabi> " + Style.RESET_ALL)
                sys.stdout.flush()
                command_line = input().strip()
                
                if not command_line:
                    continue

                command_parts = command_line.split()
                if command_parts[0] == "exit":
                    break

                self.run_command(command_parts)
                
            except EOFError: # Gérer Ctrl+D pour quitter
                print_colored("\nDétection de EOF. Quittant le shell. Que la force éthique soit avec toi.", INFO_COLOR)
                break
            except KeyboardInterrupt: # Gérer Ctrl+C pour éviter les erreurs
                print_colored("\nOpération interrompue. Pour quitter, tapez 'exit'. La persévérance est une vertu.", WARNING_COLOR)
            except Exception as e:
                logger.exception("Erreur inattendue dans la boucle du shell.")
                print_colored(f"Une erreur inattendue est survenue : {e}. Le code a trébuché.", ERROR_COLOR)

        self.db_manager.close() # S'assurer de fermer la connexion DB à la sortie

# --- Point d'entrée du script ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Lance le Wazabi Shell interactif ou exécute une commande directe, imprégné de la philosophie éthique."
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Active le mode verbeux (niveau de journalisation DEBUG), pour une vision plus profonde."
    )
    parser.add_argument(
        "command_args",
        nargs=argparse.REMAINDER,
        help="Commande et arguments à exécuter directement, sans lancer le shell interactif, pour une action rapide."
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Mode verbeux activé. Que la lumière des détails éclaire ton chemin.")

    shell = WazabiShell()

    if args.command_args:
        logger.info(f"Exécution directe de la commande : {' '.join(args.command_args)}")
        print_colored(f"Exécution de la commande directe : {' '.join(args.command_args)}. Rapidité et précision.", PROMPT_COLOR)
        shell.run_command(args.command_args)
        shell.db_manager.close()
    else:
        shell.start_shell()

