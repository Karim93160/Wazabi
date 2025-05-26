import json
import os
from colorama import Fore, Style, init
init(autoreset=True)

# Constantes de couleurs
INFO_COLOR = Fore.BLUE + Style.BRIGHT
SUCCESS_COLOR = Fore.GREEN + Style.BRIGHT
WARNING_COLOR = Fore.YELLOW + Style.BRIGHT
ERROR_COLOR = Fore.RED + Style.BRIGHT # <-- Correction ici

def print_colored(message, color=INFO_COLOR):
    """Affiche un message coloré dans la console."""
    print(color + message + Style.RESET_ALL)

class ConfigManager:
    def __init__(self, config_file='wazabi_config.json'):
        self.config_file = config_file
        self.config_data = {}
        self.default_config = {
            "default_target_host": "example.com",
            "default_scan_ports": "80,443",
            "default_payload_length": 16,
            "log_level": "INFO",
            "theme_color": "green"
        }
        self.load_config()

    def load_config(self):
        """Charge la configuration depuis le fichier ou utilise les valeurs par défaut."""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config_data = json.load(f)
                # Fusionner avec les valeurs par défaut pour s'assurer que toutes les clés existent
                self.config_data = {**self.default_config, **self.config_data}
                print_colored(f"Configuration chargée depuis '{self.config_file}'.", SUCCESS_COLOR)
            else:
                self.config_data = self.default_config
                self.save_config() # Sauvegarder la config par défaut si le fichier n'existe pas
                print_colored(f"Fichier de configuration '{self.config_file}' non trouvé. Configuration par défaut appliquée et sauvegardée.", WARNING_COLOR)
        except json.JSONDecodeError:
            print_colored(f"Erreur: Le fichier de configuration '{self.config_file}' est corrompu. Utilisation de la configuration par défaut.", ERROR_COLOR)
            self.config_data = self.default_config
            self.save_config()
        except Exception as e:
            print_colored(f"Erreur lors du chargement de la configuration: {e}. Utilisation de la configuration par défaut.", ERROR_COLOR)
            self.config_data = self.default_config

    def save_config(self):
        """Sauvegarde la configuration actuelle dans le fichier."""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config_data, f, indent=4)
            print_colored(f"Configuration sauvegardée dans '{self.config_file}'.", SUCCESS_COLOR)
        except Exception as e:
            print_colored(f"Erreur lors de la sauvegarde de la configuration: {e}", ERROR_COLOR)

    def get_setting(self, key, default_value=None):
        """Récupère une valeur de configuration. Retourne une valeur par défaut si la clé n'existe pas."""
        return self.config_data.get(key, default_value)

    def set_setting(self, key, value):
        """Définit une valeur de configuration."""
        self.config_data[key] = value
        print_colored(f"Paramètre '{key}' défini à '{value}'. N'oubliez pas de 'config save' pour persister les changements.", INFO_COLOR)

    def show(self):
        """Affiche la configuration actuelle."""
        print_colored("\n--- Configuration Actuelle de Wazabi Shell ---", INFO_COLOR)
        for key, value in self.config_data.items():
            # Attention : NORMAL_TEXT_COLOR n'est pas défini dans le code que vous avez fourni.
            # Si vous utilisez cette variable, assurez-vous de la définir.
            # Pour l'instant, je vais la remplacer par un Style.RESET_ALL pour ne pas causer une nouvelle erreur.
            print_colored(f"  {key}: {value}", Style.RESET_ALL)
        print_colored("--------------------------------------------", INFO_COLOR)

