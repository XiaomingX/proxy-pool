# 测试运行器 - 执行所有测试套件并生成报告
import asyncio
import sys
from datetime import datetime


async def run_test_suite(name: str, module_name: str) -> dict:
    """运行单个测试套件"""
    print(f"\n{'='*60}")
    print(f"测试套件: {name}")
    print(f"{'='*60}")
    
    try:
        if module_name == "test_api":
            from test_api import run_all_tests
        elif module_name == "test_storage":
            from test_storage import run_all_tests
        elif module_name == "test_integration":
            from test_integration import run_all_tests
        else:
            return {"suite": name, "status": "✗ 失败", "error": "未知测试套件"}
        
        await run_all_tests()
        return {"suite": name, "status": "✓ 完成"}
    except Exception as e:
        return {"suite": name, "status": "✗ 失败", "error": str(e)}


async def main() -> None:
    """主测试运行器"""
    start_time = datetime.now()
    
    print("╔" + "="*58 + "╗")
    print("║" + " "*15 + "ProxyPool 测试套件" + " "*23 + "║")
    print("╚" + "="*58 + "╝")
    print(f"\n开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    test_suites = [
        ("API 端点测试", "test_api"),
        ("存储功能测试", "test_storage"),
        ("集成测试", "test_integration"),
    ]
    
    results = []
    for suite_name, module_name in test_suites:
        result = await run_test_suite(suite_name, module_name)
        results.append(result)
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print("\n" + "╔" + "="*58 + "╗")
    print("║" + " "*20 + "总体测试报告" + " "*24 + "║")
    print("╚" + "="*58 + "╝")
    
    for result in results:
        status_icon = "✓" if "✓" in result["status"] else "✗"
        print(f"\n{status_icon} {result['suite']}: {result['status']}")
        if "error" in result:
            print(f"  错误: {result['error']}")
    
    completed = sum(1 for r in results if "✓" in r["status"])
    failed = sum(1 for r in results if "✗" in r["status"])
    
    print(f"\n{'='*60}")
    print(f"测试套件总数: {len(results)}")
    print(f"完成: {completed} ✓")
    print(f"失败: {failed} ✗")
    print(f"总耗时: {duration:.2f}秒")
    print(f"结束时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # 返回退出码
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    asyncio.run(main())
