# ProxyPool Architect

Python 3.11+, FastAPI 및 Redis를 기반으로 구축된 현대적이고 빠르며 신뢰할 수 있는 프록시 풀입니다.

## 특징
- **현대적인 기술 스택**: FastAPI, aiohttp, Redis, APScheduler, Loguru.
- **비동기 방식**: 크롤링부터 검증까지 완전한 비동기 처리.
- **가중치 기반 점수 관리**: 동적 점수 기반 관리 (성공 +10, 실패 -20).
- **쉬운 배포**: `uv`를 통한 관리.

## 빠른 시작

### 1. Redis 설치 (사전 요구 사항)

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

### 2. 설정

필요한 경우 기본 설정을 재정의하기 위해 루트 디렉토리에 `.env` 파일을 생성합니다:
```env
REDIS_HOST=localhost
REDIS_PORT=6379
# REDIS_PASSWORD=your_password
```

### 3. 프로젝트 설치 및 실행
`uv`가 설치되어 있는지 확인하세요 ([uv 설치하기](https://docs.astral.sh/uv/getting-started/installation/)).

```bash
uv sync
uv run main.py
```

## API 엔드포인트
- `GET /get`: 고품질의 랜덤 프록시를 가져옵니다. `format=text`를 지원합니다.
- `GET /stats`: 풀의 상태 및 통계를 확인합니다.
- `GET /all`: 풀에 있는 모든 프록시를 나열합니다.

## 사용된 기술
![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)

---

## Docker를 이용한 배포

이 프로젝트는 Docker 및 Docker Compose를 통한 빠른 배포를 지원합니다.

### 1. Docker Compose 사용 (권장)
가장 간단한 방법으로, Redis와 ProxyPool 컨테이너를 자동으로 시작합니다:

```bash
docker-compose up -d
```

### 2. ProxyPool 이미지만 빌드
이미 실행 중인 Redis가 있는 경우:

```bash
# 이미지 빌드
docker build -t proxy-pool .

# 컨테이너 실행 (Redis 주소 지정 필요)
docker run -d -p 8000:8000 -e REDIS_HOST=host.docker.internal proxy-pool
```

---

## 빠른 사용 예시

프록시를 가져와서 `curl`로 Google에 접속하기:

```bash
# 1. 프록시 가져오기 (텍스트 형식)
PROXY=$(curl -s http://localhost:8000/get?format=text)

# 2. 해당 프록시를 사용하여 웹사이트 접속
curl -x "http://$PROXY" https://www.google.com -I
```

Python 스크립트에서 사용:

```python
import httpx

# 프록시 가져오기
proxy = httpx.get("http://localhost:8000/get?format=text").text

# 프록시 사용
proxies = {
    "http://": f"http://{proxy}",
    "https://": f"http://{proxy}",
}
response = httpx.get("https://www.google.com", proxies=proxies)
print(response.status_code)
```


## 주요 기능

- 여러 소스에서 프록시 IP 자동 수집
- 프록시 IP의 가용성 및 속도 실시간 검증
- 배치 처리 및 예약된 업데이트 지원
- 사용하기 쉽고 빠른 배포

## 설치 및 실행

1. 저장소 클론:

```
git clone https://github.com/XiaomingX/proxypool.git
cd proxypool
```

2. 종속성 설치 (Python 환경 기준):

```
pip install -r requirements.txt
```

3. 프록시 수집 스크립트 실행:

```
python main.py
```

4. 프록시 검증 스크립트 실행:

```
python verify.py
```

## 관심이 있을 만한 사이버 보안 프로젝트:
 - Rust로 구현된 포트 스캐너:
   - https://github.com/XiaomingX/RustProxyHunter
 - Python으로 구현된 프록시 풀 탐지:
   - https://github.com/XiaomingX/proxy-pool
 - Golang으로 구현된 공급망 보안 및 CVE-POC 자동 수집 (주의: 수동 검토 없음):
   - https://github.com/XiaomingX/data-cve-poc
 - Python으로 구현된 .git 유출 탐지 도구:
   - https://github.com/XiaomingX/github-sensitive-hack

## 참고 및 영감의 원천

이 프로젝트의 디자인과 구현은 다음의 우수한 오픈 소스 프로젝트에서 영감을 받았습니다:

- [ProjectDiscovery Katana](https://github.com/projectdiscovery/katana) —— 현대적인 크롤러 및 스파이더 프레임워크.
- [Spider-rs Spider](https://github.com/spider-rs/spider) —— 고성능의 확장 가능한 크롤러 프레임워크.

## 기여 가이드

개선을 위한 이슈 및 풀 리퀘스트 제출을 환영합니다.

## 라이선스

이 프로젝트는 MIT 라이선스에 따라 라이선스가 부여됩니다. 자세한 내용은 LICENSE 파일을 참조하십시오.

---

*ProxyPool을 즐겁게 사용하세요! 궁금한 점이 있으면 작성자에게 문의하십시오.*
