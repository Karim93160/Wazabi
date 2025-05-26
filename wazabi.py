import argparse
import sys
import os
import json
import logging
import time
from datetime import datetime
from colorama import init, Fore, Style
from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.document import Document
from prompt_toolkit.styles import Style as PromptStyle
from prompt_toolkit.formatted_text import ANSI # Pour afficher les couleurs colorama

# Initialisation de Colorama
init(autoreset=True)

# Configuration des chemins
WAZABI_ROOT = os.environ.get('WAZABI_SHELL_ROOT', os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(WAZABI_ROOT, "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, f"wazabi_shell_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("WazabiShell")

# Constantes de couleur (utilisées avec Colorama)
SUCCESS_COLOR = Fore.GREEN + Style.BRIGHT
INFO_COLOR = Fore.BLUE + Style.BRIGHT
WARNING_COLOR = Fore.YELLOW + Style.BRIGHT
ERROR_COLOR = Fore.RED + Style.BRIGHT
PROMPT_COLOR = Fore.CYAN + Style.BRIGHT
WAZABI_COLOR = Fore.MAGENTA + Style.BRIGHT
NORMAL_TEXT_COLOR = Fore.WHITE + Style.NORMAL

def print_colored(message, color=INFO_COLOR):
    """Affiche un message coloré dans la console."""
    print(color + message + Style.RESET_ALL)

def load_banner():
    """
    Charge et retourne le contenu de la bannière en utilisant le chemin racine.
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

# --- WazabiShellCompleter for prompt_toolkit ---
class WazabiShellCompleter(Completer):
    _ARG_MAPPING = {
        ("file", "copy"): {"s": "source", "d": "destination"},
        ("file", "move"): {"s": "source", "d": "destination"},
        ("file", "delete"): {"p": "path"},
        ("file", "list"): {"p": "path", "recursive": "recursive"},
        ("file", "find"): {"d": "directory", "pattern": "pattern", "extension": "extension", "recursive": "recursive"},
        ("network", "get"): {"u": "url", "params": "params", "headers": "headers"},
        ("network", "post"): {"u": "url", "data": "data", "json": "json_data", "headers": "headers"},
        ("network", "download"): {"u": "url", "d": "destination"},
        ("network", "scan_ports"): {"h": "host", "p": "ports"},
        ("data", "read_csv"): {"p": "path"},
        ("data", "write_csv"): {"p": "path", "j": "data_json"},
        ("data", "read_json"): {"p": "path"},
        ("data", "write_json"): {"p": "path", "d": "data_dict"},
        ("data", "process_text"): {"s": "source_path", "o": "output_path", "operation": "operation"},
        ("db", "add_url"): {"u": "url", "s": "status"},
        ("db", "execute_sql"): {"q": "query"},
        ("security", "hash"): {"t": "text", "a": "algorithm"},
        ("security", "encode_base64"): {"d": "data"},
        ("security", "decode_base64"): {"d": "data"},
        ("security", "generate_password"): {"l": "length", "no_digits": "include_digits", "no_special": "include_special"},
        ("security", "check_hash"): {"c": "candidate", "t": "target_hash", "a": "algorithm"},
        ("wazabi", "analyze_dir"): {"d": "directory", "sensitive_extensions": "sensitive_extensions", "min_size_mb": "min_size_mb", "o": "output_file"},
        ("wazabi", "generate_payload"): {"l": "length", "charset": "charset", "num_lines": "num_lines", "prefix": "prefix", "suffix": "suffix"},
        ("wazabi", "dict_attack"): {"h": "target_hash", "w": "wordlist_path", "a": "algorithm"},
        ("config", "set"): {"key": "key_to_set", "value": "value_to_set"},
        ("config", "get"): {"key": "key_to_get"},
    }

    _JSON_ARGS = {
        "params", "headers", "json_data", # Pour network
        "data_json", "data_dict", # Pour data (write_csv/write_json)
    }

    # Dictionnaire pour les suggestions de valeurs spécifiques pour certains arguments
    _VALUE_SUGGESTIONS = {
        ("data", "process_text", "operation"): ["uppercase", "lowercase", "reverse", "rot13"],
        ("security", "hash", "algorithm"): ["md5", "sha256", "sha512"],
        ("security", "check_hash", "algorithm"): ["md5", "sha256", "sha512"],
        ("wazabi", "generate_payload", "charset"): ["alphanum_special", "alpha", "num", "special", "whitespace"],
    }

    # Arguments qui attendent un chemin de fichier/dossier
    _PATH_ARGS = {
        "source", "destination", "path", "directory", "output_file",
        "wordlist_path", "source_path", "target_file"
    }

    def __init__(self, commands, config_manager=None):
        self.commands = commands
        self.config_manager = config_manager
        self.all_top_level_commands = sorted(list(self.commands.keys()) + ["exit", "help"])

    def _get_last_arg_name(self, command_parts, key_tuple):
        """Détermine le nom long du dernier argument si le jeton précédent était un flag."""
        mapping_for_cmd = self._ARG_MAPPING.get(key_tuple, {})
        for i in range(len(command_parts) - 1, -1, -1):
            token = command_parts[i]
            if token.startswith('-'):
                stripped_token = token.lstrip('-')
                # Cherche la correspondance exacte ou le nom long
                if stripped_token in mapping_for_cmd:
                    return mapping_for_cmd[stripped_token]
                for short, long in mapping_for_cmd.items():
                    if stripped_token == short or stripped_token == long:
                        return long
        return None

    def get_completions(self, document: Document, complete_event):
        text_before_cursor = document.text_before_cursor
        parts = document.text.split()
        current_word = document.get_word_before_cursor(WORD=True)

        # Determine the position of the current word within the entire line
        # This is crucial for calculating start_position for Completion
        current_word_start_index = document.cursor_position - len(current_word)

        # 1. Suggestions de commandes de premier niveau
        if not parts or (len(parts) == 1 and not text_before_cursor.endswith(' ')):
            for cmd in self.all_top_level_commands:
                if cmd.startswith(current_word):
                    yield Completion(cmd, start_position=-len(current_word))
            return

        module_name = parts[0].lower()
        if module_name not in self.commands:
            return # Module inconnu, pas de suggestions

        # 2. Suggestions de sous-commandes
        if len(parts) == 1 or (len(parts) == 2 and not text_before_cursor.endswith(' ')):
            current_subcommand_text = parts[1] if len(parts) == 2 and not text_before_cursor.endswith(' ') else ""
            for sub_cmd in self.commands[module_name]:
                if sub_cmd.startswith(current_subcommand_text):
                    yield Completion(sub_cmd, start_position=-len(current_word)) # Corrected
            return

        # Si on est au-delà du module et de la sous-commande
        command_name = parts[1].lower()
        key_tuple = (module_name, command_name)

        # 3. Suggestions pour les arguments positionnels de 'config set/get'
        if module_name == "config":
            if command_name in ("set", "get"):
                # Si on est après 'config set' ou 'config get' et qu'on tape la clé (position 2 ou 3 sans flag)
                if ((len(parts) == 2 and text_before_cursor.endswith(' ')) or
                    (len(parts) == 3 and not current_word.startswith('-'))): # Corrected
                    if self.config_manager:
                        for key in self.config_manager.config_data.keys():
                            if key.startswith(current_word): # Corrected
                                yield Completion(key, start_position=-len(current_word)) # Corrected
                    return
                # Si on est après 'config set <key>' et qu'on tape la valeur (position 4 ou plus sans flag)
                if command_name == "set" and len(parts) >= 4 and not current_word.startswith('-'): # Corrected
                    # Pour la valeur de set, il n'y a pas de suggestions prédéfinies
                    return

        # Déterminer si le token précédent était un argument nécessitant une valeur
        last_arg_name = self._get_last_arg_name(parts[:-1], key_tuple) # Regarde les tokens précédents, pas le token actuel

        # 4. Suggestions de valeurs pour les arguments
        if last_arg_name:
            # Suggestions de valeurs prédéfinies
            value_suggestions_key = (module_name, command_name, last_arg_name)
            if value_suggestions_key in self._VALUE_SUGGESTIONS:
                for val_sugg in self._VALUE_SUGGESTIONS[value_suggestions_key]:
                    if val_sugg.startswith(current_word): # Corrected
                        yield Completion(val_sugg, start_position=-len(current_word)) # Corrected
                return # Si des valeurs prédéfinies existent, on ne fait pas d'autres suggestions pour cet argument

            # Suggestions de chemins pour les arguments de type fichier/dossier
            if last_arg_name in self._PATH_ARGS:
                path_prefix = current_word # Corrected
                directory = os.path.dirname(path_prefix)
                if not directory: # Si pas de répertoire spécifié, on regarde le répertoire courant
                    directory = "."

                try:
                    for item in os.listdir(directory):
                        full_path = os.path.join(directory, item)
                        # Pour qu'il corresponde à la partie tapée
                        if item.startswith(os.path.basename(path_prefix)):
                            if os.path.isdir(full_path):
                                # Ajouter un slash pour les répertoires
                                yield Completion(item + os.sep, start_position=-len(current_word)) # Corrected
                            else:
                                yield Completion(item, start_position=-len(current_word)) # Corrected
                except OSError:
                    pass # Le répertoire n'existe pas ou permissions refusées
                return

            # Pas de suggestions spécifiques pour les arguments JSON ou autres arguments
            if last_arg_name in self._JSON_ARGS:
                return # Pas de suggestions pour les valeurs JSON, laisse l'utilisateur taper

        # 5. Suggestions d'arguments (flags comme --source ou -s)
        # Suggérer si le mot courant commence par '-' ou si le dernier caractère était un espace (et pas déjà une valeur attendue)
        if current_word.startswith('-') or (text_before_cursor.endswith(' ') and not last_arg_name): # Corrected

            command_mapping = self._ARG_MAPPING.get(key_tuple, {})
            existing_args = set()
            for p in parts:
                if p.startswith('-'):
                    stripped = p.lstrip('-')
                    # Convertir en nom long pour la vérification
                    found_long_name = None
                    for short, long in command_mapping.items():
                        if stripped == short or stripped == long:
                            found_long_name = long
                            break
                    if found_long_name:
                        existing_args.add(found_long_name)

            for short_arg, long_arg in command_mapping.items():
                if long_arg not in existing_args: # Suggérer seulement si l'argument n'est pas déjà présent
                    if f"-{short_arg}".startswith(current_word): # Corrected
                        yield Completion(f"-{short_arg}", start_position=-len(current_word)) # Corrected
                    if f"--{long_arg}".startswith(current_word): # Corrected
                        yield Completion(f"--{long_arg}", start_position=-len(current_word)) # Corrected


# --- WazabiShell Class ---
class WazabiShell:
    _ARG_MAPPING = WazabiShellCompleter._ARG_MAPPING # Réutilise le mapping du completer
    _JSON_ARGS = WazabiShellCompleter._JSON_ARGS

    def __init__(self):
        from modules.file_manager import FileManager
        from modules.network_utils import NetworkUtils
        from modules.data_processor import DataProcessor
        from modules.db_manager import DBManager
        from modules.security_utils import SecurityUtils
        from modules.wazabi_tools import WazabiTools
        from modules.config_manager import ConfigManager

        self.db_manager = DBManager(os.path.join(WAZABI_ROOT, "wazabi_shell_data.db"))
        self.config_manager = ConfigManager(os.path.join(WAZABI_ROOT, "config.json"))

        self.file_manager = FileManager()
        self.network_utils = NetworkUtils()
        self.data_processor = DataProcessor()
        self.security_utils = SecurityUtils()
        self.wazabi_tools = WazabiTools(self.network_utils, self.file_manager)

        self.db_manager.connect()

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
                "scan_ports": self.wazabi_tools.port_scan_wrapper,
            },
            "data": {
                "read_csv": self.data_processor.read_csv,
                "write_csv": self.data_processor.write_csv,
                "read_json": self.data_processor.read_json,
                "write_json": self.data_processor.write_json,
                "process_text": self._process_text_file_wrapper,
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
                "check_hash": self.security_utils.check_hash,
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

        self.completer = WazabiShellCompleter(self.commands, self.config_manager)

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
        """
        Exécute une commande basée sur les parties analysées de la ligne de commande.
        Gère la logique de parsing des arguments, la validation et l'appel des fonctions de module.
        """
        if not command_parts:
            return

        module_name = command_parts[0].lower()
        if module_name == "exit":
            print_colored("Au revoir, Gardien Éthique ! Que tes audits soient fructueux.", SUCCESS_COLOR)
            return "exit"
        elif module_name == "help":
            if len(command_parts) > 1:
                self.show_module_help(command_parts[1].lower())
            else:
                show_help()
            return

        if module_name not in self.commands:
            print_colored(f"Erreur: Module '{module_name}' non reconnu. Le chemin de la sagesse est ailleurs. Tapez 'help'.", ERROR_COLOR)
            return

        if len(command_parts) < 2:
            print_colored(f"Erreur: Commande manquante pour le module '{module_name}'. Cherchez la lumière : 'help {module_name}'.", ERROR_COLOR)
            return

        command_name = command_parts[1].lower()
        if command_name not in self.commands[module_name]:
            print_colored(f"Erreur: Commande '{command_name}' non reconnue pour le module '{module_name}'. Explorez : 'help {module_name}'.", ERROR_COLOR)
            return

        func = self.commands[module_name][command_name]
        raw_args_dict = {} # Dictionnaire temporaire pour stocker les arguments tels que saisis
        i = 2
        while i < len(command_parts):
            arg = command_parts[i]
            if arg.startswith('-') or arg.startswith('--'):
                key = arg.lstrip('-').replace('-', '_')

                # Vérifier si la clé suivante existe ET si elle n'est PAS un autre flag
                if i + 1 < len(command_parts) and not command_parts[i+1].startswith('-'):
                    value = command_parts[i+1]

                    # Déterminer le nom long de l'argument pour vérifier s'il attend un JSON
                    mapped_key_for_json_check = self._ARG_MAPPING.get((module_name, command_name), {}).get(key, key)

                    if mapped_key_for_json_check in self._JSON_ARGS or key in self._JSON_ARGS:
                        try:
                            raw_args_dict[key] = json.loads(value)
                        except json.JSONDecodeError:
                            print_colored(f"Avertissement: Valeur '{value}' pour '{arg}' n'est pas un JSON valide. Traité comme une chaîne.", WARNING_COLOR)
                            raw_args_dict[key] = value # Conserver la valeur brute si non JSON
                    else:
                        try:
                            raw_args_dict[key] = int(value)
                        except ValueError:
                            try:
                                raw_args_dict[key] = float(value)
                            except ValueError:
                                raw_args_dict[key] = value # Reste une chaîne
                    i += 2
                else: # Argument sans valeur (flag) ou argument qui attend une valeur mais n'en a pas
                    mapped_key_for_json_check = self._ARG_MAPPING.get((module_name, command_name), {}).get(key, key)
                    if mapped_key_for_json_check in self._JSON_ARGS or key in self._JSON_ARGS:
                        raw_args_dict[key] = {} # JSON vide par défaut
                    else:
                        raw_args_dict[key] = True # C'est un vrai flag booléen
                    i += 1
            else:
                # Gérer les arguments positionnels pour 'config set/get'
                # Ces arguments ne sont pas préfixés par '-' ou '--'
                if module_name == "config" and command_name == "set" and 'key_to_set' not in raw_args_dict:
                    raw_args_dict['key_to_set'] = arg
                    i += 1
                elif module_name == "config" and command_name == "set" and 'value_to_set' not in raw_args_dict:
                    raw_args_dict['value_to_set'] = ' '.join(command_parts[i:]) # Capture le reste de la ligne comme valeur
                    i = len(command_parts) # Avance l'index à la fin pour arrêter le traitement
                elif module_name == "config" and command_name == "get" and 'key_to_get' not in raw_args_dict:
                    raw_args_dict['key_to_get'] = arg
                    i += 1
                else:
                    print_colored(f"Avertissement: Argument inattendu ou mal formaté : '{arg}'. Ignoré. Concentrez-vous sur la syntaxe.", WARNING_COLOR)
                    i += 1

        # Dictionnaire final avec les noms de paramètres corrects pour l'appel de fonction
        final_args_for_func = {}
        mapping_for_command = self._ARG_MAPPING.get((module_name, command_name), {})

        for raw_key, raw_value in raw_args_dict.items():
            mapped_key = mapping_for_command.get(raw_key, raw_key)
            final_args_for_func[mapped_key] = raw_value

        try:
            # Cas spécifiques qui ne peuvent pas être gérés par un simple **kwargs
            if module_name == "config" and command_name == "set":
                if 'key_to_set' in raw_args_dict and 'value_to_set' in raw_args_dict:
                    self.config_manager.set_setting(raw_args_dict['key_to_set'], raw_args_dict['value_to_set'])
                else:
                    print_colored("Erreur: Utilisation: config set <clé> <valeur> (précision requise).", ERROR_COLOR)
            elif module_name == "config" and command_name == "get":
                if 'key_to_get' in raw_args_dict:
                    value = self.config_manager.get_setting(raw_args_dict['key_to_get'])
                    print_colored(f"Paramètre '{raw_args_dict['key_to_get']}' : {value}", INFO_COLOR)
                else:
                    print_colored("Erreur: Utilisation: config get <clé> (clarté nécessaire).", ERROR_COLOR)
            elif module_name == "security" and command_name == "generate_password":
                length_val = final_args_for_func.get('length', 16)
                if isinstance(length_val, str) and length_val.isdigit():
                    length_val = int(length_val)

                func(length=length_val,
                     include_digits=not final_args_for_func.get('include_digits', False),
                     include_special=not final_args_for_func.get('include_special', False))
            elif module_name == "network" and command_name == "scan_ports":
                host = final_args_for_func.get('host', self.config_manager.get_setting("default_target_host"))
                ports = final_args_for_func.get('ports', self.config_manager.get_setting("default_scan_ports"))
                func(host, ports)
            elif module_name == "wazabi" and command_name == "analyze_dir":
                sensitive_ext = final_args_for_func.get('sensitive_extensions')
                if isinstance(sensitive_ext, str):
                    sensitive_ext = sensitive_ext.split(',')
                func(directory=final_args_for_func.get('directory'),
                     sensitive_extensions=sensitive_ext,
                     min_size_mb=final_args_for_func.get('min_size_mb', 10),
                     output_file=final_args_for_func.get('output_file'))
            elif module_name == "wazabi" and command_name == "generate_payload":
                 func(length=final_args_for_func.get('length', self.config_manager.get_setting("default_payload_length")),
                     charset=final_args_for_func.get('charset', 'alphanum_special'),
                     num_lines=final_args_for_func.get('num_lines', 1),
                     prefix=final_args_for_func.get('prefix', ''),
                     suffix=final_args_for_func.get('suffix', ''))
            elif module_name == "db" and command_name == "add_url":
                func(final_args_for_func.get('url'), final_args_for_func.get('status'), datetime.now().isoformat())
            else:
                # Pour toutes les autres commandes, on essaie d'appeler la fonction avec les arguments mappés
                func(**final_args_for_func)

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
        """Lance la boucle interactive du shell."""
        print_colored("Tapez 'help' pour invoquer la sagesse.", INFO_COLOR)
        print_colored("Tapez 'exit' pour vous retirer de la matrice.", INFO_COLOR)

        # Style pour le prompt_toolkit pour correspondre à Colorama
        prompt_style = PromptStyle.from_dict({
            'prompt': 'ansicyan bold',  # Utilise la couleur cyan de colorama
            'completion-menu.completion': 'bg:#333333 #ffffff', # Fond sombre, texte blanc
            'completion-menu.completion.current': 'bg:#00aa00 #ffffff', # Élément sélectionné en vert
            'scrollbar.background': 'bg:#888888',
            'scrollbar.button': 'bg:#cccccc',
        })

        while True:
            try:
                # Utilise prompt de prompt_toolkit
                command_line = prompt(
                    ANSI(f"{PROMPT_COLOR}Wazabi> {Style.RESET_ALL}"), # Permet à prompt_toolkit d'interpréter les codes ANSI de Colorama
                    completer=self.completer,
                    style=prompt_style,
                    complete_while_typing=True, # Active la complétion pendant la frappe
                    wrap_lines=True # Permet aux lignes longues de s'enrouler
                ).strip()

                if not command_line:
                    continue

                command_parts = command_line.split()
                if command_parts[0].lower() == "exit":
                    break

                self.run_command(command_parts)

            except EOFError:
                print_colored("\nDétection de EOF. Quittant le shell. Que la force éthique soit avec toi.", INFO_COLOR)
                break
            except KeyboardInterrupt:
                print_colored("\nOpération interrompue. Pour quitter, tapez 'exit'. La persévérance est une vertu.", WARNING_COLOR)
            except Exception as e:
                logger.exception("Erreur inattendue dans la boucle du shell.")
                print_colored(f"Une erreur inattendue est survenue : {e}. Le code a trébuché.", ERROR_COLOR)

        self.db_manager.close()

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

    banner_content = load_banner()
    display_animated_banner(banner_content)

    shell = WazabiShell()
    if args.command_args:
        logger.info(f"Exécution directe de la commande : {' '.join(args.command_args)}")
        print_colored(f"Exécution de la commande directe : {' '.join(args.command_args)}. Rapidité et précision.", PROMPT_COLOR)
        if shell.run_command(args.command_args) != "exit":
            shell.db_manager.close()
    else:
        shell.start_shell()
