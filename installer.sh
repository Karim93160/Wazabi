#!/bin/bash

# Configuration des chemins
WAZABI_ROOT_DIR=$(pwd)
WAZABI_MAIN_SCRIPT="wazabi.py"
WAZABI_BANNER_FILE="$WAZABI_ROOT_DIR/wazabi/banner/banner.txt"
INSTALL_DIR="$HOME/bin"
REQUIREMENTS_FILE="$WAZABI_ROOT_DIR/requirements.txt"

# Couleurs pour le terminal
COLOR_BLUE='\033[0;34m'
COLOR_GREEN='\033[0;32m'
COLOR_RED='\033[0;31m'
COLOR_YELLOW='\033[0;33m'
COLOR_CYAN='\033[0;36m'
COLOR_RESET='\033[0m'

echo -e "${COLOR_CYAN}=== Installation de Wazabi Shell ===${COLOR_RESET}"

# 1. Vérification des prérequis
echo -e "\n${COLOR_BLUE}Vérification des prérequis...${COLOR_RESET}"

# Vérification Python
if ! command -v python3 &>/dev/null; then
    echo -e "${COLOR_RED}Python3 n'est pas installé. Installez-le avec: pkg install python${COLOR_RESET}"
    exit 1
fi

# Vérification pip
if ! command -v pip &>/dev/null && ! command -v pip3 &>/dev/null; then
    echo -e "${COLOR_YELLOW}pip n'est pas installé. Installez-le avec: pkg install python-pip${COLOR_RESET}"
fi

# 2. Installation des dépendances
if [ -f "$REQUIREMENTS_FILE" ]; then
    echo -e "\n${COLOR_BLUE}Installation des dépendances Python...${COLOR_RESET}"
    pip install -r "$REQUIREMENTS_FILE" || {
        echo -e "${COLOR_RED}Erreur lors de l'installation des dépendances${COLOR_RESET}"
        exit 1
    }
fi

# 3. Création du répertoire d'installation
mkdir -p "$INSTALL_DIR" || {
    echo -e "${COLOR_RED}Impossible de créer $INSTALL_DIR${COLOR_RESET}"
    exit 1
}

# 4. Création du wrapper universel
echo -e "\n${COLOR_BLUE}Création de la commande 'wazabi'...${COLOR_RESET}"

cat > "$INSTALL_DIR/wazabi" << EOF
#!/bin/bash
# Wrapper universel pour Wazabi Shell
export WAZABI_ROOT_DIR="$WAZABI_ROOT_DIR"
export WAZABI_BANNER_PATH="$WAZABI_BANNER_FILE"
export PYTHONPATH="$WAZABI_ROOT_DIR:\$PYTHONPATH"
exec python3 "$WAZABI_ROOT_DIR/$WAZABI_MAIN_SCRIPT" "\$@"
EOF

chmod +x "$INSTALL_DIR/wazabi" || {
    echo -e "${COLOR_RED}Erreur lors de la création du wrapper${COLOR_RESET}"
    exit 1
}

# 5. Configuration du PATH
echo -e "\n${COLOR_BLUE}Configuration de l'environnement...${COLOR_RESET}"

# Ajout au PATH si pas déjà présent
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    export PATH="$INSTALL_DIR:$PATH"
    echo -e "${COLOR_GREEN}Ajout de $INSTALL_DIR au PATH${COLOR_RESET}"
    
    # Ajout permanent dans .bashrc ou .zshrc
    SHELL_RC="$HOME/.bashrc"
    [ -f "$HOME/.zshrc" ] && SHELL_RC="$HOME/.zshrc"
    
    if ! grep -q "export PATH=\"$INSTALL_DIR:\$PATH\"" "$SHELL_RC"; then
        echo -e "\n# Wazabi Shell Path" >> "$SHELL_RC"
        echo "export PATH=\"$INSTALL_DIR:\$PATH\"" >> "$SHELL_RC"
        echo -e "${COLOR_GREEN}Configuration permanente ajoutée à $SHELL_RC${COLOR_RESET}"
    fi
fi

# 6. Rafraîchissement automatique du shell
echo -e "\n${COLOR_BLUE}Rafraîchissement de l'environnement...${COLOR_RESET}"
if [ -n "$BASH" ]; then
    source ~/.bashrc 2>/dev/null || source ~/.bash_profile
elif [ -n "$ZSH_VERSION" ]; then
    source ~/.zshrc
fi

# 7. Vérification finale
echo -e "\n${COLOR_GREEN}=== Installation réussie ! ===${COLOR_RESET}"
echo -e "Vous pouvez maintenant utiliser: ${COLOR_CYAN}wazabi${COLOR_RESET} depuis n'importe où"
echo -e "Le banner sera toujours chargé depuis: ${COLOR_YELLOW}$WAZABI_BANNER_FILE${COLOR_RESET}"

# Test automatique
if command -v wazabi &>/dev/null; then
    echo -e "\n${COLOR_GREEN}Test: La commande 'wazabi' est maintenant disponible !${COLOR_RESET}"
else
    echo -e "\n${COLOR_YELLOW}Attention: Pour que la commande soit disponible, exécutez:${COLOR_RESET}"
    echo -e "source ~/.bashrc  # ou source ~/.zshrc selon votre shell"
fi
