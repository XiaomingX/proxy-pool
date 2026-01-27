# ProxyPool Architect

Un pool de proxies moderno, rápido y fiable construido con Python 3.11+, FastAPI y Redis.

## Características
- **Stack Tecnológico Moderno**: FastAPI, aiohttp, Redis, APScheduler, Loguru.
- **Asíncrono**: Totalmente asíncrono desde el rastreo hasta la validación.
- **Puntuación Ponderada**: Gestión dinámica basada en puntuación (Éxito +10, Fallo -20).
- **Despliegue Fácil**: Gestionado por `uv`.

## Inicio Rápido

### 1. Instalar Redis (Prerrequisito)

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

### 2. Configuración

Cree un archivo `.env` en el directorio raíz para sobrescribir la configuración predeterminada si es necesario:
```env
REDIS_HOST=localhost
REDIS_PORT=6379
# REDIS_PASSWORD=tu_contraseña
```

### 3. Instalar y Ejecutar el Proyecto
Asegúrese de tener `uv` instalado ([Instalar uv](https://docs.astral.sh/uv/getting-started/installation/)).

```bash
uv sync
uv run main.py
```

## Endpoints de la API
- `GET /get`: Obtiene un proxy aleatorio de alta calidad. Soporta `format=text`.
- `GET /stats`: Ver el estado y las estadísticas del pool.
- `GET /all`: Lista todos los proxies en el pool.

## Construido con
![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)

---

## Despliegue con Docker

Este proyecto soporta el despliegue rápido a través de Docker y Docker Compose.

### 1. Usando Docker Compose (Recomendado)
Este es el método más sencillo, que inicia automáticamente los contenedores de Redis y ProxyPool:

```bash
docker-compose up -d
```

### 2. Construir solo la imagen de ProxyPool
Si ya tiene una instancia de Redis en ejecución:

```bash
# Construir la imagen
docker build -t proxy-pool .

# Ejecutar el contenedor (especificar la dirección de Redis)
docker run -d -p 8000:8000 -e REDIS_HOST=host.docker.internal proxy-pool
```

---

## Ejemplos de Uso Rápido

Obtener un proxy y acceder a Google con `curl`:

```bash
# 1. Obtener un proxy (formato de texto plano)
PROXY=$(curl -s http://localhost:8000/get?format=text)

# 2. Usar el proxy para acceder a un sitio web
curl -x "http://$PROXY" https://www.google.com -I
```

Uso en un script de Python:

```python
import httpx

# Obtener proxy
proxy = httpx.get("http://localhost:8000/get?format=text").text

# Usar proxy
proxies = {
    "http://": f"http://{proxy}",
    "https://": f"http://{proxy}",
}
response = httpx.get("https://www.google.com", proxies=proxies)
print(response.status_code)
```


## Funciones Principales

- Rastreo automático de IPs de proxy de múltiples fuentes
- Validación en tiempo real de la disponibilidad y velocidad de la IP del proxy
- Soporte para procesamiento por lotes y actualizaciones programadas
- Simple de usar y rápido de desplegar

## Instalación y Ejecución

1. Clonar este repositorio:

```
git clone https://github.com/XiaomingX/proxypool.git
cd proxypool
```

2. Instalar dependencias (asumiendo un entorno Python):

```
pip install -r requirements.txt
```

3. Ejecutar el script de rastreo de proxies:

```
python main.py
```

4. Ejecutar el script de validación de proxies:

```
python verify.py
```

## Proyectos de Ciberseguridad que te pueden interesar:
 - Escáner de puertos implementado en Rust:
   - https://github.com/XiaomingX/RustProxyHunter
 - Detección de Pool de Proxies implementado en Python:
   - https://github.com/XiaomingX/proxy-pool
 - Seguridad de la cadena de suministro y recolección automatizada de CVE-POC en Golang (Nota: Sin revisión manual):
   - https://github.com/XiaomingX/data-cve-poc
 - Herramienta de detección de fugas de .git implementada en Python:
   - https://github.com/XiaomingX/github-sensitive-hack

## Referencias e Inspiración

El diseño y la implementación de este proyecto se inspiraron en los siguientes excelentes proyectos de código abierto:

- [ProjectDiscovery Katana](https://github.com/projectdiscovery/katana) —— Un framework moderno de rastreo y spidering.
- [Spider-rs Spider](https://github.com/spider-rs/spider) —— Un framework de rastreo de alto rendimiento y escalable.

## Guía de Contribución

Siéntete libre de enviar issues y pull requests para ayudarnos a mejorar.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.

---

*¡Disfruta usando ProxyPool! Si tienes alguna pregunta, contacta con el autor.*
