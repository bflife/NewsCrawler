"""
快速测试脚本 - 验证调度器基本功能
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from news_crawler.scheduler import NewsScheduler
from news_crawler.sites import register_all_crawlers


def test_basic_setup():
    """测试基本设置"""
    print("=" * 60)
    print("测试1: 基本设置")
    print("=" * 60)
    
    scheduler = NewsScheduler()
    
    # 测试数据库初始化
    print("✓ 数据库初始化成功")
    
    # 测试配置加载
    sources = scheduler.load_sources_config()
    print(f"✓ 加载配置文件: {len(sources)} 个新闻源")
    
    # 显示部分新闻源
    print("\n示例新闻源:")
    for source in sources[:5]:
        print(f"  - {source['name']} ({source['country']}) - {source['url']}")
    
    print("\n✓ 基本设置测试通过\n")


def test_task_init():
    """测试任务初始化"""
    print("=" * 60)
    print("测试2: 任务初始化")
    print("=" * 60)
    
    scheduler = NewsScheduler()
    
    # 初始化任务
    print("初始化任务...")
    scheduler.init_tasks_from_config(interval_minutes=60)
    
    # 统计
    tasks = scheduler.db.get_all_tasks()
    print(f"✓ 创建任务: {len(tasks)} 个")
    
    # 按国家统计
    countries = scheduler.get_all_countries()
    print(f"✓ 覆盖国家/地区: {len(countries)} 个")
    
    print("\n按国家分布:")
    for country in countries[:10]:
        country_tasks = scheduler.get_tasks_by_country(country)
        enabled = sum(1 for t in country_tasks if t.enabled)
        print(f"  {country}: {len(country_tasks)} 个任务 (启用: {enabled})")
    
    print("\n✓ 任务初始化测试通过\n")


def test_crawler_registration():
    """测试爬虫注册"""
    print("=" * 60)
    print("测试3: 爬虫注册")
    print("=" * 60)
    
    scheduler = NewsScheduler()
    
    # 注册爬虫
    print("注册爬虫...")
    register_all_crawlers(scheduler)
    
    print(f"✓ 已注册爬虫: {len(scheduler.crawlers)} 个")
    
    # 列出已注册的爬虫
    print("\n已注册的爬虫:")
    for source_id in scheduler.crawlers.keys():
        print(f"  - {source_id}")
    
    print("\n✓ 爬虫注册测试通过\n")


def test_statistics():
    """测试统计功能"""
    print("=" * 60)
    print("测试4: 统计功能")
    print("=" * 60)
    
    scheduler = NewsScheduler()
    
    stats = scheduler.get_task_statistics()
    
    print("调度器统计:")
    print(f"  总任务数:        {stats['total_tasks']}")
    print(f"  启用任务数:      {stats['enabled_tasks']}")
    print(f"  禁用任务数:      {stats['disabled_tasks']}")
    print(f"  国家/地区数:     {stats['countries']}")
    print(f"  最近成功次数:    {stats['recent_success']}")
    print(f"  最近失败次数:    {stats['recent_failed']}")
    
    print("\n✓ 统计功能测试通过\n")


def main():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("新闻爬虫调度器 - 快速测试")
    print("=" * 60 + "\n")
    
    tests = [
        ("基本设置", test_basic_setup),
        ("任务初始化", test_task_init),
        ("爬虫注册", test_crawler_registration),
        ("统计功能", test_statistics),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"\n✗ 测试失败: {name}")
            print(f"  错误: {e}")
            failed += 1
    
    # 总结
    print("=" * 60)
    print("测试总结")
    print("=" * 60)
    print(f"通过: {passed}/{len(tests)}")
    print(f"失败: {failed}/{len(tests)}")
    
    if failed == 0:
        print("\n✓ 所有测试通过!")
    else:
        print(f"\n✗ {failed} 个测试失败")
    
    print("=" * 60)
    
    # 提示下一步
    print("\n下一步操作:")
    print("1. 查看所有任务: uv run python scheduler_cli.py list")
    print("2. 按国家查看:   uv run python scheduler_cli.py list --country 台湾")
    print("3. 启动调度器:   uv run python scheduler_cli.py start")
    print("4. 手动执行:     uv run python scheduler_cli.py run --source-id zaobao")
    print("5. 查看帮助:     uv run python scheduler_cli.py --help")


if __name__ == '__main__':
    main()
