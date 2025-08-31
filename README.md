# ProxyPool - 高效的代理IP池管理工具

ProxyPool 是一个用于采集、验证和管理代理IP的轻量级工具，旨在帮助用户自动维护高质量的代理池，方便在爬虫、网络请求中灵活使用匿名代理。

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
python main.py
```

4. 运行代理验证脚本：

```
python verify.py
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
