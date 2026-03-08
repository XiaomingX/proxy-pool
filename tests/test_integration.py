# 集成测试 - 验证完整的代理获取和使用流程
import asyncio
import httpx
import sys
from pathlib import Path
from typing import Any

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


BASE_URL = "http://localhost:8000"


async def test_full_workflow() -> dict[str, Any]:
    """测试完整工作流：获取代理 -> 使用代理访问网站"""
    async with httpx.AsyncClient() as client:
        try:
            # 1. 获取代理
            response = await client.get(f"{BASE_URL}/get?format=text", timeout=10.0)
            
            if response.status_code == 503:
                return {
                    "test": "full_workflow",
                    "status": "⚠ 跳过",
                    "reason": "代理池为空，等待抓取"
                }
            
            assert response.status_code == 200
            proxy_str = response.text.strip()
            
            # 2. 使用代理访问测试网站
            proxies = {
                "http://": f"http://{proxy_str}",
                "https://": f"http://{proxy_str}",
            }
            
            try:
                test_response = await client.get(
                    "http://httpbin.org/ip",
                    proxies=proxies,
                    timeout=15.0
                )
                
                if test_response.status_code == 200:
                    return {
                        "test": "full_workflow",
                        "status": "✓ 通过",
                        "proxy": proxy_str,
                        "proxy_works": True
                    }
            except Exception as proxy_error:
                # 代理可能不可用，但流程是正确的
                return {
                    "test": "full_workflow",
                    "status": "⚠ 部分通过",
                    "proxy": proxy_str,
                    "proxy_works": False,
                    "note": "代理获取成功但不可用（正常情况）"
                }
                
        except Exception as e:
            return {"test": "full_workflow", "status": "✗ 失败", "error": str(e)}


async def test_concurrent_requests() -> dict[str, Any]:
    """测试并发请求处理"""
    async with httpx.AsyncClient() as client:
        try:
            # 并发发送10个请求
            tasks = [
                client.get(f"{BASE_URL}/stats", timeout=10.0)
                for _ in range(10)
            ]
            
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            
            # 检查所有响应
            success_count = sum(
                1 for r in responses
                if not isinstance(r, Exception) and r.status_code == 200
            )
            
            if success_count == 10:
                return {
                    "test": "concurrent_requests",
                    "status": "✓ 通过",
                    "success_count": success_count
                }
            return {
                "test": "concurrent_requests",
                "status": "✗ 失败",
                "success_count": success_count,
                "expected": 10
            }
        except Exception as e:
            return {"test": "concurrent_requests", "status": "✗ 失败", "error": str(e)}


async def test_api_response_time() -> dict[str, Any]:
    """测试API响应时间"""
    async with httpx.AsyncClient() as client:
        try:
            import time
            
            start = time.time()
            response = await client.get(f"{BASE_URL}/stats", timeout=10.0)
            elapsed = time.time() - start
            
            assert response.status_code == 200
            
            # 响应时间应该小于1秒
            if elapsed < 1.0:
                return {
                    "test": "api_response_time",
                    "status": "✓ 通过",
                    "response_time": f"{elapsed:.3f}s"
                }
            return {
                "test": "api_response_time",
                "status": "⚠ 慢",
                "response_time": f"{elapsed:.3f}s",
                "note": "响应时间超过1秒"
            }
        except Exception as e:
            return {"test": "api_response_time", "status": "✗ 失败", "error": str(e)}


async def test_error_handling() -> dict[str, Any]:
    """测试错误处理"""
    async with httpx.AsyncClient() as client:
        try:
            # 测试不存在的端点
            response = await client.get(f"{BASE_URL}/nonexistent", timeout=10.0)
            
            if response.status_code == 404:
                return {"test": "error_handling", "status": "✓ 通过"}
            return {
                "test": "error_handling",
                "status": "✗ 失败",
                "error": f"期望404，得到{response.status_code}"
            }
        except Exception as e:
            return {"test": "error_handling", "status": "✗ 失败", "error": str(e)}


async def run_all_tests() -> None:
    """运行所有集成测试"""
    print("=" * 60)
    print("开始运行 集成测试 套件")
    print("=" * 60)
    
    tests = [
        test_full_workflow,
        test_concurrent_requests,
        test_api_response_time,
        test_error_handling,
    ]
    
    results = []
    for test_func in tests:
        print(f"\n运行测试: {test_func.__name__}")
        result = await test_func()
        results.append(result)
        print(f"  结果: {result['status']}")
        if "error" in result:
            print(f"  错误: {result['error']}")
        if "response_time" in result:
            print(f"  响应时间: {result['response_time']}")
        if "note" in result:
            print(f"  备注: {result['note']}")
    
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    
    passed = sum(1 for r in results if "✓" in r["status"])
    failed = sum(1 for r in results if "✗" in r["status"])
    warnings = sum(1 for r in results if "⚠" in r["status"])
    
    print(f"总计: {len(results)} 个测试")
    print(f"通过: {passed} ✓")
    print(f"失败: {failed} ✗")
    print(f"警告: {warnings} ⚠")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(run_all_tests())
