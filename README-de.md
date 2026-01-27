# ProxyPool Architect

Ein moderner, schneller und zuverlässiger Proxy-Pool, entwickelt mit Python 3.11+, FastAPI und Redis.

## Funktionen
- **Moderner Tech-Stack**: FastAPI, aiohttp, Redis, APScheduler, Loguru.
- **Asynchron**: Vollständig asynchron vom Crawling bis zur Validierung.
- **Gewichtete Bewertung**: Dynamische punktbasierte Verwaltung (Erfolg +10, Fehler -20).
- **Einfache Bereitstellung**: Verwaltet durch `uv`.

## Schnellstart

### 1. Redis installieren (Voraussetzung)

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

### 2. Konfiguration

Erstellen Sie bei Bedarf eine `.env`-Datei im Stammverzeichnis, um die Standardeinstellungen zu überschreiben:
```env
REDIS_HOST=localhost
REDIS_PORT=6379
# REDIS_PASSWORD=ihr_passwort
```

### 3. Projekt installieren und ausführen
Stellen Sie sicher, dass `uv` installiert ist ([uv installieren](https://docs.astral.sh/uv/getting-started/installation/)).

```bash
uv sync
uv run main.py
```

## API-Endpunkte
- `GET /get`: Ruft einen zufälligen, hochwertigen Proxy ab. Unterstützt `format=text`.
- `GET /stats`: Zeigt den Status und die Statistiken des Pools an.
- `GET /all`: Listet alle Proxys im Pool auf.

## Erstellt mit
![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)

---

## Bereitstellung mit Docker

Dieses Projekt unterstützt die schnelle Bereitstellung über Docker und Docker Compose.

### 1. Docker Compose verwenden (Empfohlen)
Dies ist die einfachste Methode, die automatisch Redis- und ProxyPool-Container startet:

```bash
docker-compose up -d
```

### 2. Nur ProxyPool-Image erstellen
Wenn Sie bereits eine laufende Redis-Instanz haben:

```bash
# Image erstellen
docker build -t proxy-pool .

# Container ausführen (Redis-Adresse angeben)
docker run -d -p 8000:8000 -e REDIS_HOST=host.docker.internal proxy-pool
```

---

## Kurze Anwendungsbeispiele

Proxy abrufen und mit `curl` auf Google zugreifen:

```bash
# 1. Einen Proxy abrufen (Nur-Text-Format)
PROXY=$(curl -s http://localhost:8000/get?format=text)

# 2. Diesen Proxy verwenden, um eine Website aufzurufen
curl -x "http://$PROXY" https://www.google.com -I
```

Verwendung in einem Python-Skript:

```python
import httpx

# Proxy abrufen
proxy = httpx.get("http://localhost:8000/get?format=text").text

# Proxy verwenden
proxies = {
    "http://": f"http://{proxy}",
    "https://": f"http://{proxy}",
}
response = httpx.get("https://www.google.com", proxies=proxies)
print(response.status_code)
```


## Hauptfunktionen

- Automatisches Crawlen von Proxy-IPs aus mehreren Quellen
- Echtzeit-Validierung der Verfügbarkeit und Geschwindigkeit von Proxy-IPs
- Unterstützung für Stapelverarbeitung und geplante Aktualisierungen
- Einfach zu bedienen und schnell einsatzbereit

## Installation und Ausführung

1. Repository klonen:

```
git clone https://github.com/XiaomingX/proxypool.git
cd proxypool
```

2. Abhängigkeiten installieren (ausgehend von einer Python-Umgebung):

```
pip install -r requirements.txt
```

3. Proxy-Crawling-Skript ausführen:

```
python main.py
```

4. Proxy-Validierungsskript ausführen:

```
python verify.py
```

## Cybersicherheitsprojekte, die Sie interessieren könnten:
 - Port-Scanner in Rust:
   - https://github.com/XiaomingX/RustProxyHunter
 - Proxy-Pool-Erkennung in Python:
   - https://github.com/XiaomingX/proxy-pool
 - Lieferkettensicherheit & CVE-POC automatisierte Sammlung in Golang (Hinweis: Keine manuelle Überprüfung):
   - https://github.com/XiaomingX/data-cve-poc
 - .git Leak-Erkennungstool in Python:
   - https://github.com/XiaomingX/github-sensitive-hack

## Referenzen und Inspirationen

Das Design und die Implementierung dieses Projekts wurden von den folgenden exzellenten Open-Source-Projekten inspiriert:

- [ProjectDiscovery Katana](https://github.com/projectdiscovery/katana) —— Ein modernes Crawler- und Spider-Framework.
- [Spider-rs Spider](https://github.com/spider-rs/spider) —— Ein leistungsstarkes, skalierbares Crawler-Framework.

## Richtlinien für Beiträge

Gerne können Sie Issues und Pull-Requests einreichen, um uns bei der Verbesserung zu helfen.

## Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert. Weitere Details finden Sie in der LICENSE-Datei.

---

*Viel Spaß mit ProxyPool! Bei Fragen wenden Sie sich bitte an den Autor.*
