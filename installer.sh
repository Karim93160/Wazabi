#!/bin/bash

# Définition des couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Définition des chemins
INSTALL_DIR="/data/data/com.termux/files/usr/bin"
WAZABI_ROOT="$(cd "$(dirname "$0")" && pwd)"
BANNER_SOURCE="$WAZABI_ROOT/banner/banner.txt"
BANNER_DEST="$INSTALL_DIR/banner.txt"

echo -e "${BLUE}=== Installation de Wazabi ===${NC}"

# 📌 Vérification de la présence de banner.txt
if [ ! -f "$BANNER_SOURCE" ]; then
    echo -e "${RED}ERREUR: banner.txt est introuvable dans ./banner/banner.txt${NC}"
    echo -e "Contenu actuel du dossier banner:"
    ls -l "$WAZABI_ROOT/banner/"
    exit 1
fi

# 📌 Vérification de Python3
if ! command -v python3 &>/dev/null; then
    echo -e "${RED}Python3 requis: pkg install python${NC}"
    exit 1
fi

# 📌 Installation des dépendances si requirements.txt existe
if [ -f "$WAZABI_ROOT/requirements.txt" ]; then
    echo -e "${BLUE}Installation des dépendances...${NC}"
    pip install -r "$WAZABI_ROOT/requirements.txt"
fi

# 📌 Copie du banner sous le bon nom
echo -e "${BLUE}Installation du banner...${NC}"
cp "$BANNER_SOURCE" "$BANNER_DEST" || {
    echo -e "${RED}Échec de la copie du banner!${NC}"
    exit 1
}

# 📌 Copie du fichier wazabi.py dans bin
echo -e "${BLUE}Installation des fichiers exécutables...${NC}"
cp "$WAZABI_ROOT/wazabi.py" "$INSTALL_DIR/wazabi.py" || {
    echo -e "${RED}Échec de la copie de wazabi.py!${NC}"
    exit 1
}

# 📌 Création du wrapper wazabi
echo -e "${BLUE}Création du wrapper Wazabi...${NC}"
cat > "$INSTALL_DIR/wazabi" <<EOF
#!/bin/bash
BANNER="/data/data/com.termux/files/usr/bin/banner.txt"

if [ ! -f "\$BANNER" ]; then
    echo -e "${RED}ERREUR: Banner introuvable! Réinstallez.${NC}" >&2
    exit 1
fi

exec python3 "/data/data/com.termux/files/usr/bin/wazabi.py" "\$@"
EOF

chmod +x "$INSTALL_DIR/wazabi"

# 📌 Vérification finale
echo -e "\n${GREEN}=== INSTALLATION TERMINÉE ===${NC}"
echo -e "Testez immédiatement avec:"
echo -e "  ${BLUE}wazabi${NC}"
echo -e "Le banner est installé à:"
echo -e "  ${YELLOW}$BANNER_DEST${NC}"
