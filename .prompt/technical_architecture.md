# 技术架构文档

## 技术栈概览

- **Web 框架**: FastAPI 0.128.0
- **异步运行时**: asyncio + aiohttp
- **数据存储**: Redis 7.1.0
- **任务调度**: APScheduler 3.11.2
- **依赖管理**: uv
- **日志系统**: Loguru 0.7.3
- **Python 版本**: 3.11+

## 当前架构设计

```
┌─────────────────────────────────────────────────────────┐
│                     FastAPI Application                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  API Routes  │  │  Scheduler   │  │   Storage    │  │
│  │  (/get,      │  │  (APScheduler)│  │  (Redis)     │  │
│  │   /stats,    │  │              │  │              │  │
│  │   /all)      │  │  - Fetch     │  │  - Hash      │  │
│  └──────────────┘  │  - Validate  │  │  - HSET/HGET │  │
│                    └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
                    ┌──────────────┐
                    │  Redis Store │
                    │  (Hash: key) │
                    └──────────────┘
```

## 严重的技术债务与性能瓶颈

### 1. 存储层 - O(N) 复杂度问题 ⚠️ 高优先级

#### 当前实现问题
```python
# storage.py - get_random() 方法
async def get_random(self) -> Proxy | None:
    proxies = await self.redis.hvals(self.key)  # ❌ 获取所有代理到内存
    if not proxies:
        return None
    
    proxy_list = [Proxy.model_validate_json(p) for p in proxies]  # ❌ 反序列化所有对象
    max_score = max(p.score for p in proxy_list)  # ❌ 遍历所有代理
    best_proxies = [p for p in proxy_list if p.score == max_score]  # ❌ 再次遍历
    
    return random.choice(best_proxies)
```

**性能影响**:
- [ ] **时间复杂度**: O(N) - 代理数量增长到 10k+ 时延迟显著增加
- [ ] **内存占用**: 每次请求都将所有代理加载到内存
- [ ] **序列化开销**: 每个代理都需要 JSON 反序列化
- [ ] **扩展性差**: 无法支持大规模代理池（100k+）

#### 迁移方案: Redis Sorted Set (ZSET)

**实现步骤**:
- [ ] 修改 `storage.py` 使用 ZSET 替代 Hash
  ```python
  # 新实现示例
  async def add(self, proxy: Proxy):
      # ZADD proxies <score> <proxy_json>
      await self.redis.zadd("proxies", {proxy.model_dump_json(): proxy.score})
  
  async def get_random(self) -> Proxy | None:
      # ZREVRANGE proxies 0 99 - 获取前100个高分代理
      top_proxies = await self.redis.zrevrange("proxies", 0, 99, withscores=True)
      if not top_proxies:
          return None
      # 从高分代理中随机选择
      proxy_json = random.choice(top_proxies)[0]
      return Proxy.model_validate_json(proxy_json)
  ```
- [ ] 更新 `increase()` 和 `decrease()` 方法使用 `ZINCRBY`
- [ ] 修改 `get_all()` 使用 `ZRANGE` 并支持分页
- [ ] 添加按分数范围查询的方法 `get_by_score_range(min_score, max_score)`
- [ ] 编写数据迁移脚本（Hash → ZSET）
- [ ] 性能基准测试（对比 Hash vs ZSET）

**预期收益**:
- 时间复杂度降至 O(log N)
- 内存占用减少 90%+
- 支持百万级代理池
- 查询延迟降至毫秒级

### 2. 验证器 - 单点故障风险 ⚠️ 高优先级

#### 当前问题
```python
# validator.py
class Validator:
    def __init__(self):
        self.test_url = "http://httpbin.org/get"  # ❌ 硬编码单一目标
        self.semaphore = asyncio.Semaphore(200)  # ❌ 硬编码并发限制
```

**风险**:
- [ ] httpbin.org 宕机或限流会导致所有代理被误判为失效
- [ ] 无法适配不同业务场景的验证需求
- [ ] 并发数固定，无法根据机器性能调整

#### 改进方案
- [ ] 将 `test_url` 改为配置列表
  ```python
  # config.py
  VALIDATION_TARGETS: list[str] = [
      "http://httpbin.org/get",
      "https://www.google.com",
      "https://www.bing.com"
  ]
  VALIDATION_CONCURRENCY: int = 200
  VALIDATION_TIMEOUT: int = 10
  ```
- [ ] 实现多目标轮询验证策略
- [ ] 添加验证目标健康检查
- [ ] 支持自定义验证规则（响应码、响应时间、内容匹配）
- [ ] 记录每个代理的响应时间并存储

### 3. 抓取器 - 脆弱的正则解析 ⚠️ 中优先级

#### 当前问题
```python
# fetchers/common.py
found = re.findall(r'(\d+\.\d+\.\d+\.\d+)</td>\s*<td.*?>(\d+)</td>', html)
```

**问题**:
- [ ] 正则表达式依赖 HTML 结构，网站改版即失效
- [ ] 无法处理 JavaScript 渲染的页面
- [ ] 缺少错误处理和重试机制
- [ ] 无 User-Agent 轮换，易被识别为爬虫

#### 改进方案
- [ ] 引入 BeautifulSoup4 或 lxml 进行 DOM 解析
- [ ] 实现解析器接口，支持多种解析策略
  ```python
  class ParserInterface:
      async def parse(self, html: str) -> list[Proxy]:
          pass
  
  class RegexParser(ParserInterface):
      pass
  
  class XPathParser(ParserInterface):
      pass
  ```
