[English](README.md) | [Русский](README.RU.md) | [Українська](README.UK.md) | [Português](README.PT.md) | [Deutsch](README.DE.md) | Français

# 🎬 YouTube Downloader

Télécharge des **vidéos (mp4)**, de l'**audio (mp3)** et des **transcriptions textuelles** (à partir des sous-titres) depuis YouTube — au choix, ou tout à la fois. Deux interfaces :

- **CLI** — `download.py`, un outil en console écrit en Python ;
- **Interface Web** — `web_server.py` (Flask) + `web_ui.html` (JS dans le navigateur) : barre de progression, journal de téléchargement, liste des fichiers avec liens de téléchargement.

![YouTube Downloader](Screeshot/YouTubDownloader.png)

Langues de l'interface : **English, Русский, Українська, Português, Deutsch, Français**.

Licence : **MIT** — utilisation libre sans restriction (voir [LICENSE](LICENSE)).

## Fonctionnalités

- 🎥 Vidéo en qualité maximale (1080p / 1440p / 4K via flux DASH fusionnés avec ffmpeg), moyenne ou basse
- 🎧 Audio seul, converti en mp3 (192 kbps) — idéal pour l'écoute en déplacement
- 📄 Transcription textuelle des sous-titres (nettoyée des codes temporels et des balises) enregistrée à côté du fichier média
- 🌍 Choix de la langue de la piste audio et des sous-titres (`--lang ru`, `en`, …) ; la piste russe est prioritaire sur les vidéos multilingues
- 🔁 Protection contre les doublons : les vidéos déjà téléchargées sont ignorées (un journal basé sur les ID est tenu)
- 📝 Journal de téléchargement en deux formats : `download_log.txt` et `download_log.html`
- 🖥️ Interface Web : informations sur la vidéo avant téléchargement, progression en direct, historique, téléchargement des fichiers directement depuis le navigateur
- 🌐 Langue de l'interface modifiable en CLI comme dans l'interface Web (6 langues, détection automatique par défaut)

## Structure du dépôt

```
├── download.py            # Téléchargeur CLI (logique principale)
├── web_server.py          # Serveur Web (API Flask + sert l'interface)
├── web_ui.html            # Interface Web (HTML/JS)
├── i18n.py                # Moteur de langue de l'interface
├── locales/               # Traductions : en, ru, uk, pt, de, fr
├── requirements.txt       # Dépendances Python
├── Screeshot/             # Capture d'écran utilisée dans les README
├── .github/workflows/     # GitHub Actions : téléchargement sans installation locale
├── .devcontainer/         # Configuration GitHub Codespaces
└── legacy/                # Anciennes versions du script (historique de développement)
```

Les fichiers téléchargés vont dans `downloads/`, le journal se trouve à la racine du projet. Ces deux chemins (ainsi que les fichiers personnels) sont exclus de git via `.gitignore`.

## Installation (locale)

### 1. Prérequis

- **Python 3.10+** (testé sur 3.12)
- **ffmpeg** — nécessaire pour fusionner les flux DASH (qualité au-delà de 720p) et convertir en mp3. Sans lui, le programme fonctionne quand même, mais la vidéo est limitée à 720p (progressive) et l'audio reste dans son format d'origine (m4a)

### 2. Installation de ffmpeg

| OS | Commande |
|---|---|
| macOS | `brew install ffmpeg` |
| Ubuntu / Debian | `sudo apt install ffmpeg` |
| Windows | `winget install Gyan.FFmpeg` (ou `choco install ffmpeg`), puis redémarrer le terminal |

Vérification : `ffmpeg -version`

### 3. Clonage et dépendances

```bash
git clone https://github.com/YOUR_LOGIN/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY

python3 -m venv .venv
source .venv/bin/activate        # Windows : .venv\Scripts\activate
pip install -r requirements.txt
```

## Utilisation : CLI

### Mode interactif

```bash
python download.py
```

Pose les questions étape par étape : URL → qualité → langue → faut-il enregistrer le mp3.

### Avec arguments

```bash
python download.py "https://youtu.be/XXXX" max          # vidéo de meilleure qualité + transcription
python download.py "https://youtu.be/XXXX" audio        # mp3 seul + transcription
python download.py "https://youtu.be/XXXX" medium --lang en
python download.py "https://youtu.be/XXXX" max --mp3 -o video   # + mp3, dossier video/
python download.py "https://youtu.be/XXXX" max --ui-lang de     # interface en allemand
```

| Argument | Signification |
|---|---|
| `url` | URL de la vidéo (sans elle — mode interactif) |
| `quality` | `max` / `medium` / `low` / `audio` |
| `--lang`, `-l` | langue de l'audio et de la transcription (par défaut : `ru`) |
| `--mp3` | enregistrer en plus une piste mp3 à côté du mp4 |
| `-o`, `--output` | dossier de sortie (par défaut : `downloads`) |
| `--ui-lang`, `-u` | langue de l'interface : `en`/`ru`/`uk`/`pt`/`de`/`fr` |

