#!/bin/bash

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Chemins absolus
WAZABI_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
INSTALL_DIR="$HOME/bin"
BANNER_RELATIVE="wazabi/banner/banner.txt"
BANNER_ABSOLUTE="$WAZABI_ROOT/$BANNER_RELATIVE"

echo -e "${BLUE}=== Installation Wazabi Shell ===${NC}"

# 1. Vérification Python
if ! command -v python3 &>/dev/null; then
    echo -e "${RED}ERREUR: Python3 requis. Installez-le avec: pkg install python${NC}"
    exit 1
fi

# 2. Création du répertoire bin
mkdir -p "$INSTALL_DIR" || {
    echo -e "${RED}ERREUR: Impossible de créer $INSTALL_DIR${NC}"
    exit 1
}

# 3. Installation dépendances
[ -f "requirements.txt" ] && {
    pip install -r requirements.txt || echo -e "${YELLOW}ATTENTION: Certaines dépendances n'ont pas pu s'installer${NC}"
}

# 4. Création du wrapper intelligent
cat > "$INSTALL_DIR/wazabi" <<EOF
#!/bin/bash
# Wrapper Universel Wazabi
WAZABI_ROOT="$WAZABI_ROOT"
BANNER_PATH="$BANNER_ABSOLUTE"

# Vérification et chargement du banner
if [ -f "\$BANNER_PATH" ]; then
    export WAZABI_BANNER="\$(cat "\$BANNER_PATH")"
else
    echo -e "${YELLOW}ATTENTION: Banner introuvable à \$BANNER_PATH${NC}" >&2
fi

# Exécution du script principal
exec python3 "\$WAZABI_ROOT/wazabi.py" "\$@"
EOF

chmod +x "$INSTALL_DIR/wazabi"

# 5. Configuration du PATH
grep -q "$INSTALL_DIR" ~/.bashrc || echo "export PATH=\"$INSTALL_DIR:\$PATH\"" >> ~/.bashrc
[ -f ~/.zshrc ] && grep -q "$INSTALL_DIR" ~/.zshrc || echo "export PATH=\"$INSTALL_DIR:\$PATH\"" >> ~/.zshrc

# 6. Message final
echo -e "\n${GREEN}=== Installation réussie ! ==="
echo -e "Commandes disponibles:"
echo -e "  ${BLUE}wazabi${NC} - Lancer le shell"
echo -e "\nEmplacement du banner:"
echo -e "  ${YELLOW}$BANNER_ABSOLUTE${NC}"

if [ ! -f "$BANNER_ABSOLUTE" ]; then
    echo -e "\n${RED}ERREUR: Le fichier banner.txt est introuvable à l'emplacement ci-dessus${NC}"
    exit 1
fi