- [ ] 添加 User-Agent 池
  ```python
  USER_AGENTS = [
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...",
      # ...
  ]
  ```
- [ ] 实现请求重试机制（tenacity 库）
- [ ] 添加随机延迟（避免请求过快）
- [ ] 考虑使用 Playwright/Selenium 处理 JS 渲染页面

### 4. 调度器 - 固定时间间隔 ⚠️ 低优先级

#### 当前问题
```python
# scheduler.py
self.scheduler.add_job(self.fetch_task, 'interval', minutes=30)
self.scheduler.add_job(self.validate_task, 'interval', minutes=5)
```

**问题**:
- [ ] 固定间隔无法适应动态需求
- [ ] 高峰期可能需要更频繁的验证
- [ ] 低峰期浪费资源

#### 改进方案
- [ ] 将调度间隔改为配置项
  ```python
  FETCH_INTERVAL_MINUTES: int = 30
  VALIDATE_INTERVAL_MINUTES: int = 5
  ```
- [ ] 实现动态调度策略
  - 代理池数量低于阈值时增加抓取频率
  - 高分代理占比高时降低验证频率
- [ ] 添加手动触发接口
  ```python
  @router.post("/admin/fetch")
  async def trigger_fetch():
      asyncio.create_task(scheduler.fetch_task())
  ```

### 5. 配置管理 - 缺少环境隔离 ⚠️ 中优先级

#### 当前问题
- [ ] 所有配置混在一个 `Settings` 类中
- [ ] 缺少开发/测试/生产环境配置隔离
- [ ] 敏感信息（Redis 密码）可能被提交到代码库

#### 改进方案
- [ ] 实现多环境配置
  ```python
  # config.py
  class BaseSettings(BaseSettings):
      pass
  
  class DevelopmentSettings(BaseSettings):
      REDIS_HOST: str = "localhost"
  
  class ProductionSettings(BaseSettings):
      REDIS_HOST: str = "redis"
  
  def get_settings():
      env = os.getenv("ENV", "development")
      if env == "production":
          return ProductionSettings()
      return DevelopmentSettings()
  ```
- [ ] 使用 `.env.example` 作为模板
- [ ] 添加配置验证（必填项检查）
- [ ] 支持从环境变量或配置文件加载

### 6. 错误处理与日志 ⚠️ 低优先级

#### 当前问题
- [ ] 异常捕获过于宽泛（`except Exception`）
- [ ] 缺少结构化日志字段
- [ ] 无请求追踪 ID

#### 改进方案
- [ ] 细化异常类型
  ```python
  class ProxyFetchError(Exception):
      pass
  
  class ProxyValidationError(Exception):
      pass
  ```
- [ ] 添加结构化日志
  ```python
  logger.bind(proxy=proxy.string, source=proxy.source).info("Validation success")
  ```
- [ ] 集成 OpenTelemetry 进行分布式追踪
- [ ] 添加 Sentry 错误监控

## 可删除的过时代码

### 当前无过时代码需要删除
- [x] 代码库较新，暂无明显废弃代码

### 未来可能废弃
- [ ] 当迁移到 ZSET 后，删除 Hash 相关的辅助方法
- [ ] 当实现分布式架构后，可能废弃 APScheduler（改用 Celery/RQ）

## 技术栈升级计划

### 依赖版本
- [x] Python 3.11+ (当前)
- [ ] 考虑升级到 Python 3.12（性能提升）
- [x] FastAPI 0.128.0 (当前)
- [ ] 定期更新依赖（安全补丁）

### 新技术引入
- [ ] **BeautifulSoup4**: 替代正则解析
- [ ] **Tenacity**: 重试机制
- [ ] **Prometheus Client**: 指标导出
- [ ] **Celery/RQ**: 分布式任务队列（替代 APScheduler）
- [ ] **Pydantic V2**: 已使用，保持更新
- [ ] **Redis OM**: 考虑使用 Redis ORM 简化操作

## 性能优化检查清单

### 立即执行（高优先级）
- [ ] 迁移到 Redis ZSET（存储层重构）
- [ ] 实现多验证目标支持
- [ ] 添加 User-Agent 轮换

### 短期执行（1-2周）
- [ ] 配置项外部化
- [ ] 添加 `/health` 端点
- [ ] 实现请求重试机制
- [ ] 优化日志结构

### 中期执行（1-2个月）
- [ ] 引入 BeautifulSoup4
- [ ] 实现动态调度策略
- [ ] 添加 Prometheus 指标
- [ ] 开发 Web 管理界面

### 长期执行（3-6个月）
- [ ] 分布式架构改造
- [ ] 集成 OpenTelemetry
- [ ] 实现多租户支持
- [ ] 性能压测与优化

## 架构演进路线图

### 阶段 1: 单体优化（当前 → 1个月）
- 修复 O(N) 性能问题
- 增强配置管理
- 改进错误处理

### 阶段 2: 功能增强（1-3个月）
- 扩展代理源
- 多验证策略
- Web 管理界面

### 阶段 3: 分布式改造（3-6个月）
- 组件解耦
- 水平扩展
- 监控告警

### 阶段 4: 企业级（6-12个月）
- 多租户
- SLA 保障
- 商业化准备
