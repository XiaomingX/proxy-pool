# API端点测试 - 验证所有API接口的功能和响应格式
import httpx
import asyncio
from typing import Any


BASE_URL = "http://localhost:8000"


async def test_health_check() -> dict[str, Any]:
    """测试服务是否正常运行"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/stats", timeout=10.0)
            assert response.status_code == 200, f"状态码错误: {response.status_code}"
            data = response.json()
            assert "total" in data, "响应缺少 total 字段"
            assert "status" in data, "响应缺少 status 字段"
            return {"test": "health_check", "status": "✓ 通过", "data": data}
        except Exception as e:
            return {"test": "health_check", "status": "✗ 失败", "error": str(e)}


async def test_get_stats() -> dict[str, Any]:
    """测试统计信息接口"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/stats", timeout=10.0)
            assert response.status_code == 200
            data = response.json()
            
            # 验证必需字段
            assert "total" in data
            assert "high_score" in data
            assert "status" in data
            assert isinstance(data["total"], int)
            assert isinstance(data["high_score"], int)
            
            return {"test": "get_stats", "status": "✓ 通过", "data": data}
        except Exception as e:
            return {"test": "get_stats", "status": "✗ 失败", "error": str(e)}


async def test_get_all_proxies() -> dict[str, Any]:
    """测试获取所有代理接口"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/all", timeout=10.0)
            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list), "响应应该是列表"
            
            # 如果有代理，验证代理格式
            if data:
                proxy = data[0]
                assert "host" in proxy
                assert "port" in proxy
                assert "score" in proxy
            
            return {"test": "get_all_proxies", "status": "✓ 通过", "count": len(data)}
        except Exception as e:
            return {"test": "get_all_proxies", "status": "✗ 失败", "error": str(e)}


async def test_get_proxy_json() -> dict[str, Any]:
    """测试获取单个代理（JSON格式）"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/get?format=json", timeout=10.0)
            
            # 如果池为空，返回503是正常的
            if response.status_code == 503:
                return {"test": "get_proxy_json", "status": "⚠ 代理池为空", "note": "等待抓取"}
            
            assert response.status_code == 200
            data = response.json()
            assert "host" in data
            assert "port" in data
            assert "score" in data
            
            return {"test": "get_proxy_json", "status": "✓ 通过", "proxy": f"{data['host']}:{data['port']}"}
        except Exception as e:
            return {"test": "get_proxy_json", "status": "✗ 失败", "error": str(e)}


async def test_get_proxy_text() -> dict[str, Any]:
    """测试获取单个代理（文本格式）"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/get?format=text", timeout=10.0)
            
            if response.status_code == 503:
                return {"test": "get_proxy_text", "status": "⚠ 代理池为空", "note": "等待抓取"}
            
            assert response.status_code == 200
            text = response.text
            assert ":" in text, "代理格式应为 host:port"
            
            return {"test": "get_proxy_text", "status": "✓ 通过", "proxy": text}
        except Exception as e:
            return {"test": "get_proxy_text", "status": "✗ 失败", "error": str(e)}


async def run_all_tests() -> None:
    """运行所有API测试"""
    print("=" * 60)
    print("开始运行 API 测试套件")
    print("=" * 60)
    
    tests = [
        test_health_check,
        test_get_stats,
        test_get_all_proxies,
        test_get_proxy_json,
        test_get_proxy_text,
    ]
    
    results = []
    for test_func in tests:
        print(f"\n运行测试: {test_func.__name__}")
        result = await test_func()
        results.append(result)
        print(f"  结果: {result['status']}")
        if "data" in result:
            print(f"  数据: {result['data']}")
        if "error" in result:
            print(f"  错误: {result['error']}")
    
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
