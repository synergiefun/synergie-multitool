# ⚡ SYNERGIE MULTITOOL V1

<p align="center">
  <strong>🚀 PC DIAGNOSTIC • NETWORK • PUBLIC OSINT • UTILITIES</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/VERSION-1.0-00DDAA?style=for-the-badge" />
  <img src="https://img.shields.io/badge/PYTHON-3.10+-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/PLATFORM-WINDOWS-0078D6?style=for-the-badge&logo=windows" />
  <img src="https://img.shields.io/badge/LICENSE-MIT-green?style=for-the-badge" />
</p>

---

## 🖥️ Présentation

**Synergie MultiTool V1** est un outil multifonction développé en Python, conçu pour regrouper plusieurs fonctionnalités informatiques dans une seule interface terminal.

Son objectif est de proposer un ensemble d'outils pratiques pour le diagnostic PC, l'analyse réseau, l'OSINT public et la gestion de fichiers.

### ✨ Fonctionnalités principales

| Catégorie | Fonctionnalités |
|---|---:|
| 🖥️ Système | 7 |
| 🌐 Réseau | 7 |
| 🔎 OSINT public | 9 |
| 📁 Fichiers | 4 |
| 🛠️ Utilitaires | 3 |
| **TOTAL** | **30** |

---

## 🔎 Liste des fonctionnalités

### 🖥️ 01 — SYSTEM

- Informations détaillées du PC
- Affichage des processus
- Analyse du stockage
- Informations sur la batterie
- Applications au démarrage
- État de sécurité Windows
- Informations système et environnement

### 🌐 02 — NETWORK

- Affichage des adresses IP locales
- Recherche de l'adresse IP publique
- Recherche DNS
- Test Ping
- Traceroute
- Vérification d'un port unique
- Informations sur les cartes réseau

### 🔎 03 — PUBLIC OSINT

- Informations publiques sur une adresse IP
- Informations de domaine RDAP
- Analyse des en-têtes HTTP
- Vérification des certificats SSL/TLS
- Consultation de robots.txt et sitemap.xml
- Recherche publique de pseudonymes
- Recherche web d'adresses e-mail
- Validation de numéros de téléphone
- Recherche multi-moteurs

### 📁 04 — FILES

- Calcul de hash SHA-256
- Consultation des métadonnées
- Analyse avec Microsoft Defender
- Exploration de dossiers

### 🛠️ 05 — UTILITIES

- Lecteur JSON
- Générateur de mots de passe
- Exportation et consultation des rapports

---

## 📥 Installation

### Méthode automatique

1. Téléchargez `Synergie_MultiTool_V1_Installateur_EXE.zip`.
2. Extrayez le contenu du ZIP.
3. Installez Python 3.10 ou supérieur si nécessaire.
4. Lancez `INSTALLER.bat`.
5. Attendez l'installation des dépendances et la compilation.

Votre exécutable sera créé automatiquement dans :

`dist/Synergie MultiTool V1.exe`

### Installation manuelle

```bash
py -m pip install psutil dnspython phonenumbers pyinstaller
```

Lancement du programme :

```bash
py Synergie_MultiTool_V1.py
```

---

## ⚙️ Configuration requise

| Composant | Configuration |
|---|---|
| OS | Windows 10 / 11 |
| Python | 3.10 ou supérieur |
| RAM | 4 Go recommandés |
| Connexion | Internet pour les fonctions en ligne |
| Stockage | Quelques dizaines de Mo |

---

## 🛡️ Sécurité et utilisation

Synergie MultiTool est destiné au diagnostic informatique et à la consultation d'informations publiques.

Les fonctions réseau et OSINT doivent être utilisées uniquement dans un cadre légal, sur vos propres équipements ou avec une autorisation.

Aucune fonction ne doit servir à accéder à des comptes, systèmes ou données privés sans permission.

---

## 📂 Structure du projet

```text
Synergie-MultiTool/
│
├── Synergie_MultiTool_V1.py
├── INSTALLER.bat
├── SynergieLogo.ico
├── requirements.txt
├── LISEZ-MOI.txt
└── README.md
```

---

## 🚀 Développé par

**SYNERGIE COMMUNITY**

Créateur : [@synergiefun](https://github.com/synergiefun)

Projet : Synergie MultiTool V1

---

<p align="center">
  ⚡ <strong>SYNERGIE MULTITOOL</strong>
  <br/>
  <i>One Tool. Multiple Possibilities.</i>
</p>