La langue de l'interface est détectée automatiquement depuis les paramètres régionaux du système (`LANG`/`LC_ALL`) ; utilisez `--ui-lang` pour forcer le choix, ou définissez la variable d'environnement `YTD_LANG`.

Aide complète : `python download.py --help`

Résultat dans `downloads/` :

```
Titre de la vidéo.mp4            # vidéo (ou .mp3 en mode audio)
Titre de la vidéo.mp3            # avec --mp3 ou quality=audio
Titre de la vidéo.transcript.txt # transcription des sous-titres
```

## Utilisation : interface Web

```bash
python web_server.py
```

Ouvrez **http://127.0.0.1:5000** dans votre navigateur :

1. Collez un lien → **« Obtenir les infos »** : miniature, auteur, durée, résolutions disponibles, présence de sous-titres, statut (« nouveau » / « déjà téléchargée »)
2. Choisissez la qualité et la langue → **« Télécharger »** : barre de progression en direct et journal console
3. En dessous — la liste des fichiers prêts (téléchargez-les directement depuis le navigateur) et le journal complet des téléchargements

La langue de l'interface se choisit avec le sélecteur 🌐 en haut à droite ; le choix est mémorisé dans le navigateur. Le journal de téléchargement et la sortie console suivent eux aussi la langue sélectionnée.

L'hôte et le port peuvent être modifiés via des variables d'environnement :

```bash
HOST=0.0.0.0 PORT=8080 python web_server.py
```

## Exécution directement sur GitHub

Un site statique (GitHub Pages) ne fonctionnera pas ici — un backend Python est indispensable. Deux options fonctionnelles à la place.

### Option 1 : GitHub Actions (sans installation locale)

Le dépôt contient un workflow à déclenchement manuel `.github/workflows/download.yml` :

1. Ouvrez l'onglet **Actions** → **Download YouTube video** → **Run workflow**
2. Renseignez l'URL, la qualité (`max`/`medium`/`low`/`audio`), la langue du contenu, la langue de l'interface et la nécessité du mp3
3. Attendez la fin → le résumé de l'exécution affiche l'**artefact `youtube-download`** — téléchargez le zip avec vos fichiers

Rien n'est stocké dans le dépôt : l'exécution livre uniquement le fichier média lui-même (mp4/mp3) sous forme d'artefact éphémère (1 jour). Téléchargez le zip depuis le résumé de l'exécution ; pour les transcriptions et les journaux, exécutez l'outil localement.

⚠️ **Limites** : les artefacts sont conservés une durée limitée (1 jour ici), la taille est plafonnée, et YouTube bloque souvent les IP de datacenters (l'erreur « Sign in to confirm you're not a bot »). Pour un usage régulier, exécutez localement.

### Option 2 : GitHub Codespaces (interface Web complète dans le cloud)

1. Bouton **Code** → onglet **Codespaces** → **Create codespace on master**
2. Le conteneur est configuré via `.devcontainer/devcontainer.json` : Python 3.12, ffmpeg, dépendances — installés automatiquement
3. Dans le terminal : `python web_server.py` — le port 5000 est transféré automatiquement et le navigateur s'ouvre tout seul

Pour info : le quota gratuit de Codespaces pour les comptes GitHub personnels est de 120 heures-cœur par mois — largement suffisant pour un usage occasionnel.

## Journal de téléchargement

Chaque téléchargement ajoute une entrée :

- `download_log.txt` — journal lisible par machine (utilisé pour détecter les « déjà téléchargées ») ;
- `download_log.html` — un tableau lisible avec des liens.

Pour retélécharger une vidéo, supprimez son ID de `download_log.txt` (et le fichier de `downloads/`).

## Dépannage

| Problème | Solution |
|---|---|
| La vidéo se télécharge en 720p maximum | ffmpeg introuvable → fusion DASH indisponible. Installez ffmpeg et vérifiez `ffmpeg -version` |
| « Sign in to confirm you're not a bot » | YouTube bloque votre IP (souvent avec les VPN/datacenters). Essayez un autre réseau ou exécutez localement |
| Pas de mp3, un `.m4a` subsiste | ffmpeg n'est pas installé — conversion impossible, le flux audio d'origine a été conservé |
| Pas de transcription | La vidéo n'a pas de sous-titres. Les sous-titres auto-générés par YouTube sont également pris en charge quand ils existent |
| « Address already in use » au démarrage de l'interface Web | Sur macOS, le port 5000 est souvent occupé par AirPlay (Centre de contrôle) — utilisez un autre port : `PORT=8080 python web_server.py` |
| pytubefix cesse de fonctionner après une mise à jour de YouTube | `pip install -U pytubefix` — la bibliothèque est corrigée activement au fil des changements de YouTube |

## Licence

[MIT](LICENSE) — utilisation, copie, modification et distribution libres, y compris à des fins commerciales.

⚠️ **Note juridique** : ce programme est destiné au téléchargement de contenu dont vous détenez les droits (votre propre contenu, contenu sous licence ouverte, ou téléchargement autorisé dans votre juridiction). Respectez les conditions d'utilisation de YouTube et le droit d'auteur.
