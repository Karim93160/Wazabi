#!/bin/bash

# Nom du script principal et du dossier racine
WAZABI_ROOT_DIR=$(pwd)  # Obtient le répertoire courant où le script est exécuté
WAZABI_MAIN_SCRIPT="wazabi.py"
INSTALL_DIR="$HOME/bin"
REQUIREMENTS_FILE="$WAZABI_ROOT_DIR/requirements.txt"
BANNER_DIR="$WAZABI_ROOT_DIR/banner"
BANNER_FILE="$BANNER_DIR/banner.txt"

# Couleurs pour une meilleure lisibilité
COLOR_BLUE='\033[0;34m'
COLOR_GREEN='\033[0;32m'
COLOR_RED='\033[0;31m'
COLOR_YELLOW='\033[0;33m'
COLOR_CYAN='\033[0;36m'
COLOR_RESET='\033[0m' 

echo -e "${COLOR_CYAN}--- Démarrage de l'installation de Wazabi Shell ---${COLOR_RESET}"

# --- 0. Création du répertoire d'installation ---
echo -e "\n${COLOR_BLUE}Vérification et création du répertoire d'installation local ($INSTALL_DIR)...${COLOR_RESET}"
mkdir -p "$INSTALL_DIR"
if [ $? -ne 0 ]; then
    echo -e "${COLOR_RED}Erreur: Impossible de créer le répertoire '$INSTALL_DIR'.${COLOR_RESET}"
    exit 1
fi

# --- 1. Vérification et Installation des Prérequis ---
echo -e "\n${COLOR_BLUE}Vérification des prérequis système...${COLOR_RESET}"
if ! command -v python3 &> /dev/null; then
    echo -e "${COLOR_RED}Python 3 n'est pas installé. Installe-le avec 'pkg install python'.${COLOR_RESET}"
    exit 1
fi
if ! command -v pip &> /dev/null; then
    echo -e "${COLOR_YELLOW}pip n'est pas trouvé. Installe-le avec 'pkg install python-pip'.${COLOR_RESET}"
    exit 1
fi

# --- 2. Installation des dépendances Python ---
echo -e "\n${COLOR_BLUE}Installation des dépendances Python...${COLOR_RESET}"
if [ -f "$REQUIREMENTS_FILE" ]; then
    pip install -r "$REQUIREMENTS_FILE"
fi

# --- 3. Attribution des permissions ---
echo -e "\n${COLOR_BLUE}Attribution des permissions d'exécution...${COLOR_RESET}"
chmod +x "$WAZABI_ROOT_DIR/$WAZABI_MAIN_SCRIPT"
MODULES_DIR="$WAZABI_ROOT_DIR/modules"
if [ -d "$MODULES_DIR" ]; then
    find "$MODULES_DIR" -name "*.py" -exec chmod +x {} \;
fi

# --- 4. Création du script wrapper pour l’exécution globale ---
WRAPPER_SCRIPT_PATH="$INSTALL_DIR/wazabi"
echo -e "\n${COLOR_BLUE}Configuration de l'exécution globale...${COLOR_RESET}"
cat << EOF > "$WRAPPER_SCRIPT_PATH"
#!/bin/bash
python3 "$WAZABI_ROOT_DIR/$WAZABI_MAIN_SCRIPT" "\$@"
EOF
chmod +x "$WRAPPER_SCRIPT_PATH"

# --- 5. Vérification et gestion du banner ---
echo -e "\n${COLOR_BLUE}Vérification du fichier banner...${COLOR_RESET}"
if [ ! -f "$BANNER_FILE" ]; then
    echo -e "${COLOR_YELLOW}Avertissement: banner.txt introuvable dans '$BANNER_DIR'.${COLOR_RESET}"
fi

# --- 6. Ajout à PATH si nécessaire ---
echo -e "\n${COLOR_BLUE}Vérification du PATH...${COLOR_RESET}"
if ! echo "$PATH" | grep -q "$INSTALL_DIR"; then
    echo "export PATH=\$HOME/bin:\$PATH" >> $HOME/.bashrc
    source $HOME/.bashrc
fi

echo -e "\n${COLOR_GREEN}Installation terminée ! Tu peux lancer Wazabi avec : 'wazabi'${COLOR_RESET}"
