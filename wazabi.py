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

# --- Détermination du répertoire racine de Wazabi ---
# On tente de récupérer le chemin racine depuis la variable d'environnement définie par l'installeur.
WAZABI_ROOT = os.environ.get('WAZABI_SHELL_ROOT')

# Si la variable n'est pas définie (par exemple, si le script est exécuté directement sans le wrapper),
# on utilise le répertoire du script lui-même comme fallback.
if WAZABI_ROOT is None:
    WAZABI_ROOT = os.path.dirname(os.path.abspath(__file__))

# --- 1. Configuration de la Journalisation (Logging) ---
# Le répertoire des logs est maintenant basé sur WAZABI_ROOT
LOG_DIR = os.path.join(WAZABI_ROOT, "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, f"wazabi_shell_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

logging.basicConfig(
    level=logging.INFO, # Niveau par défaut, sera ajusté par argparse si -v est présent
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

def load_banner():
    """
    Charge et retourne le contenu de la bannière en utilisant le chemin racine.
    Le chemin de la bannière est maintenant construit ici, basé sur WAZABI_ROOT.
    """
    banner_file_path = os.path.join(WAZABI_ROOT, "banner", "banner.txt")
    try:
        with open(banner_file_path, 'r', encoding='utf-8') as f:
            return f.readlines()
    except FileNotFoundError:
        logger.error(f"Fichier de bannière introuvable : {banner_file_path}")
        return ["--- Wazabi Shell ---", "Banner not found!"]
    except Exception as e:
        logger.exception(f"Erreur lors du chargement de la bannière : {e}")
        return ["--- Wazabi Shell ---", f"Error loading banner: {e}"]

def display_animated_banner(banner_lines):
    """Affiche la bannière avec une animation simple et des couleurs thématiques."""
    sys.stdout.write("\033[H\033[J") # Efface l'écran et place le curseur en haut à gauche
    sys.stdout.flush()

    colors = [Fore.GREEN, Fore.CYAN, Fore.MAGENTA, Fore.BLUE, Fore.YELLOW]

    try:
        terminal_width = os.get_terminal_size().columns
    except OSError:
        terminal_width = 80 # Valeur par défaut si la taille n'est pas détectée

    clear_line = "\r" + " " * terminal_width + "\r"

    print("\n" * 2) # Espace avant la bannière

    for i, line in enumerate(banner_lines):
        colored_line = ""
        for j, char in enumerate(line):
            color = colors[(j + i) % len(colors)] # Cycle les couleurs
            colored_line += color + char

        display_line = colored_line.rstrip()

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
        # On importe les modules ici pour s'assurer que WAZABI_ROOT est défini avant leur instanciation
        # et que les chemins relatifs à WAZABI_ROOT peuvent être utilisés dans ces modules.
        from modules.file_manager import FileManager
        from modules.network_utils import NetworkUtils
        from modules.data_processor import DataProcessor
        from modules.db_manager import DBManager
        from modules.security_utils import SecurityUtils
        from modules.wazabi_tools import WazabiTools
        from modules.config_manager import ConfigManager

        # Instanciation des modules importés, en passant WAZABI_ROOT si nécessaire
        # Par exemple, DBManager aura besoin du chemin de la DB
        self.db_manager = DBManager(os.path.join(WAZABI_ROOT, "wazabi_shell_data.db"))
        self.config_manager = ConfigManager(os.path.join(WAZABI_ROOT, "config.json")) # Supposons que config.json est aussi à la racine

        self.file_manager = FileManager()
        self.network_utils = NetworkUtils()
        self.data_processor = DataProcessor()
        self.security_utils = SecurityUtils()
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

        module_name = command_parts[0].lower() # Convertir en minuscule pour la robustesse
        if module_name == "exit":
            print_colored("Au revoir, Gardien Éthique ! Que tes audits soient fructueux.", SUCCESS_COLOR)
            return "exit"
        elif module_name == "help":
            if len(command_parts) > 1:
                self.show_module_help(command_parts[1].lower()) # Convertir en minuscule
            else:
                show_help()
            return

        if module_name not in self.commands:
            print_colored(f"Erreur: Module '{module_name}' non reconnu. Le chemin de la sagesse est ailleurs. Tapez 'help'.", ERROR_COLOR)
            return

        if len(command_parts) < 2:
            print_colored(f"Erreur: Commande manquante pour le module '{module_name}'. Cherchez la lumière : 'help {module_name}'.", ERROR_COLOR)
            return

        command_name = command_parts[1].lower() # Convertir en minuscule
        if command_name not in self.commands[module_name]:
            print_colored(f"Erreur: Commande '{command_name}' non reconnue pour le module '{module_name}'. Explorez : 'help {module_name}'.", ERROR_COLOR)
            return

        # Tentative de parser les arguments directement pour les fonctions
        args_dict = {}
        i = 2
        while i < len(command_parts):
            arg = command_parts[i]
            if arg.startswith('-') or arg.startswith('--'):
                key = arg.lstrip('-').replace('-', '_') # Convertir 'no-digits' en 'no_digits' pour les clés Python
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
                # Si nous sommes dans 'config set', les arguments positionnels sont attendus
                if module_name == "config" and command_name == "set" and i == 2: # Clé
                    args_dict['key_to_set'] = arg
                    i += 1
                elif module_name == "config" and command_name == "set" and i == 3: # Valeur (peut être multi-mots)
                    args_dict['value_to_set'] = ' '.join(command_parts[i:])
                    i = len(command_parts) # On a consommé le reste des arguments
                elif module_name == "config" and command_name == "get" and i == 2: # Clé
                    args_dict['key_to_get'] = arg
                    i += 1
                else:
                    # Gérer les arguments positionnels pour 'config set' plus bas, sinon avertissement.
                    print_colored(f"Avertissement: Argument inattendu ou mal formaté : '{arg}'. Ignoré. Concentrez-vous sur la syntaxe.", WARNING_COLOR)
                    i += 1

        try:
            func = self.commands[module_name][command_name]

            # Gestion des appels de fonction avec *args et **kwargs
            # Cela rend le mapping plus flexible et réduit les lignes de code répétitives
            if module_name == "config" and command_name == "set":
                if 'key_to_set' in args_dict and 'value_to_set' in args_dict:
                    self.config_manager.set_setting(args_dict['key_to_set'], args_dict['value_to_set'])
                else:
                    print_colored("Erreur: Utilisation: config set <clé> <valeur> (précision requise).", ERROR_COLOR)
            elif module_name == "config" and command_name == "get":
                if 'key_to_get' in args_dict:
                    value = self.config_manager.get_setting(args_dict['key_to_get'])
                    print_colored(f"Paramètre '{args_dict['key_to_get']}' : {value}", INFO_COLOR)
                else:
                    print_colored("Erreur: Utilisation: config get <clé> (clarté nécessaire).", ERROR_COLOR)
            elif module_name == "security" and command_name == "generate_password":
                # Convertir les flags en booléens attendus par la fonction
                func(length=args_dict.get('l', 16),
                     include_digits=not args_dict.get('no_digits', False),
                     include_special=not args_dict.get('no_special', False))
            elif module_name == "network" and command_name == "scan_ports":
                # Utiliser les valeurs par défaut de config_manager si non fournies
                host = args_dict.get('h', self.config_manager.get_setting("default_target_host"))
                ports = args_dict.get('p', self.config_manager.get_setting("default_scan_ports"))
                func(host, ports)
            elif module_name == "wazabi" and command_name == "analyze_dir":
                # Gérer la conversion de sensitive_extensions
                sensitive_ext = args_dict.get('sensitive_extensions')
                if isinstance(sensitive_ext, str):
                    sensitive_ext = sensitive_ext.split(',')
                func(directory=args_dict.get('d'),
                     sensitive_extensions=sensitive_ext,
                     min_size_mb=args_dict.get('min_size_mb', 10),
                     output_file=args_dict.get('o'))
            elif module_name == "wazabi" and command_name == "generate_payload":
                 func(length=args_dict.get('l', self.config_manager.get_setting("default_payload_length")),
                     charset=args_dict.get('charset', 'alphanum_special'),
                     num_lines=args_dict.get('num_lines', 1),
                     prefix=args_dict.get('prefix', ''),
                     suffix=args_dict.get('suffix', ''))
            elif module_name == "db" and command_name == "add_url":
                # Ajout de la date de traitement
                func(args_dict.get('u'), args_dict.get('s'), datetime.now().isoformat())
            else:
                # Pour toutes les autres commandes, on essaie d'appeler la fonction avec les arguments collectés
                # Assurez-vous que les noms des arguments dans args_dict correspondent aux paramètres de la fonction
                func(**args_dict)

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
        # La bannière est maintenant chargée et affichée avant l'appel à start_shell dans __main__
        # Assurez-vous que l'appel `display_animated_banner(load_banner())` n'est pas dupliqué ici.
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
                # Gérer la commande exit directement pour une sortie propre
                if command_parts[0].lower() == "exit":
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

    # Le niveau de logging est ajusté ici, après l'analyse des arguments
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Mode verbeux activé. Que la lumière des détails éclaire ton chemin.")

    # Charge et affiche la bannière après la configuration du logging, avant de lancer le shell ou la commande.
    banner_content = load_banner()
    display_animated_banner(banner_content)

    shell = WazabiShell() # Instancie le shell, qui se connectera à la DB

    if args.command_args:
        logger.info(f"Exécution directe de la commande : {' '.join(args.command_args)}")
        print_colored(f"Exécution de la commande directe : {' '.join(args.command_args)}. Rapidité et précision.", PROMPT_COLOR)
        # run_command peut retourner "exit" si la commande était "exit"
        if shell.run_command(args.command_args) != "exit":
            shell.db_manager.close() # S'assurer de fermer la connexion DB après une commande directe
    else:
        shell.start_shell() # Le shell interactif gère sa propre fermeture de DB

