#!/bin/bash

# Couleurs
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# Chemins absolus
WAZABI_ROOT=$(pwd)
INSTALL_DIR="$HOME/bin"
BANNER_PATH="$WAZABI_ROOT/wazabi/banner/banner.txt"

echo -e "${BLUE}=== Installation Wazabi Shell ===${NC}"

# 1. Vérification des prérequis
if ! command -v python3 &>/dev/null; then
    echo -e "${RED}Python3 requis. Installez-le avec: pkg install python${NC}"
    exit 1
fi

# 2. Création du répertoire bin si nécessaire
mkdir -p "$INSTALL_DIR"

# 3. Installation des dépendances
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt || echo -e "${YELLOW}Attention lors de l'installation des dépendances${NC}"
fi

# 4. Création du wrapper intelligent
cat > "$INSTALL_DIR/wazabi" <<EOF
#!/bin/bash
# Wrapper universel Wazabi
WAZABI_ROOT="$WAZABI_ROOT"
BANNER_PATH="$BANNER_PATH"

# Vérification du banner
if [ ! -f "\$BANNER_PATH" ]; then
    echo -e "${YELLOW}Avertissement: banner.txt introuvable à \$BANNER_PATH${NC}" >&2
else
    export WAZABI_BANNER_PATH="\$BANNER_PATH"
fi

# Exécution du script principal
exec python3 "\$WAZABI_ROOT/wazabi.py" "\$@"
EOF

chmod +x "$INSTALL_DIR/wazabi"

# 5. Configuration du PATH
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    echo "export PATH=\"$INSTALL_DIR:\$PATH\"" >> ~/.bashrc
    [ -f ~/.zshrc ] && echo "export PATH=\"$INSTALL_DIR:\$PATH\"" >> ~/.zshrc
fi

# 6. Vérification finale
if [ -f "$BANNER_PATH" ]; then
    echo -e "${GREEN}Banner configuré: $BANNER_PATH${NC}"
else
    echo -e "${YELLOW}Avertissement: banner.txt non trouvé à l'emplacement attendu${NC}"
fi

echo -e "${GREEN}Installation terminée avec succès !${NC}"
echo -e "Utilisez la commande: ${BLUE}wazabi${NC}"
