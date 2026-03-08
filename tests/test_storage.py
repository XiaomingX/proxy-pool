# Redis存储功能测试 - 验证代理的增删改查和评分机制
import asyncio
import sys
from pathlib import Path

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from proxy_pool.core.storage import storage
from proxy_pool.schemas.proxy import Proxy
from proxy_pool.utils.config import settings


async def test_add_proxy() -> dict:
    """测试添加代理"""
    try:
        test_proxy = Proxy(host="1.2.3.4", port=8080, source="test")
        await storage.add(test_proxy)
        
        # 验证是否添加成功
        all_proxies = await storage.get_all()
        found = any(p.host == "1.2.3.4" and p.port == 8080 for p in all_proxies)
        
        if found:
            return {"test": "add_proxy", "status": "✓ 通过"}
        return {"test": "add_proxy", "status": "✗ 失败", "error": "代理未添加成功"}
    except Exception as e:
        return {"test": "add_proxy", "status": "✗ 失败", "error": str(e)}


async def test_increase_score() -> dict:
    """测试增加代理评分"""
    try:
        test_proxy = Proxy(host="5.6.7.8", port=9090, score=50, source="test")
        await storage.add(test_proxy)
        
        # 增加评分
        await storage.increase(test_proxy)
        
        # 验证评分是否增加
        all_proxies = await storage.get_all()
        proxy = next((p for p in all_proxies if p.host == "5.6.7.8"), None)
        
        if proxy and proxy.score == 60:
            return {"test": "increase_score", "status": "✓ 通过", "new_score": proxy.score}
        return {"test": "increase_score", "status": "✗ 失败", "error": f"评分未正确增加: {proxy.score if proxy else 'None'}"}
    except Exception as e:
        return {"test": "increase_score", "status": "✗ 失败", "error": str(e)}


async def test_decrease_score() -> dict:
    """测试减少代理评分"""
    try:
        test_proxy = Proxy(host="9.10.11.12", port=7070, score=30, source="test")
        await storage.add(test_proxy)
        
        # 减少评分
        await storage.decrease(test_proxy)
        
        # 验证评分是否减少
        all_proxies = await storage.get_all()
        proxy = next((p for p in all_proxies if p.host == "9.10.11.12"), None)
        
        if proxy and proxy.score == 10:
            return {"test": "decrease_score", "status": "✓ 通过", "new_score": proxy.score}
        return {"test": "decrease_score", "status": "✗ 失败", "error": f"评分未正确减少: {proxy.score if proxy else 'None'}"}
    except Exception as e:
        return {"test": "decrease_score", "status": "✗ 失败", "error": str(e)}


async def test_auto_remove_low_score() -> dict:
    """测试低分代理自动删除"""
    try:
        test_proxy = Proxy(host="13.14.15.16", port=6060, score=10, source="test")
        await storage.add(test_proxy)
        
        # 减少评分到0以下，应该被删除
        await storage.decrease(test_proxy)
        
        # 验证是否被删除
        all_proxies = await storage.get_all()
        found = any(p.host == "13.14.15.16" for p in all_proxies)
        
        if not found:
            return {"test": "auto_remove_low_score", "status": "✓ 通过"}
        return {"test": "auto_remove_low_score", "status": "✗ 失败", "error": "低分代理未被删除"}
    except Exception as e:
        return {"test": "auto_remove_low_score", "status": "✗ 失败", "error": str(e)}


async def test_get_random() -> dict:
    """测试获取随机高分代理"""
    try:
        # 添加多个不同分数的代理
        proxies = [
            Proxy(host="20.20.20.20", port=8001, score=100, source="test"),
            Proxy(host="20.20.20.21", port=8002, score=100, source="test"),
            Proxy(host="20.20.20.22", port=8003, score=50, source="test"),
        ]
        
        for p in proxies:
            await storage.add(p)
        
        # 获取随机代理，应该返回高分代理
        random_proxy = await storage.get_random()
        
        if random_proxy and random_proxy.score == 100:
            return {"test": "get_random", "status": "✓ 通过", "proxy": random_proxy.string}
        return {"test": "get_random", "status": "✗ 失败", "error": f"未返回最高分代理: {random_proxy.score if random_proxy else 'None'}"}
    except Exception as e:
        return {"test": "get_random", "status": "✗ 失败", "error": str(e)}


async def test_count() -> dict:
    """测试代理计数"""
    try:
        count = await storage.count()
        if isinstance(count, int) and count >= 0:
            return {"test": "count", "status": "✓ 通过", "count": count}
        return {"test": "count", "status": "✗ 失败", "error": "计数返回值异常"}
    except Exception as e:
        return {"test": "count", "status": "✗ 失败", "error": str(e)}


async def run_all_tests() -> None:
    """运行所有存储测试"""
    print("=" * 60)
    print("开始运行 存储功能 测试套件")
    print("=" * 60)
    
    tests = [
        test_add_proxy,
        test_increase_score,
        test_decrease_score,
        test_auto_remove_low_score,
        test_get_random,
        test_count,
    ]
    
    results = []
    for test_func in tests:
        print(f"\n运行测试: {test_func.__name__}")
        result = await test_func()
        results.append(result)
        print(f"  结果: {result['status']}")
        if "error" in result:
            print(f"  错误: {result['error']}")
        if "new_score" in result:
            print(f"  新评分: {result['new_score']}")
    
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    
    passed = sum(1 for r in results if "✓" in r["status"])
    failed = sum(1 for r in results if "✗" in r["status"])
    
    print(f"总计: {len(results)} 个测试")
    print(f"通过: {passed} ✓")
    print(f"失败: {failed} ✗")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(run_all_tests())
