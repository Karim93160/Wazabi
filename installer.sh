#!/bin/bash

# Couleurs pour les messages
GREEN='\033[0;32m'
NC='\033[0m' # No Color
YELLOW='\033[0;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'

# Configuration des chemins
REPO_NAME="wazabi"
DEFAULT_REPO_PATH="/data/data/com.termux/files/home/$REPO_NAME"
REPO_PATH="$DEFAULT_REPO_PATH"
INSTALL_DIR="/data/data/com.termux/files/usr/bin/"
BANNER_PATH="$REPO_PATH/wazabi/banner/banner.txt"

echo -e "${BLUE}=== Installation de Wazabi Shell ===${NC}"

# Vérification du répertoire Wazabi
if [ ! -d "$REPO_PATH" ]; then
  echo -e "${YELLOW}Le répertoire '$REPO_NAME' n'a pas été trouvé à l'emplacement par défaut.${NC}"
  read -p "Entrez le chemin complet du dépôt Wazabi (laissez vide pour '$DEFAULT_REPO_PATH') : " CUSTOM_REPO_PATH
  [ -n "$CUSTOM_REPO_PATH" ] && REPO_PATH="$CUSTOM_REPO_PATH"
fi

# Validation du script principal
if [ ! -f "$REPO_PATH/wazabi.py" ]; then
  echo -e "${RED}Erreur : wazabi.py introuvable dans '$REPO_PATH'${NC}"
  exit 1
fi

# Installation des dépendances
echo -e "${BLUE}Installation des dépendances Python...${NC}"
cd "$REPO_PATH" && pip install -r requirements.txt 2>/dev/null
[ $? -eq 0 ] && echo -e "${GREEN}Dépendances installées avec succès.${NC}" || echo -e "${YELLOW}Certaines erreurs sont survenues lors de l'installation.${NC}"

# Création des liens symboliques
echo -e "${BLUE}Configuration des liens symboliques...${NC}"

# Script principal
ln -sf "$REPO_PATH/wazabi.py" "$INSTALL_DIR/wazabi.py"
chmod +x "$INSTALL_DIR/wazabi.py"

# Banner
if [ -f "$BANNER_PATH" ]; then
  ln -sf "$BANNER_PATH" "$INSTALL_DIR/wazabi_banner.txt"
  echo -e "${GREEN}Banner configuré : $INSTALL_DIR/wazabi_banner.txt${NC}"
else
  echo -e "${YELLOW}Avertissement : banner.txt introuvable dans $BANNER_PATH${NC}"
fi

# Création du wrapper
echo -e "${BLUE}Création du wrapper d'exécution...${NC}"

cat > "$INSTALL_DIR/wazabi" <<EOF
#!/data/data/com.termux/files/usr/bin/bash
# Wrapper universel pour Wazabi
export WAZABI_ROOT_DIR="$REPO_PATH"
export WAZABI_BANNER_PATH="$INSTALL_DIR/wazabi_banner.txt"
exec python3 "$INSTALL_DIR/wazabi.py" "\$@"
EOF

chmod +x "$INSTALL_DIR/wazabi"

# Configuration du PATH
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
  echo -e "${BLUE}Configuration du PATH...${NC}"
  export PATH="$INSTALL_DIR:$PATH"
  echo "export PATH=\"$INSTALL_DIR:\$PATH\"" >> ~/.bashrc
  echo "export PATH=\"$INSTALL_DIR:\$PATH\"" >> ~/.zshrc 2>/dev/null
fi

# Rafraîchissement du shell
echo -e "${BLUE}Rafraîchissement de l'environnement...${NC}"
source ~/.bashrc 2>/dev/null || source ~/.zshrc 2>/dev/null

echo -e "${GREEN}\nInstallation terminée avec succès !${NC}"
echo -e "${GREEN}Vous pouvez maintenant utiliser Wazabi en tapant simplement :${NC}"
echo -e "  ${BLUE}wazabi${NC}"
echo -e "${GREEN}Le banner sera chargé depuis : ${YELLOW}$INSTALL_DIR/wazabi_banner.txt${NC}"
