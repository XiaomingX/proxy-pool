# ProxyPool Architect

Un pool de proxys moderne, rapide et fiable construit avec Python 3.11+, FastAPI et Redis.

## Caractéristiques
- **Stack Technique Moderne** : FastAPI, aiohttp, Redis, APScheduler, Loguru.
- **Asynchrone** : Entièrement asynchrone, de la collecte à la validation.
- **Scoring Pondéré** : Gestion dynamique basée sur le score (Succès +10, Échec -20).
- **Déploiement Facile** : Géré par `uv`.

## Démarrage Rapide

### 1. Installer Redis (Prérequis)

#### macOS
```bash
brew install redis
brew services start redis
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis-server
```

### 2. Configuration

Créez un fichier `.env` dans le répertoire racine pour écraser les paramètres par défaut si nécessaire :
```env
REDIS_HOST=localhost
REDIS_PORT=6379
# REDIS_PASSWORD=votre_mot_de_passe
```

### 3. Installer et Lancer le Projet
Assurez-vous d'avoir `uv` installé ([Installer uv](https://docs.astral.sh/uv/getting-started/installation/)).

```bash
uv sync
uv run main.py
```

## Points de Terminaison de l'API
- `GET /get` : Récupère un proxy aléatoire de haute qualité. Supporte `format=text`.
- `GET /stats` : Affiche l'état de santé et les statistiques du pool.
- `GET /all` : Liste tous les proxys du pool.

## Construit avec
![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)

---

## Déploiement avec Docker

Ce projet supporte un déploiement rapide via Docker et Docker Compose.

### 1. Utiliser Docker Compose (Recommandé)
C'est la méthode la plus simple, qui démarre automatiquement les conteneurs Redis et ProxyPool :

```bash
docker-compose up -d
```

### 2. Construire uniquement l'image ProxyPool
Si vous avez déjà une instance Redis en cours d'exécution :

```bash
# Construire l'image
docker build -t proxy-pool .

# Lancer le conteneur (spécifier l'adresse Redis)
docker run -d -p 8000:8000 -e REDIS_HOST=host.docker.internal proxy-pool
```

---

## Exemples d'Utilisation Rapide

Récupérer un proxy et accéder à Google avec `curl` :

```bash
# 1. Récupérer un proxy (format texte brut)
PROXY=$(curl -s http://localhost:8000/get?format=text)

# 2. Utiliser ce proxy pour accéder à un site web
curl -x "http://$PROXY" https://www.google.com -I
```

Utilisation dans un script Python :

```python
import requests

# Récupérer le proxy
proxy = requests.get("http://localhost:8000/get?format=text").text

# Utiliser le proxy
proxies = {
    "http": f"http://{proxy}",
    "https": f"http://{proxy}",
}
response = requests.get("https://www.google.com", proxies=proxies)
print(response.status_code)
```


## Fonctions Principales

- Collecte automatique d'IPs de proxy à partir de plusieurs sources
- Validation en temps réel de la disponibilité et de la vitesse de l'IP du proxy
- Support du traitement par lots et des mises à jour planifiées
- Simple à utiliser et rapide à déployer

## Installation et Exécution

1. Cloner ce dépôt :

```
git clone https://github.com/XiaomingX/proxypool.git
cd proxypool
```

2. Installer les dépendances (en supposant un environnement Python) :

```
pip install -r requirements.txt
```

3. Lancer le script de collecte de proxys :

```
python main.py
```

4. Lancer le script de validation de proxys :

```
python verify.py
```

## Projets de Cybersécurité qui pourraient vous intéresser :
 - Scanner de ports implémenté en Rust :
   - https://github.com/XiaomingX/RustProxyHunter
 - Détection de pool de proxys implémentée en Python :
   - https://github.com/XiaomingX/proxy-pool
 - Sécurité de la chaîne d'approvisionnement & collecte automatisée de CVE-POC en Golang (Note : Pas de révision manuelle) :
   - https://github.com/XiaomingX/data-cve-poc
 - Outil de détection de fuites .git implémenté en Python :
   - https://github.com/XiaomingX/github-sensitive-hack

## Références et Inspiration

La conception et l'implémentation de ce projet ont été inspirées par les excellents projets open-source suivants :

- [ProjectDiscovery Katana](https://github.com/projectdiscovery/katana) —— Un framework moderne de crawling et de spidering.
- [Spider-rs Spider](https://github.com/spider-rs/spider) —— Un framework de crawling haute performance et évolutif.

## Guide de Contribution

N'hésitez pas à soumettre des issues et des pull requests pour nous aider à nous améliorer.

## Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

---

*Profitez bien de ProxyPool ! Si vous avez des questions, n'hésitez pas à contacter l'auteur.*
