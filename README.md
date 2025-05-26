# 🌶️ Wazabi Shell : Le Sanctuaire du Hacker Éthique 🛡️

![Wazabi Shell Banner](banner/banner.txt)
*(Affiche la bannière animée en ASCII art, générée dynamiquement par l'outil)*

## Table des Matières

1.  [À Propos de Wazabi Shell](#-à-propos-de-wazabi-shell-)
2.  [Philosophie Wazabi](#-philosophie-wazabi-)
3.  [Fonctionnalités Clés](#-fonctionnalités-clés-)
4.  [Installation](#-installation-)
    * [Cloner le Dépôt](#cloner-le-dépôt)
    * [Exécuter l'Installer](#exécuter-linstaller)
    * [Vérification de l'Installation](#vérification-de-linstallation)
5.  [Utilisation](#-utilisation-)
    * [Lancer le Shell Interactif](#lancer-le-shell-interactif)
    * [Exécuter une Commande Directe](#exécuter-une-commande-directe)
    * [Commandes Disponibles et Aide](#commandes-disponibles-et-aide)
6.  [Dépendances](#-dépendances-)
7.  [Contribuer](#-contribuer-)
8.  [Licence](#-licence-)
9.  [Contact](#-contact-)

---

## 🌟 À Propos de Wazabi Shell 🌟

Wazabi Shell est bien plus qu'un simple outil en ligne de commande ; c'est un **sanctuaire intégré et interactif** pour le professionnel de la cybersécurité éthique. Conçu avec la **précision, la connaissance et l'innovation** comme piliers, Wazabi offre un environnement unifié pour exécuter une multitude de tâches d'audit de sécurité, d'analyse de données et de gestion de systèmes, le tout depuis un unique prompt.

Fini les allers-retours entre divers scripts et outils. Wazabi te permet de concentrer ta puissance intellectuelle et technique en un seul point, fluidifiant ton workflow et augmentant ton efficacité dans le respect des principes éthiques.

## 🌿 Philosophie Wazabi 🌿

Inspiré par le "piment" (Wasabi en japonais), notre philosophie repose sur trois piliers fondamentaux :

* **Protection 🛡️ :** Détecter les vulnérabilités, renforcer les défenses, et garantir la sécurité des systèmes avec responsabilité.
* **Connaissance 📚 :** Analyser, comprendre et interpréter les données pour prendre des décisions éclairées et anticiper les menaces.
* **Innovation ✨ :** Développer des solutions intelligentes et efficaces, repoussant les limites de la cybersécurité avec créativité.

Wazabi est un engagement envers la pratique éthique du hacking, en mettant l'accent sur la découverte proactive des faiblesses pour un monde numérique plus sûr.

## 🚀 Fonctionnalités Clés 🚀

Wazabi Shell est organisé en modules logiques, chacun regroupant des commandes spécifiques :

* **`file` (Gestion des Flux) :** Opérations robustes de copie, déplacement, suppression, listage et recherche de fichiers et répertoires.
* **`network` (Maîtrise du Réseau) :** Requêtes HTTP (GET, POST), téléchargement de fichiers, et un scanner de ports rapide pour cartographier les infrastructures.
* **`data` (Traitement des Informations) :** Lecture/écriture de fichiers CSV et JSON, et transformation de contenu texte (majuscules, minuscules, inversion, ROT13).
* **`db` (Interaction avec le Savoir Stocké) :** Gestion d'une base de données SQLite interne pour le suivi des URLs traitées et l'exécution de requêtes SQL personnalisées (avec prudence !).
* **`security` (Art de la Discrétion) :** Fonctions de hachage (MD5, SHA-256, SHA-512), encodage/décodage Base64, génération de mots de passe robustes, et **vérification de correspondance de hachages**.
* **`wazabi` (Piment Wazabi - Exploration Avancée) :**
    * **`port_scan` :** Scanner de ports intégré (alias de `network scan_ports`).
    * **`analyze_dir` :** Analyse approfondie des répertoires pour détecter des fichiers volumineux ou sensibles.
    * **`generate_payload` :** Création de payloads textuels personnalisables pour le fuzzing et les tests d'injection.
    * **`dict_attack` :** **Nouvelle fonctionnalité !** Attaque par dictionnaire pour tenter de craquer des hachages de mots de passe en utilisant des listes de mots.
* **`config` (Ajustement des Paramètres) :** Permet de visualiser, définir, sauvegarder et charger les paramètres de configuration du shell pour une expérience personnalisée.

## ⚙️ Installation ⚙️

L'installation de Wazabi Shell est simple et rapide grâce à notre script `installer.sh`.

### Cloner le Dépôt

Commencez par cloner le dépôt GitHub dans le répertoire de votre choix :

```bash
git clone [https://github.com/Karim93160/wazabi.git](https://github.com/Karim93160/wazabi.git)
cd wazabi

