#!/bin/bash

# Nom du script principal et du dossier racine
WAZABI_ROOT_DIR=$(pwd) # Obtient le répertoire courant où le script est exécuté
WAZABI_MAIN_SCRIPT="wazabi.py"
WAZABI_BANNER_PATH="$WAZABI_ROOT_DIR/wazabi/banner/banner.txt"  # Chemin complet vers le banner
# Répertoire d'installation pour le lien symbolique (Termux: $HOME/bin/)
INSTALL_DIR="$HOME/bin"
REQUIREMENTS_FILE="$WAZABI_ROOT_DIR/requirements.txt"

# Couleurs pour une meilleure lisibilité
COLOR_BLUE='\033[0;34m'
COLOR_GREEN='\033[0;32m'
COLOR_RED='\033[0;31m'
COLOR_YELLOW='\033[0;33m'
COLOR_CYAN='\033[0;36m'
COLOR_RESET='\033[0m' # Réinitialise la couleur

echo -e "${COLOR_CYAN}--- Démarrage de l'installation de Wazabi Shell ---${COLOR_RESET}"

# --- 0. Création du répertoire d'installation si nécessaire ---
echo -e "\n${COLOR_BLUE}Vérification et création du répertoire d'installation local ($INSTALL_DIR)...${COLOR_RESET}"
mkdir -p "$INSTALL_DIR"
if [ $? -ne 0 ]; then
    echo -e "${COLOR_RED}Erreur: Impossible de créer le répertoire '$INSTALL_DIR'. Veuillez vérifier vos permissions.${COLOR_RESET}"
    echo -e "${COLOR_RED}Installation incomplète. Assurez-vous que '$INSTALL_DIR' est inscriptible.${COLOR_RESET}"
    exit 1
fi
echo -e "${COLOR_GREEN}Répertoire '$INSTALL_DIR' prêt.${COLOR_RESET}"

# --- 1. Vérification et Installation des Prérequis Système (adapté pour Termux) ---
echo -e "\n${COLOR_BLUE}Vérification des prérequis système...${COLOR_RESET}"

# Vérifier si Python 3 est installé
if ! command -v python3 &> /dev/null
then
    echo -e "${COLOR_RED}Erreur: Python 3 n'est pas installé. Veuillez l'installer avec 'pkg install python' et réessayez.${COLOR_RESET}"
    return 1
fi

# Vérifier si pip est installé
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null
then
    echo -e "${COLOR_YELLOW}Avertissement: pip ou pip3 n'est pas trouvé. Veuillez l'installer avec 'pkg install python-pip' et réessayez.${COLOR_RESET}"
fi
echo -e "${COLOR_GREEN}Python 3 et pip sont disponibles.${COLOR_RESET}"

# --- 2. Installation des Dépendances Python ---
echo -e "\n${COLOR_BLUE}Installation des dépendances Python...${COLOR_RESET}"

if [ -f "$REQUIREMENTS_FILE" ]; then
    echo -e "${COLOR_BLUE}Installation des dépendances listées dans '$REQUIREMENTS_FILE'...${COLOR_RESET}"
    pip install -r "$REQUIREMENTS_FILE"
    if [ $? -eq 0 ]; then
        echo -e "${COLOR_GREEN}Toutes les dépendances Python ont été installées avec succès.${COLOR_RESET}"
    else
        echo -e "${COLOR_RED}Erreur lors de l'installation des dépendances Python. Veuillez vérifier les erreurs ci-dessus.${COLOR_RESET}"
        return 1
    fi
else
    echo -e "${COLOR_YELLOW}Avertissement: Le fichier 'requirements.txt' n'a pas été trouvé.${COLOR_RESET}"
fi

# --- 3. Donner les autorisations d'exécution aux scripts Python ---
echo -e "\n${COLOR_BLUE}Attribution des permissions d'exécution aux scripts Python...${COLOR_RESET}"

