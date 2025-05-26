#!/bin/bash

# Nom du script principal et du dossier racine
WAZABI_ROOT_DIR=$(pwd) # Obtient le répertoire courant où le script est exécuté
WAZABI_MAIN_SCRIPT="wazabi.py"
# Répertoire d'installation pour le lien symbolique, généralement $HOME/bin/ sur Termux
# ou ~/.local/bin/ sur d'autres systèmes Linux pour installations sans sudo
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
    return 1 # Utiliser return au lieu de exit si le script est sourcé
fi

# Vérifier si pip est installé. Si non, suggérer de l'installer avec pkg.
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null
then
    echo -e "${COLOR_YELLOW}Avertissement: pip ou pip3 n'est pas trouvé. Veuillez l'installer avec 'pkg install python-pip' et réessayez.${COLOR_RESET}"
    # Ne pas sortir ici, car l'utilisateur pourrait avoir pip dans son PATH après une installation manuelle.
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
    echo -e "${COLOR_YELLOW}Avertissement: Le fichier 'requirements.txt' n'a pas été trouvé à '$REQUIREMENTS_FILE'. Aucune dépendance Python spécifique ne sera installée.${COLOR_RESET}"
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

# Donner les permissions à tous les modules Python
MODULES_DIR="$WAZABI_ROOT_DIR/modules"
if [ -d "$MODULES_DIR" ]; then
    echo -e "${COLOR_BLUE}Attribution des permissions aux fichiers Python dans '$MODULES_DIR'...${COLOR_RESET}"
    find "$MODULES_DIR" -name "*.py" -exec chmod +x {} \;
    if [ $? -eq 0 ]; then
        echo -e "${COLOR_GREEN}Permissions accordées à tous les fichiers Python dans '$MODULES_DIR'.${COLOR_RESET}"
    else
        echo -e "${COLOR_RED}Erreur lors de l'attribution des permissions aux modules.${COLOR_RESET}"
    fi
else
    echo -e "${COLOR_YELLOW}Avertissement: Le dossier '$MODULES_DIR' n'existe pas. Aucune permission n'a été changée pour les modules.${COLOR_RESET}"
fi


# --- 4. Rendre Wazabi exécutable comme une commande ---
echo -e "\n${COLOR_BLUE}Configuration de la commande 'wazabi' dans votre PATH...${COLOR_RESET}"

# Chemin du script wrapper
WRAPPER_SCRIPT_PATH="$INSTALL_DIR/wazabi_wrapper.sh"

# Créer le script wrapper
echo -e "${COLOR_BLUE}Création du script wrapper '$WRAPPER_SCRIPT_PATH'...${COLOR_RESET}"
cat << EOF > "$WRAPPER_SCRIPT_PATH"
#!/bin/bash
# Ce script lance Wazabi Shell en utilisant python3.
# Il transmet tous les arguments au script principal.
python3 "$WAZABI_ROOT_DIR/$WAZABI_MAIN_SCRIPT" "\$@"
EOF

# Rendre le script wrapper exécutable
chmod +x "$WRAPPER_SCRIPT_PATH"
if [ $? -ne 0 ]; then
    echo -e "${COLOR_RED}Erreur: Impossible de rendre le script wrapper '$WRAPPER_SCRIPT_PATH' exécutable.${COLOR_RESET}"
    echo -e "${COLOR_RED}Installation incomplète. Veuillez vérifier vos permissions sur '$INSTALL_DIR'.${COLOR_RESET}"
    rm -f "$WRAPPER_SCRIPT_PATH" # Nettoyage si échec
    return 1
fi
echo -e "${COLOR_GREEN}Script wrapper rendu exécutable.${COLOR_RESET}"

# Créer le lien symbolique
echo -e "${COLOR_BLUE}Création du lien symbolique 'wazabi' dans '$INSTALL_DIR'...${COLOR_RESET}"
rm -f "$INSTALL_DIR/wazabi" # Supprimer l'ancien lien symbolique s'il existe
ln -s "$WRAPPER_SCRIPT_PATH" "$INSTALL_DIR/wazabi"

if [ $? -ne 0 ]; then
    echo -e "${COLOR_RED}Erreur: Impossible de créer le lien symbolique pour 'wazabi'.${COLOR_RESET}"
    echo -e "${COLOR_RED}Vérifiez vos permissions sur '$INSTALL_DIR'.${COLOR_RESET}"
    echo -e "${COLOR_RED}Vous devrez lancer Wazabi manuellement avec 'python3 $WAZABI_ROOT_DIR/$WAZABI_MAIN_SCRIPT'.${COLOR_RESET}"
    rm -f "$WRAPPER_SCRIPT_PATH" # Nettoyage si échec du lien
    return 1
fi
echo -e "${COLOR_GREEN}Lien symbolique '$INSTALL_DIR/wazabi' créé avec succès.${COLOR_RESET}"

# --- 5. Configuration automatique du PYTHONPATH et PATH (si le script est sourcé) ---
echo -e "\n${COLOR_BLUE}Configuration des variables d'environnement pour Wazabi...${COLOR_RESET}"

