"""
调度器使用示例
"""

import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from news_crawler.scheduler import NewsScheduler
from news_crawler.sites import register_all_crawlers


def example_1_basic_usage():
    """示例1：基本使用"""
    print("\n" + "="*60)
    print("示例1：基本使用 - 初始化和查看任务")
    print("="*60)
    
    # 创建调度器
    scheduler = NewsScheduler()
    
    # 初始化任务（从配置文件加载）
    print("\n1. 初始化任务...")
    scheduler.init_tasks_from_config(interval_minutes=60)
    
    # 查看所有任务
    print("\n2. 查看所有任务...")
    tasks = scheduler.db.get_all_tasks()
    print(f"总共 {len(tasks)} 个任务")
    
    # 查看各国任务数
    print("\n3. 按国家统计...")
    countries = scheduler.get_all_countries()
    for country in countries[:10]:  # 显示前10个
        country_tasks = scheduler.get_tasks_by_country(country)
        print(f"  {country}: {len(country_tasks)} 个任务")


def example_2_manual_crawl():
    """示例2：手动执行爬取"""
    print("\n" + "="*60)
    print("示例2：手动执行爬取")
    print("="*60)
    
    # 创建调度器
    scheduler = NewsScheduler()
    
    # 注册爬虫
    register_all_crawlers(scheduler)
    
    # 手动执行单个任务
    print("\n执行单个爬取任务...")
    source_id = "zaobao"  # 联合早报
    success = scheduler.execute_task_by_source_id(source_id)
    
    if success:
        print(f"\n✓ 爬取成功: {source_id}")
        
        # 查看爬取历史
        task = scheduler.db.get_task_by_source_id(source_id)
        history = scheduler.db.get_history_by_task_id(task.id, limit=1)
        if history:
            h = history[0]
            print(f"  - 文章数: {h.articles_count}")
            print(f"  - 耗时: {h.duration_seconds:.2f} 秒")
    else:
        print(f"\n✗ 爬取失败: {source_id}")


def example_3_country_filter():
    """示例3：按国家筛选和爬取"""
    print("\n" + "="*60)
    print("示例3：按国家筛选和爬取")
    print("="*60)
    
    # 创建调度器
    scheduler = NewsScheduler()
    register_all_crawlers(scheduler)
    
    # 获取台湾的新闻源
    country = "台湾"
    print(f"\n查找 {country} 的新闻源...")
    tasks = scheduler.get_tasks_by_country(country)
    print(f"找到 {len(tasks)} 个 {country} 新闻源")
    
    # 显示前5个
    print(f"\n前5个新闻源:")
    for i, task in enumerate(tasks[:5], 1):
        print(f"  {i}. {task.source_name} ({task.source_id})")
        print(f"     URL: {task.url}")
        print(f"     状态: {'启用' if task.enabled else '禁用'}")


def example_4_statistics():
    """示例4：查看统计信息"""
    print("\n" + "="*60)
    print("示例4：查看统计信息")
    print("="*60)
    
    # 创建调度器
    scheduler = NewsScheduler()
    
    # 获取统计信息
    stats = scheduler.get_task_statistics()
    
    print("\n调度器统计:")
    print(f"  总任务数:        {stats['total_tasks']}")
    print(f"  启用任务数:      {stats['enabled_tasks']}")
    print(f"  禁用任务数:      {stats['disabled_tasks']}")
    print(f"  国家/地区数:     {stats['countries']}")
    print(f"  最近成功次数:    {stats['recent_success']}")
    print(f"  最近失败次数:    {stats['recent_failed']}")


def example_5_task_management():
    """示例5：任务管理"""
    print("\n" + "="*60)
    print("示例5：任务管理 - 启用/禁用/设置间隔")
    print("="*60)
    
    # 创建调度器
    scheduler = NewsScheduler()
    
    source_id = "zaobao"
    task = scheduler.db.get_task_by_source_id(source_id)
    
    if not task:
        print(f"任务不存在: {source_id}")
        return
    
    print(f"\n任务: {task.source_name}")
    print(f"  当前状态: {'启用' if task.enabled else '禁用'}")
    print(f"  爬取间隔: {task.interval_minutes} 分钟")
    
    # 修改间隔
    print(f"\n将间隔改为 120 分钟...")
    task.interval_minutes = 120
    scheduler.db.update_task(task)
    print("✓ 已更新")
    
    # 验证
    task = scheduler.db.get_task_by_source_id(source_id)
    print(f"  新间隔: {task.interval_minutes} 分钟")


def example_6_history():
    """示例6：查看爬取历史"""
    print("\n" + "="*60)
    print("示例6：查看爬取历史")
    print("="*60)
    
    # 创建调度器
    scheduler = NewsScheduler()
    
    # 获取最近的爬取历史
    print("\n最近10条爬取记录:")
    history_list = scheduler.db.get_recent_history(limit=10)
    
    if not history_list:
        print("  暂无爬取记录")
        return
    
    for i, h in enumerate(history_list, 1):
        status_icon = "✓" if h.status == "success" else "✗"
        print(f"\n  {i}. [{status_icon}] {h.source_id}")
        print(f"     时间: {h.crawl_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"     状态: {h.status}")
        print(f"     文章数: {h.articles_count}")
        print(f"     耗时: {h.duration_seconds:.2f} 秒")
        if h.error_message:
            print(f"     错误: {h.error_message}")


def example_7_scheduler_start():
    """示例7：启动调度器（演示模式）"""
    print("\n" + "="*60)
    print("示例7：启动调度器（演示模式 - 10秒后自动停止）")
    print("="*60)
    
    import time
    
    # 创建调度器
    scheduler = NewsScheduler()
    register_all_crawlers(scheduler)
    
    # 启动调度器
    print("\n启动调度器...")
    scheduler.start()
    
    print("调度器运行中...")
    print("（实际使用时，调度器会一直运行，直到手动停止）")
    
    # 等待10秒
    for i in range(10, 0, -1):
        print(f"  {i} 秒后停止...", end='\r')
        time.sleep(1)
    
    # 停止调度器
    print("\n\n停止调度器...")
    scheduler.stop()
    print("✓ 调度器已停止")


def main():
    """运行所有示例"""
    print("\n" + "="*80)
    print("新闻爬虫调度器 - 使用示例")
    print("="*80)
    
    examples = [
        ("基本使用", example_1_basic_usage),
        ("手动执行爬取", example_2_manual_crawl),
        ("按国家筛选", example_3_country_filter),
        ("查看统计信息", example_4_statistics),
        ("任务管理", example_5_task_management),
        ("查看历史", example_6_history),
        ("启动调度器（演示）", example_7_scheduler_start),
    ]
    
    print("\n可用示例:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    
    print("\n请选择要运行的示例（输入数字，0=全部运行，q=退出）:")
    
    try:
        choice = input("> ").strip()
        
        if choice.lower() == 'q':
            print("退出")
            return
        
        if choice == '0':
            # 运行所有示例
            for name, func in examples:
                try:
                    func()
                    input("\n按回车继续...")
                except KeyboardInterrupt:
                    print("\n\n跳过当前示例")
                    continue
        else:
            # 运行指定示例
            idx = int(choice) - 1
            if 0 <= idx < len(examples):
                name, func = examples[idx]
                func()
            else:
                print("无效的选择")
    
    except KeyboardInterrupt:
        print("\n\n程序中断")
    except Exception as e:
        print(f"\n错误: {e}")
    
    print("\n" + "="*80)
    print("示例结束")
    print("="*80)


if __name__ == '__main__':
    main()
