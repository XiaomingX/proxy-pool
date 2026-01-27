# ProxyPool Architect

Python 3.11+、FastAPI、および Redis で構築された、モダンで高速かつ信頼性の高いプロキシプール。

## 特徴
- **モダンな技術スタック**: FastAPI, aiohttp, Redis, APScheduler, Loguru。
- **非同期**: クローリングから検証まで完全に非同期。
- **重み付けスコアリング**: 動的なスコアベース管理（成功 +10、失敗 -20）。
- **簡単なデプロイ**: `uv` による管理。

## クイックスタート

### 1. Redis のインストール (必須)

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

### 2. 設定

必要に応じて、ルートディレクトリに `.env` ファイルを作成してデフォルト設定を上書きします：
```env
REDIS_HOST=localhost
REDIS_PORT=6379
# REDIS_PASSWORD=your_password
```

### 3. プロジェクトのインストールと実行
`uv` がインストールされていることを確認してください ([uv のインストール](https://docs.astral.sh/uv/getting-started/installation/))。

```bash
uv sync
uv run main.py
```

## API エンドポイント
- `GET /get`: 高品質なランダムプロキシを取得します。`format=text` をサポート。
- `GET /stats`: プールの状態と統計を表示します。
- `GET /all`: プール内のすべてのプロキシをリストします。

## 使用技術
![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)

---

## Docker によるデプロイ

本プロジェクトは Docker および Docker Compose による迅速なデプロイをサポートしています。

### 1. Docker Compose を使用する (推奨)
これが最も簡単な方法で、Redis と ProxyPool コンテナを自動的に起動します：

```bash
docker-compose up -d
```

### 2. ProxyPool イメージのみをビルドする
すでに稼働中の Redis がある場合：

```bash
# イメージのビルド
docker build -t proxy-pool .

# コンテナの実行 (Redis のアドレスを指定)
docker run -d -p 8000:8000 -e REDIS_HOST=host.docker.internal proxy-pool
```

---

## クイック使用例

プロキシを取得し、`curl` で Google にアクセスする：

```bash
# 1. プロキシを取得 (テキスト形式)
PROXY=$(curl -s http://localhost:8000/get?format=text)

# 2. そのプロキシを使用してウェブサイトにアクセス
curl -x "http://$PROXY" https://www.google.com -I
```

Python スクリプトでの使用：

```python
import httpx

# プロキシの取得
proxy = httpx.get("http://localhost:8000/get?format=text").text

# プロキシの使用
proxies = {
    "http://": f"http://{proxy}",
    "https://": f"http://{proxy}",
}
response = httpx.get("https://www.google.com", proxies=proxies)
print(response.status_code)
```


## 主な機能

- 複数のソースからプロキシ IP を自動収集
- プロキシ IP の可用性と速度をリアルタイムで検証
- バッチ処理と定期更新をサポート
- シンプルで使いやすく、迅速なデプロイが可能

## インストールと実行

1. リポジトリをクローンする：

```
git clone https://github.com/XiaomingX/proxypool.git
cd proxypool
```

2. 依存関係をインストールする（Python 環境を想定）：

```
pip install -r requirements.txt
```

3. プロキシ収集スクリプトを実行する：

```
python main.py
```

4. プロキシ検証スクリプトを実行する：

```
python verify.py
```

## 興味があるかもしれないサイバーセキュリティプロジェクト：
 - Rust で実装されたポートスキャナー:
   - https://github.com/XiaomingX/RustProxyHunter
 - Python で実装されたプロキシプール検出:
   - https://github.com/XiaomingX/proxy-pool
 - Golang で実装されたサプライチェーンセキュリティと CVE-POC 自動収集 (注意: 手動レビューなし):
   - https://github.com/XiaomingX/data-cve-poc
 - Python で実装された .git 漏洩検出ツール:
   - https://github.com/XiaomingX/github-sensitive-hack

## 参考とインスピレーション

本プロジェクトのデザインと思想は、以下の優れたオープンソースプロジェクトからインスピレーションを得ています：

- [ProjectDiscovery Katana](https://github.com/projectdiscovery/katana) —— モダンなクローラーおよびスパイダーフレームワーク。
- [Spider-rs Spider](https://github.com/spider-rs/spider) —— 高性能でスケーラブルなクローラーフレームワーク。

## 貢献ガイド

改善のための issue や pull request をお待ちしております。

## ライセンス

このプロジェクトは MIT ライセンスの下でライセンスされています。詳細は LICENSE ファイルを参照してください。

---

*ProxyPool をお楽しみください！ご不明な点がございましたら、作者までお問い合わせください。*