# Vérifier si le script est sourcé
if [[ -z "$BASH_SOURCE" || "$BASH_SOURCE" == "$0" ]]; then
    # Le script n'est pas sourcé, il est exécuté directement.
    # Dans ce cas, nous ne pouvons pas modifier le PATH et PYTHONPATH de la session courante.
    # Nous allons seulement ajouter les instructions pour l'utilisateur.
    IS_SOURCED=false
else
    # Le script est sourcé, nous pouvons modifier le PATH et PYTHONPATH de la session courante.
    IS_SOURCED=true
fi

# Ajout du répertoire des exécutables de Wazabi au PATH
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
  if [ "$IS_SOURCED" = true ]; then
    export PATH="$INSTALL_DIR:$PATH"
    echo -e "${COLOR_GREEN}Répertoire '$INSTALL_DIR' ajouté à votre \$PATH pour cette session.${COLOR_RESET}"
  else
    echo -e "${COLOR_YELLOW}Ajoutez 'export PATH=\"$INSTALL_DIR:\$PATH\"' à votre fichier de configuration de shell pour une disponibilité permanente.${COLOR_RESET}"
  fi
else
    echo -e "${COLOR_YELLOW}Le répertoire '$INSTALL_DIR' est déjà dans votre \$PATH.${COLOR_RESET}"
fi

# Ajout du répertoire racine de Wazabi au PYTHONPATH
if [[ ":$PYTHONPATH:" != *":$WAZABI_ROOT_DIR:"* ]]; then
  if [ "$IS_SOURCED" = true ]; then
    export PYTHONPATH="$WAZABI_ROOT_DIR:$PYTHONPATH"
    echo -e "${COLOR_GREEN}Répertoire racine de Wazabi ajouté à votre \$PYTHONPATH pour cette session.${COLOR_RESET}"
  else
    echo -e "${COLOR_YELLOW}Ajoutez 'export PYTHONPATH=\"$WAZABI_ROOT_DIR:\$PYTHONPATH\"' à votre fichier de configuration de shell pour une disponibilité permanente.${COLOR_RESET}"
  fi
else
    echo -e "${COLOR_YELLOW}Le répertoire racine de Wazabi est déjà dans votre \$PYTHONPATH.${COLOR_RESET}"
fi


# --- 6. Instructions Post-Installation pour l'activation ---
echo -e "\n${COLOR_YELLOW}--- Instructions Importantes Post-Installation ---${COLOR_RESET}"
echo -e "${COLOR_YELLOW}L'installation de Wazabi Shell est terminée.${COLOR_RESET}"

if [ "$IS_SOURCED" = true ]; then
    echo -e "${COLOR_GREEN}Wazabi est maintenant prêt à l'emploi dans cette session !${COLOR_RESET}"
    echo -e "${COLOR_GREEN}Pour lancer le shell: ${COLOR_CYAN}wazabi${COLOR_RESET}"
    echo -e "${COLOR_GREEN}Pour exécuter une commande directe: ${COLOR_CYAN}wazabi file list -p .${COLOR_RESET}"
    echo -e "${COLOR_YELLOW}Pour que Wazabi soit disponible dans toutes vos futures sessions Termux, veuillez ajouter la ligne suivante à votre ${HOME}/.bashrc (ou .zshrc) :${COLOR_RESET}"
    echo -e "  ${COLOR_GREEN}source $WAZABI_ROOT_DIR/installer.sh${COLOR_RESET}"
    echo -e "${COLOR_YELLOW}  (Ceci garantira que les variables d'environnement sont toujours définies au démarrage).${COLOR_RESET}"
else
    echo -e "${COLOR_YELLOW}Pour que 'wazabi' fonctionne ${COLOR_GREEN}immédiatement${COLOR_YELLOW} dans votre session actuelle, vous devez lancer l'installateur différemment :${COLOR_RESET}"
    echo -e "  ${COLOR_GREEN}source installer.sh${COLOR_RESET}"
    echo -e "${COLORYELLOW}Ceci configurera les chemins nécessaires pour Wazabi dans votre session actuelle.${COLOR_RESET}"
    echo -e "${COLOR_YELLOW}Pour que Wazabi soit disponible dans ${COLOR_GREEN}toutes vos futures sessions Termux${COLOR_YELLOW} :${COLOR_RESET}"
    echo -e "${COLOR_CYAN}  Ajoutez la ligne ${COLOR_GREEN}source $WAZABI_ROOT_DIR/installer.sh${COLOR_CYAN} à votre ${HOME}/.bashrc ou ${HOME}/.zshrc.${COLOR_RESET}"
    echo -e "${COLOR_CYAN}  (Si vous ne l'ajoutez pas, vous devrez sourcer manuellement à chaque nouvelle session).${COLOR_RESET}"
fi

echo -e "\n${COLOR_GREEN}Installation de Wazabi Shell terminée avec succès !${COLOR_RESET}"
echo -e "${COLOR_GREEN}Profitez bien de votre Wazabi Shell pimenté !${COLOR_RESET}"