# Donner les permissions à wazabi.py
chmod +x "$WAZABI_ROOT_DIR/$WAZABI_MAIN_SCRIPT"
if [ $? -eq 0 ]; then
    echo -e "${COLOR_GREEN}Permissions accordées à '$WAZABI_MAIN_SCRIPT'.${COLOR_RESET}"
else
    echo -e "${COLOR_RED}Erreur lors de l'attribution des permissions à '$WAZABI_MAIN_SCRIPT'.${COLOR_RESET}"
fi

# --- 4. Configuration de la commande 'wazabi' ---
echo -e "\n${COLOR_BLUE}Configuration de la commande 'wazabi'...${COLOR_RESET}"

# Création du script wrapper dans le répertoire d'installation
WRAPPER_SCRIPT="$INSTALL_DIR/wazabi"
echo -e "${COLOR_BLUE}Création du wrapper '$WRAPPER_SCRIPT'...${COLOR_RESET}"

cat << EOF > "$WRAPPER_SCRIPT"
#!/bin/bash
# Wrapper pour Wazabi Shell
export WAZABI_BANNER_PATH="$WAZABI_BANNER_PATH"
export PYTHONPATH="$WAZABI_ROOT_DIR:\$PYTHONPATH"
python3 "$WAZABI_ROOT_DIR/$WAZABI_MAIN_SCRIPT" "\$@"
EOF

# Rendre le wrapper exécutable
chmod +x "$WRAPPER_SCRIPT"
if [ $? -ne 0 ]; then
    echo -e "${COLOR_RED}Erreur: Impossible de rendre le wrapper exécutable.${COLOR_RESET}"
    return 1
fi
echo -e "${COLOR_GREEN}Wrapper créé avec succès.${COLOR_RESET}"

# --- 5. Configuration du banner.txt ---
echo -e "\n${COLOR_BLUE}Configuration du fichier banner...${COLOR_RESET}"

if [ -f "$WAZABI_BANNER_PATH" ]; then
    echo -e "${COLOR_GREEN}Fichier banner trouvé à: $WAZABI_BANNER_PATH${COLOR_RESET}"
    # Le wrapper exportera automatiquement cette variable
else
    echo -e "${COLOR_YELLOW}Avertissement: Fichier banner non trouvé à $WAZABI_BANNER_PATH${COLOR_RESET}"
fi

# --- 6. Configuration du PATH ---
echo -e "\n${COLOR_BLUE}Configuration du PATH...${COLOR_RESET}"

# Vérifier si le script est sourcé
if [[ $- == *i* ]]; then
    # Mode interactif (sourcé)
    if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
        export PATH="$INSTALL_DIR:$PATH"
        echo -e "${COLOR_GREEN}Répertoire '$INSTALL_DIR' ajouté au PATH pour cette session.${COLOR_RESET}"
    fi
else
    # Mode non-interactif
    echo -e "${COLOR_YELLOW}Pour une utilisation permanente, ajoutez ceci à votre ~/.bashrc ou ~/.zshrc:${COLOR_RESET}"
    echo -e "  ${COLOR_GREEN}export PATH=\"$INSTALL_DIR:\$PATH\"${COLOR_RESET}"
fi

# --- 7. Instructions finales ---
echo -e "\n${COLOR_GREEN}--- Installation terminée avec succès ! ---${COLOR_RESET}"
echo -e "${COLOR_GREEN}Vous pouvez maintenant utiliser Wazabi avec la commande:${COLOR_RESET}"
echo -e "  ${COLOR_CYAN}wazabi${COLOR_RESET}"
echo -e "\n${COLOR_YELLOW}Si la commande n'est pas reconnue immédiatement:${COLOR_RESET}"
echo -e "1. Soit exécutez: ${COLOR_CYAN}source $WAZABI_ROOT_DIR/installer.sh${COLOR_RESET}"
echo -e "2. Soit redémarrez votre terminal"
echo -e "\n${COLOR_GREEN}Profitez de Wazabi Shell !${COLOR_RESET}"
