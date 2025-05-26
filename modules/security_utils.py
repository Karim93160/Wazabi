import hashlib
import base64
import os
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
NORMAL_TEXT_COLOR = Fore.WHITE + Style.NORMAL

def print_colored(message, color=INFO_COLOR):
    """Affiche un message coloré dans la console."""
    print(color + message + Style.RESET_ALL)

class SecurityUtils:
    def hash_string(self, text, algorithm='sha256'):
        """Hashes a string using the specified algorithm."""
        try:
            hash_algorithms = {
                'md5': hashlib.md5,
                'sha1': hashlib.sha1,
                'sha256': hashlib.sha256,
                'sha512': hashlib.sha512
            }
            if algorithm not in hash_algorithms:
                print_colored(f"Erreur: Algorithme de hachage '{algorithm}' non supporté. Utilisez md5, sha1, sha256 ou sha512.", ERROR_COLOR)
                return None
            
            hasher = hash_algorithms[algorithm]()
            hasher.update(text.encode('utf-8'))
            hashed_value = hasher.hexdigest()
            print_colored(f"Hachage '{algorithm}' de '{text}': {hashed_value}", SUCCESS_COLOR)
            return hashed_value
        except Exception as e:
            print_colored(f"Erreur lors du hachage de la chaîne: {e}", ERROR_COLOR)
            return None

    def encode_base64(self, data):
        """Encodes data to Base64."""
        try:
            encoded_data = base64.b64encode(data.encode('utf-8')).decode('utf-8')
            print_colored(f"Données encodées en Base64: {encoded_data}", SUCCESS_COLOR)
            return encoded_data
        except Exception as e:
            print_colored(f"Erreur lors de l'encodage Base64: {e}", ERROR_COLOR)
            return None

    def decode_base64(self, data):
        """Decodes Base64 data."""
        try:
            decoded_data = base64.b64decode(data.encode('utf-8')).decode('utf-8')
            print_colored(f"Données décodées de Base64: {decoded_data}", SUCCESS_COLOR)
            return decoded_data
        except Exception as e:
            print_colored(f"Erreur lors du décodage Base64: {e}", ERROR_COLOR)
            return None

    def generate_password(self, length=16, include_digits=True, include_special=True):
        """Generates a strong random password."""
        characters = string.ascii_letters
        if include_digits:
            characters += string.digits
        if include_special:
            characters += string.punctuation
        
        if length < 8:
            print_colored("Avertissement: La longueur du mot de passe est faible. Minimum recommandé 8 caractères.", WARNING_COLOR)
        
        password = ''.join(random.choice(characters) for i in range(length))
        print_colored(f"Mot de passe généré: {password}", SUCCESS_COLOR)
        return password

    def check_hash(self, candidate_password, target_hash, algorithm='sha256'):
        """
        Checks if the hash of a candidate_password matches the target_hash.
        Returns True if they match, False otherwise.
        """
        try:
            hashed_candidate = self.hash_string(candidate_password, algorithm)
            if hashed_candidate and hashed_candidate == target_hash:
                print_colored(f"Match trouvé ! '{candidate_password}' correspond au hachage '{target_hash}'.", SUCCESS_COLOR)
                return True
            else:
                return False
        except Exception as e:
            print_colored(f"Erreur lors de la vérification du hachage : {e}", ERROR_COLOR)
            return False


