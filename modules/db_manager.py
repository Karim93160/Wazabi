import sqlite3
import os
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

class DBManager:
    def __init__(self, db_name='wazabi_shell_data.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def connect(self):
        """Établit la connexion à la base de données et crée la table si elle n'existe pas."""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            self._create_tables()
            print_colored(f"Connecté à la base de données '{self.db_name}'.", SUCCESS_COLOR)
            return True
        except sqlite3.Error as e:
            print_colored(f"Erreur de connexion à la base de données: {e}", ERROR_COLOR)
            return False

    def close(self):
        """Ferme la connexion à la base de données."""
        if self.conn:
            self.conn.close()
            print_colored(f"Déconnecté de la base de données '{self.db_name}'.", INFO_COLOR)

    def _create_tables(self):
        """Crée les tables nécessaires si elles n'existent pas."""
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS processed_urls (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT NOT NULL UNIQUE,
                    status TEXT,
                    timestamp TEXT
                )
            ''')
            self.conn.commit()
            print_colored("Table 'processed_urls' vérifiée/créée.", SUCCESS_COLOR)
        except sqlite3.Error as e:
            print_colored(f"Erreur lors de la création des tables: {e}", ERROR_COLOR)

    def add_processed_url(self, url, status="completed", timestamp=None):
        """Ajoute ou met à jour une URL traitée."""
        if not self.conn:
            print_colored("Erreur: Connexion à la base de données non établie.", ERROR_COLOR)
            return False
        
        if timestamp is None:
            from datetime import datetime
            timestamp = datetime.now().isoformat()

        try:
            self.cursor.execute(
                "INSERT OR REPLACE INTO processed_urls (url, status, timestamp) VALUES (?, ?, ?)",
                (url, status, timestamp)
            )
            self.conn.commit()
            print_colored(f"URL '{url}' ajoutée/mise à jour avec le statut '{status}'.", SUCCESS_COLOR)
            return True
        except sqlite3.IntegrityError:
            print_colored(f"Avertissement: L'URL '{url}' existe déjà et a été mise à jour.", WARNING_COLOR)
            return False
        except sqlite3.Error as e:
            print_colored(f"Erreur lors de l'ajout/mise à jour de l'URL: {e}", ERROR_COLOR)
            return False

    def get_processed_urls(self):
        """Récupère toutes les URLs traitées."""
        if not self.conn:
            print_colored("Erreur: Connexion à la base de données non établie.", ERROR_COLOR)
            return None
        try:
            self.cursor.execute("SELECT url, status, timestamp FROM processed_urls")
            urls = self.cursor.fetchall()
            if urls:
                print_colored("\n--- URLs Traitées ---", INFO_COLOR)
                for url, status, timestamp in urls:
                    print_colored(f"  URL: {url}, Statut: {status}, Date: {timestamp}", NORMAL_TEXT_COLOR)
                print_colored("--------------------", INFO_COLOR)
            else:
                print_colored("Aucune URL traitée trouvée dans la base de données.", INFO_COLOR)
            return urls
        except sqlite3.Error as e:
            print_colored(f"Erreur lors de la récupération des URLs: {e}", ERROR_COLOR)
            return None

    def execute_query(self, query):
        """Exécute une requête SQL arbitraire (à utiliser avec PRUDENCE)."""
        if not self.conn:
            print_colored("Erreur: Connexion à la base de données non établie.", ERROR_COLOR)
            return None
        try:
            print_colored(f"Exécution de la requête SQL: '{query}'", WARNING_COLOR)
            self.cursor.execute(query)
            if query.strip().upper().startswith("SELECT"):
                results = self.cursor.fetchall()
                if results:
                    print_colored("\n--- Résultats de la Requête SQL ---", INFO_COLOR)
                    # Afficher les noms de colonnes si possible
                    col_names = [description[0] for description in self.cursor.description]
                    print_colored(" | ".join(col_names), INFO_COLOR)
                    print_colored("-" * (len(" | ".join(col_names)) + 5), INFO_COLOR)
                    for row in results:
                        print_colored(f" {row}", NORMAL_TEXT_COLOR)
                    print_colored("---------------------------------", INFO_COLOR)
                else:
                    print_colored("La requête SELECT n'a retourné aucun résultat.", INFO_COLOR)
                return results
            else:
                self.conn.commit()
                print_colored("Requête SQL exécutée avec succès (non-SELECT).", SUCCESS_COLOR)
                return True
        except sqlite3.Error as e:
            print_colored(f"Erreur lors de l'exécution de la requête SQL: {e}", ERROR_COLOR)
            return False


