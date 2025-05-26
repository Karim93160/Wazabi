import csv
import json
from colorama import Fore, Style, init
init(autoreset=True)

# Constantes de couleurs
SUCCESS_COLOR = Fore.GREEN + Style.BRIGHT
INFO_COLOR = Fore.BLUE + Style.BRIGHT
ERROR_COLOR = Fore.RED + Style.BRIGHT
NORMAL_TEXT_COLOR = Fore.WHITE + Style.NORMAL

def print_colored(message, color=INFO_COLOR):
    """Affiche un message coloré dans la console."""
    print(color + message + Style.RESET_ALL)

class DataProcessor:
    def read_csv(self, file_path):
        """Lit un fichier CSV et retourne une liste de dictionnaires."""
        data = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data.append(row)
            print_colored(f"Fichier CSV '{file_path}' lu avec succès. {len(data)} lignes trouvées.", SUCCESS_COLOR)
            # Afficher un aperçu pour ne pas inonder la console
            for i, row in enumerate(data[:5]):
                print_colored(f"  Ligne {i+1}: {row}", NORMAL_TEXT_COLOR)
            if len(data) > 5:
                print_colored("  ...", NORMAL_TEXT_COLOR)
            return data
        except FileNotFoundError:
            print_colored(f"Erreur: Le fichier '{file_path}' est introuvable.", ERROR_COLOR)
            return None
        except Exception as e:
            print_colored(f"Erreur lors de la lecture du fichier CSV: {e}", ERROR_COLOR)
            return None

    def write_csv(self, file_path, data, fieldnames=None):
        """Écrit une liste de dictionnaires dans un fichier CSV."""
        if not data:
            print_colored("Avertissement: Aucune donnée à écrire dans le fichier CSV.", WARNING_COLOR)
            return False
        
        if fieldnames is None:
            # Tente de déduire les noms de champs à partir de la première ligne
            fieldnames = list(data[0].keys())

        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            print_colored(f"Données écrites dans '{file_path}' avec succès.", SUCCESS_COLOR)
            return True
        except Exception as e:
            print_colored(f"Erreur lors de l'écriture du fichier CSV: {e}", ERROR_COLOR)
            return False

    def read_json(self, file_path):
        """Lit un fichier JSON et retourne le contenu."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print_colored(f"Fichier JSON '{file_path}' lu avec succès.", SUCCESS_COLOR)
            print_colored(f"Aperçu du contenu JSON: {json.dumps(data, indent=2)[:500]}...", NORMAL_TEXT_COLOR)
            return data
        except FileNotFoundError:
            print_colored(f"Erreur: Le fichier '{file_path}' est introuvable.", ERROR_COLOR)
            return None
        except json.JSONDecodeError:
            print_colored(f"Erreur: Le fichier '{file_path}' n'est pas un JSON valide.", ERROR_COLOR)
            return None
        except Exception as e:
            print_colored(f"Erreur lors de la lecture du fichier JSON: {e}", ERROR_COLOR)
            return None

    def write_json(self, file_path, data):
        """Écrit des données dans un fichier JSON."""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            print_colored(f"Données écrites dans '{file_path}' avec succès.", SUCCESS_COLOR)
            return True
        except Exception as e:
            print_colored(f"Erreur lors de l'écriture du fichier JSON: {e}", ERROR_COLOR)
            return False

    def process_text_content(self, text_content, operation='uppercase'):
        """
        Traite une chaîne de texte selon l'opération spécifiée.
        Opérations supportées : 'uppercase', 'lowercase', 'reverse', 'rot13'.
        """
        processed_text = ""
        if operation == 'uppercase':
            processed_text = text_content.upper()
        elif operation == 'lowercase':
            processed_text = text_content.lower()
        elif operation == 'reverse':
            processed_text = text_content[::-1]
        elif operation == 'rot13':
            processed_text = text_content.encode('rot13').decode('utf-8')
        else:
            print_colored(f"Opération '{operation}' non supportée. Opérations valides: 'uppercase', 'lowercase', 'reverse', 'rot13'.", WARNING_COLOR)
            return text_content # Retourne l'original en cas d'opération non valide
        
        print_colored(f"Opération '{operation}' effectuée sur le texte.", SUCCESS_COLOR)
        return processed_text


