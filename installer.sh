#!/bin/bash

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Chemins ABSOLUS
INSTALL_DIR="/data/data/com.termux/files/usr/bin"
WAZABI_ROOT=$(pwd)
BANNER_SOURCE="$WAZABI_ROOT/banner/banner.txt"  # MODIFICATION ICI
BANNER_DEST="$INSTALL_DIR/wazabi_banner.txt"

echo -e "${BLUE}=== Installation Wazabi ULTIME ===${NC}"

# 1. Vérification du banner AVANT tout
if [ ! -f "$BANNER_SOURCE" ]; then
    echo -e "${RED}ERREUR: banner.txt doit être dans ./banner/banner.txt${NC}"
    echo -e "Structure actuelle:"
    ls -R --color=auto banner/
    exit 1
fi

# 2. Vérification Python
if ! command -v python3 &>/dev/null; then
    echo -e "${RED}Python3 requis: pkg install python${NC}"
    exit 1
fi

# 3. Installation dépendances
[ -f "requirements.txt" ] && pip install -r requirements.txt

# 4. COPIE DU BANNER
echo -e "${BLUE}Installation du banner système...${NC}"
cp -v "$BANNER_SOURCE" "$BANNER_DEST" || {
    echo -e "${RED}Échec de la copie du banner!${NC}"
    exit 1
}

# 5. INSTALLATION DES FICHIERS
echo -e "${BLUE}Installation des exécutables...${NC}"
cp -v wazabi.py "$INSTALL_DIR/wazabi.py" || {
    echo -e "${RED}Échec copie wazabi.py!${NC}"
    exit 1
}

# 6. CREATION DU WRAPPER
cat > "$INSTALL_DIR/wazabi" <<EOF
#!/bin/bash
# Wrapper Garanti
BANNER="/data/data/com.termux/files/usr/bin/wazabi_banner.txt"

if [ ! -f "\$BANNER" ]; then
    echo -e "${RED}ERREUR: Banner manquant! Réinstallez.${NC}" >&2
    exit 1
fi

exec python3 "/data/data/com.termux/files/usr/bin/wazabi.py" "\$@"
EOF

chmod +x "$INSTALL_DIR/wazabi"

# 7. VERIFICATION FINALE
echo -e "\n${GREEN}=== INSTALLATION RÉUSSIE ===${NC}"
echo -e "Testez immédiatement avec:"
echo -e "  ${BLUE}wazabi${NC}"
echo -e "\nEmplacement garantie du banner:"
echo -e "  ${YELLOW}$BANNER_DEST${NC}"
