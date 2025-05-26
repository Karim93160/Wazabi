#!/bin/bash

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Chemins ABSOLUS
INSTALL_DIR="/data/data/com.termux/files/usr/bin"  # Le chemin global de Termux
WAZABI_ROOT=$(pwd)
BANNER_SOURCE="$WAZABI_ROOT/wazabi/banner/banner.txt"
BANNER_DEST="$INSTALL_DIR/wazabi_banner.txt"

echo -e "${BLUE}=== Installation FORCÉE de Wazabi ===${NC}"

# 1. Vérification Python
if ! command -v python3 &>/dev/null; then
    echo -e "${RED}ERREUR: Python3 requis !${NC}"
    echo -e "Installez-le avec: ${YELLOW}pkg install python${NC}"
    exit 1
fi

# 2. Installation dépendances
[ -f "requirements.txt" ] && {
    echo -e "${BLUE}Installation des dépendances...${NC}"
    pip install -r requirements.txt
}

# 3. COPIE FORCÉE du banner
echo -e "${BLUE}Copie du banner vers $INSTALL_DIR...${NC}"
if [ -f "$BANNER_SOURCE" ]; then
    cp "$BANNER_SOURCE" "$BANNER_DEST" && \
    chmod 644 "$BANNER_DEST" && \
    echo -e "${GREEN}Banner copié avec succès !${NC}"
else
    echo -e "${RED}ERREUR CRITIQUE: banner.txt introuvable !${NC}"
    echo -e "Il doit être dans: ${YELLOW}wazabi/banner/banner.txt${NC}"
    exit 1
fi

# 4. Création du WRAPPER DUR
echo -e "${BLUE}Création du wrapper système...${NC}"
cat > "$INSTALL_DIR/wazabi" <<EOF
#!/bin/bash
# Wrapper Dur pour Wazabi
BANNER_PATH="$BANNER_DEST"

if [ ! -f "\$BANNER_PATH" ]; then
    echo -e "${RED}ERREUR: Le banner système a disparu !${NC}" >&2
    exit 1
fi

# Exécution avec le chemin ABSOLU
python3 "$INSTALL_DIR/wazabi.py" "\$@"
EOF

# 5. Copie du script principal
echo -e "${BLUE}Installation du script principal...${NC}"
cp "wazabi.py" "$INSTALL_DIR/wazabi.py" && \
chmod +x "$INSTALL_DIR/wazabi.py" "$INSTALL_DIR/wazabi" && \
echo -e "${GREEN}Script installé dans $INSTALL_DIR${NC}"

# 6. Message final
echo -e "\n${GREEN}=== INSTALLATION RÉUSSIE ===${NC}"
echo -e "Vous pouvez maintenant utiliser:"
echo -e "  ${BLUE}wazabi${NC} ${GREEN}depuis n'importe où !${NC}"
echo -e "\nLe banner est FORCÉ à l'emplacement:"
echo -e "  ${YELLOW}$BANNER_DEST${NC}"
