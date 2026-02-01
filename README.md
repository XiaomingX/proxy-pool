# ProxyPool Architect

基于 Python 3.11+、FastAPI 和 Redis 构建的现代化、快速且可靠的代理池。

## 特性
- **现代化技术栈**: FastAPI, aiohttp, Redis, APScheduler, Loguru。
- **异步**: 从抓取到验证完全异步。
- **权重评分**: 动态基于评分的管理（成功 +10，失败 -20）。
- **易于部署**: 使用 `uv` 管理。

## 项目结构

```
proxy-pool/
├── src/                          # 源代码目录
│   ├── main.py                   # 应用入口
│   └── proxy_pool/               # 核心包
│       ├── api/                  # API 路由
│       ├── core/                 # 核心功能（调度器等）
│       ├── fetchers/             # 代理抓取器
│       ├── schemas/              # 数据模型
│       └── utils/                # 工具函数
├── fetch-proxy-by-deploy/        # 部署脚本
├── fetch-proxy-by-scan/          # 扫描工具
├── pyproject.toml                # 项目配置
├── Dockerfile                    # Docker 镜像配置
└── docker-compose.yml            # Docker Compose 配置
```

## 快速开始

### 1. 安装 Redis (前提条件)

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

### 2. 配置

如果需要，在根目录创建 `.env` 文件以覆盖默认设置：
```env
REDIS_HOST=localhost
REDIS_PORT=6379
# REDIS_PASSWORD=your_password
```

### 3. 安装与运行项目
确保已安装 `uv` ([安装 uv](https://docs.astral.sh/uv/getting-started/installation/))。

```bash
uv sync
uv run src/main.py
```

## API 接口
- `GET /get`: 获取一个高质量的随机代理。支持 `format=text`。
- `GET /stats`: 查看代理池健康状况和统计数据。
- `GET /all`: 列出代理池中的所有代理。

## 构建自
![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)

---

## 使用 Docker 部署

本项目支持通过 Docker 和 Docker Compose 快速部署。

### 1. 使用 Docker Compose (推荐)
这是最简单的方法，会自动启动 Redis 和 ProxyPool 容器：

```bash
docker-compose up -d
```

### 2. 仅构建 ProxyPool 镜像
如果你已有运行中的 Redis：

```bash
# 构建镜像
docker build -t proxy-pool .

# 运行容器 (需要指定 Redis 地址)
docker run -d -p 8000:8000 -e REDIS_HOST=host.docker.internal proxy-pool
```

---

## 快速使用示例

获取代理并使用 `curl` 访问百度：

```bash
# 1. 获取一个代理 (纯文本格式)
PROXY=$(curl -s http://localhost:8000/get?format=text)

# 2. 使用该代理访问百度
curl -x "http://$PROXY" https://www.baidu.com -I
```

在 Python 脚本中使用：

```python
import httpx

# 获取代理
proxy = httpx.get("http://localhost:8000/get?format=text").text

# 使用代理
proxies = {
    "http://": f"http://{proxy}",
    "https://": f"http://{proxy}",
}
response = httpx.get("https://www.baidu.com", proxies=proxies)
print(response.status_code)
```


## 主要功能

- 自动抓取多来源的代理IP
- 实时验证代理IP的可用性和速度
- 支持批量运行和定时更新
- 简洁易用，快速部署

## 安装与运行

1. 克隆本仓库：

```
git clone https://github.com/XiaomingX/proxypool.git
cd proxypool
```

2. 安装依赖（假设您使用 Python 环境，请根据实际需求调整）：

```
pip install -r requirements.txt
```

3. 运行代理抓取脚本：

```
python src/main.py
```

4. 运行代理验证脚本：

```
python src/verify.py
```

## 如果你对网络安全感兴趣，如下开源代码不容错过：
 - rust实现的端口扫描器：
   - https://github.com/XiaomingX/RustProxyHunter
 - python实现的代理池检测：
   - https://github.com/XiaomingX/proxy-pool
 - golang实现的供应链安全，CVE-POC的全自动收集（注无人工审核，可能被投毒，仅限有基础的朋友）：
   - https://github.com/XiaomingX/data-cve-poc
 - python实现的检查.git泄漏的工具
   - https://github.com/XiaomingX/github-sensitive-hack

## 参考与灵感来源

本项目部分设计思路和实现参考了以下优秀开源项目：

- [ProjectDiscovery Katana](https://github.com/projectdiscovery/katana) —— 一款现代化的爬虫和蜘蛛框架，提供强大的爬取与解析功能。
- [Spider-rs Spider](https://github.com/spider-rs/spider) —— 一个高性能、可扩展的爬虫框架，适合大规模爬取任务。

## 贡献指南

欢迎提交 issues 和 pull requests，帮助我们不断改进。

## 许可证

该项目采用 MIT 许可证，详情请查看 LICENSE 文件。

---

*祝您使用愉快！如有任何问题，请联系作者。*
