![SYNERGIE Multitool](assets/synergie-banner.png)

# SYNERGIE Multitool — V6.1

Multitool Python en français, avec interface terminal Rich, animation de démarrage et outils regroupés par catégories : OSINT public, réseau, sécurité locale, Discord, téléphonie, système et utilitaires.

> **Projet éducatif.** Utilisez les fonctions OSINT uniquement sur des informations publiques et dans le respect des lois, des conditions des services et de la vie privée. Les diagnostics de sécurité doivent être réalisés sur des systèmes que vous possédez ou êtes autorisé à tester.

## Sommaire

- [Fonctionnalités](#fonctionnalités)
- [Télécharger la version Windows EXE](#télécharger-la-version-windows-exe)
- [Lancer depuis le code source](#lancer-depuis-le-code-source)
- [Construire le EXE sous Windows](#construire-le-exe-sous-windows)
- [Publier sur GitHub](#publier-sur-github)
- [Sécurité et confidentialité](#sécurité-et-confidentialité)
- [Dépannage](#dépannage)

## Fonctionnalités

- **01–12 — OSINT public :** recherche de pseudos et de sources publiques, outils de recherche web, vérifications de domaine et métadonnées de fichiers locaux.
- **13–17 — Réseau :** DNS, IP/domaine, test TCP et diagnostics locaux.
- **18–22 — Sécurité PC :** accès aux outils locaux de sécurité, analyse de dossiers et audit statique de scripts.
- **23–32 — Discord :** ressources et outils publics, liens, webhooks et assistant de génération d'un projet de bot.
- **33–44 — Téléphone :** validation de format, normalisation, indicatifs et utilitaires de contact.
- **45–57 — Système et utilitaires :** rapports, informations système, calculatrice, encodage et outils texte.
- **58 — Aide :** explication d'une option par son numéro.
- **00 — Quitter.**

Les résultats OSINT dépendent des sources publiques et ne prouvent pas à eux seuls l'identité d'une personne, la propriété d'un compte ou l'attribution d'un numéro. L'application ne peut pas révéler de façon fiable l'identité privée d'un titulaire de téléphone ni sa position en temps réel.

## Télécharger la version Windows EXE

Le fichier EXE est produit par GitHub Actions sur un runner Windows. Pour l'obtenir :

1. Ouvrez l'onglet **Actions** du dépôt GitHub.
2. Sélectionnez le workflow **Build Windows EXE**.
3. Ouvrez la dernière exécution réussie.
4. En bas, téléchargez l'artefact **SYNERGIE-Windows-x64**.
5. Décompressez l'archive ZIP et lancez `SYNERGIE.exe`.

Vous pouvez aussi créer une version publiée en créant une étiquette Git `v6.1.0` (voir ci-dessous). Windows Defender ou SmartScreen peut afficher un avertissement pour un EXE non signé : ne lancez que les fichiers que vous avez compilés ou dont vous avez vérifié la provenance.

## Lancer depuis le code source

Python 3.10 ou plus récent est recommandé. Sous Windows, ouvrez CMD dans le dossier du projet puis exécutez :

```bat
py -m venv .venv
.venv\Scripts\activate
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
py synergie_multitool.py
```

Sous macOS/Linux, activez l'environnement avec `source .venv/bin/activate`, puis lancez `python synergie_multitool.py`.

## Construire le EXE sous Windows

Prérequis : Python installé depuis python.org ou le Microsoft Store, avec le lanceur `py` disponible.

Double-cliquez sur `build_windows.bat` ou lancez-le dans CMD :

```bat
build_windows.bat
```

Le programme final se trouvera dans `dist\SYNERGIE.exe`. L'application garde la console visible pour afficher l'interface terminal. L'icône est définie par `assets\synergie.ico`.

Construction manuelle équivalente :

```bat
py -m pip install --upgrade pip
py -m pip install -r requirements.txt pyinstaller
py -m PyInstaller --clean --noconfirm SYNERGIE.spec
```

## Publier sur GitHub

1. Connectez-vous à GitHub et créez un dépôt vide, par exemple `synergie-multitool`. Ne cochez pas l'option de création automatique du README si vous importez déjà ce dossier.
2. Décompressez le paquet du projet et ouvrez un terminal dans ce dossier.
3. Initialisez Git et poussez le projet :

```bash
git init
git add .
git commit -m "Publie SYNERGIE Multitool V6.1"
git branch -M main
git remote add origin https://github.com/VOTRE-PSEUDO/synergie-multitool.git
git push -u origin main
```

Remplacez `VOTRE-PSEUDO` par votre nom GitHub et adaptez l'URL au dépôt créé.

Après le push, ouvrez **Actions** et autorisez les workflows si GitHub vous le demande. Le workflow construit automatiquement le programme Windows et conserve le fichier comme artefact téléchargeable.

### Créer une Release GitHub

Après avoir poussé `main`, créez et poussez un tag :

```bash
git tag v6.1.0
git push origin v6.1.0
```

Le workflow construit `SYNERGIE.exe` sur Windows et l'attache à une Release GitHub. Vérifiez la Release avant de la partager.

## Sécurité et confidentialité

- **Ne publiez jamais** un token Discord, une clé API, un mot de passe, un fichier `.env` ou des données personnelles. Le `.gitignore` exclut ces fichiers courants, mais vérifiez toujours `git status` avant un push.
- Les URL de webhook Discord sont des secrets : quiconque les possède peut publier dans le salon lié. Si une URL est exposée, supprimez/régénérez le webhook.
- Les fonctions réseau ne doivent viser que des systèmes que vous possédez ou êtes autorisé à tester.
- Les recherches OSINT ne doivent pas servir au harcèlement, au doxxing, à la surveillance non consentie ou à contourner les contrôles d'accès.
- L'EXE n'est pas signé numériquement. La signature et la réputation SmartScreen sont distinctes de la compilation.

## Dépannage

- **`py` n'est pas reconnu :** installez Python 3 depuis [python.org](https://www.python.org/downloads/windows/) et cochez l'ajout au PATH, ou utilisez `python` à la place de `py`.
- **Module manquant :** activez le bon environnement puis lancez `py -m pip install -r requirements.txt`.
- **Le EXE se ferme trop vite :** lancez-le depuis CMD pour lire le message d'erreur.
- **Le bot Discord ne se connecte pas :** suivez le README généré dans le dossier du bot et gardez le token dans le fichier `.env` local, jamais dans GitHub.
- **Les résultats DNS ou OSINT sont incomplets :** vérifiez votre connexion Internet et gardez à l'esprit que les sources publiques ne couvrent pas tout.

## Licence

Le projet est distribué sous licence MIT. Consultez [LICENSE](LICENSE).
