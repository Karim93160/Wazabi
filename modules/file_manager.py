import os
import shutil
import fnmatch
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

class FileManager:
    def copy_item(self, source, destination):
        """Copie un fichier ou un répertoire."""
        try:
            if os.path.isdir(source):
                shutil.copytree(source, destination)
                print_colored(f"Dossier '{source}' copié vers '{destination}'.", SUCCESS_COLOR)
            elif os.path.isfile(source):
                shutil.copy2(source, destination) # copy2 preserve les metadonnées
                print_colored(f"Fichier '{source}' copié vers '{destination}'.", SUCCESS_COLOR)
            else:
                print_colored(f"Erreur: La source '{source}' n'existe pas.", ERROR_COLOR)
                return False
            return True
        except FileNotFoundError:
            print_colored(f"Erreur: Le chemin source '{source}' n'existe pas.", ERROR_COLOR)
            return False
        except FileExistsError:
            print_colored(f"Erreur: La destination '{destination}' existe déjà et ne peut pas être écrasée (pour les dossiers).", ERROR_COLOR)
            return False
        except Exception as e:
            print_colored(f"Erreur lors de la copie de '{source}' vers '{destination}': {e}", ERROR_COLOR)
            return False

    def move_item(self, source, destination):
        """Déplace un fichier ou un répertoire."""
        try:
            shutil.move(source, destination)
            print_colored(f"'{source}' déplacé vers '{destination}'.", SUCCESS_COLOR)
            return True
        except FileNotFoundError:
            print_colored(f"Erreur: Le chemin source '{source}' n'existe pas.", ERROR_COLOR)
            return False
        except Exception as e:
            print_colored(f"Erreur lors du déplacement de '{source}' vers '{destination}': {e}", ERROR_COLOR)
            return False

    def delete_item(self, path):
        """Supprime un fichier ou un répertoire."""
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
                print_colored(f"Dossier '{path}' supprimé.", SUCCESS_COLOR)
            elif os.path.isfile(path):
                os.remove(path)
                print_colored(f"Fichier '{path}' supprimé.", SUCCESS_COLOR)
            else:
                print_colored(f"Erreur: Le chemin '{path}' n'existe pas.", ERROR_COLOR)
                return False
            return True
        except FileNotFoundError:
            print_colored(f"Erreur: Le chemin '{path}' est introuvable.", ERROR_COLOR)
            return False
        except Exception as e:
            print_colored(f"Erreur lors de la suppression de '{path}': {e}", ERROR_COLOR)
            return False

    def list_directory(self, path='.', recursive=False):
        """Liste le contenu d'un répertoire."""
        if not os.path.exists(path):
            print_colored(f"Erreur: Le chemin '{path}' n'existe pas.", ERROR_COLOR)
            return None
        if not os.path.isdir(path):
            print_colored(f"Erreur: Le chemin '{path}' n'est pas un répertoire.", ERROR_COLOR)
            return None

        print_colored(f"\n--- Contenu de '{path}' ---", INFO_COLOR)
        try:
            if recursive:
                for root, dirs, files in os.walk(path):
                    level = root.replace(path, '').count(os.sep)
                    indent = ' ' * 4 * (level)
                    print_colored(f"{indent}{os.path.basename(root)}/", INFO_COLOR)
                    subindent = ' ' * 4 * (level + 1)
                    for f in files:
                        print_colored(f"{subindent}{f}", NORMAL_TEXT_COLOR)
            else:
                with os.scandir(path) as entries:
                    for entry in entries:
                        if entry.is_dir():
                            print_colored(f"  [D] {entry.name}", INFO_COLOR)
                        else:
                            print_colored(f"  [F] {entry.name}", NORMAL_TEXT_COLOR)
            print_colored("-----------------------", INFO_COLOR)
            return True
        except Exception as e:
            print_colored(f"Erreur lors de la liste du répertoire '{path}': {e}", ERROR_COLOR)
            return False

    def find_files(self, directory, pattern=None, extension=None, recursive=False):
        """Recherche des fichiers dans un répertoire par nom ou extension."""
        if not os.path.isdir(directory):
            print_colored(f"Erreur: Le répertoire '{directory}' n'existe pas.", ERROR_COLOR)
            return None

        print_colored(f"\n--- Recherche dans '{directory}' ---", INFO_COLOR)
        found_files = []
        try:
            for root, _, files in os.walk(directory):
                for file_name in files:
                    match = False
                    if pattern:
                        if fnmatch.fnmatch(file_name, pattern):
                            match = True
                    
                    if extension:
                        # Assure que l'extension commence par un point pour la comparaison
                        if not extension.startswith('.'):
                            extension = '.' + extension
                        if file_name.endswith(extension):
                            match = True
                    
                    # Si aucun pattern ou extension n'est donné, tous les fichiers correspondent
                    if not pattern and not extension:
                        match = True

                    if match:
                        found_files.append(os.path.join(root, file_name))
                
                if not recursive:
                    break # Si pas récursif, ne fait qu'une seule couche

            if found_files:
                print_colored(f"Fichiers trouvés (total: {len(found_files)}) :", SUCCESS_COLOR)
                for f in found_files:
                    print_colored(f"  - {f}", NORMAL_TEXT_COLOR)
            else:
                print_colored("Aucun fichier trouvé correspondant aux critères.", WARNING_COLOR)
            print_colored("----------------------------", INFO_COLOR)
            return found_files

        except Exception as e:
            print_colored(f"Erreur lors de la recherche de fichiers dans '{directory}': {e}", ERROR_COLOR)
            return None


