"""
新闻爬虫调度器命令行工具
"""

import sys
import time
import argparse
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from news_crawler.scheduler import NewsScheduler
from news_crawler.sites import register_all_crawlers


def cmd_init(args):
    """初始化任务"""
    scheduler = NewsScheduler()
    scheduler.init_tasks_from_config(interval_minutes=args.interval)
    print(f"任务初始化完成，默认间隔: {args.interval} 分钟")


def cmd_start(args):
    """启动调度器"""
    scheduler = NewsScheduler()
    
    # 注册所有爬虫
    register_all_crawlers(scheduler)
    
    # 启动调度器
    scheduler.start()
    
    print("\n调度器已启动！按 Ctrl+C 停止...")
    print(f"监控间隔: 每 60 秒检查一次任务")
    
    try:
        # 保持运行
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n正在停止调度器...")
        scheduler.stop()
        print("调度器已停止")


def cmd_run_once(args):
    """执行单个任务"""
    scheduler = NewsScheduler()
    register_all_crawlers(scheduler)
    
    if args.source_id:
        success = scheduler.execute_task_by_source_id(args.source_id)
        if success:
            print(f"任务执行成功: {args.source_id}")
        else:
            print(f"任务执行失败: {args.source_id}")
    else:
        scheduler.check_and_execute_tasks()


def cmd_list_tasks(args):
    """列出所有任务"""
    scheduler = NewsScheduler()
    
    if args.country:
        tasks = scheduler.get_tasks_by_country(args.country)
        print(f"\n国家/地区: {args.country}")
    else:
        tasks = scheduler.db.get_all_tasks()
        print("\n所有任务:")
    
    print(f"{'='*100}")
    print(f"{'ID':<5} {'新闻源':<20} {'国家/地区':<12} {'URL':<40} {'状态':<6} {'间隔(分钟)':<10}")
    print(f"{'='*100}")
    
    for task in tasks:
        status = "启用" if task.enabled else "禁用"
        print(f"{task.id:<5} {task.source_name:<20} {task.country:<12} "
              f"{task.url[:40]:<40} {status:<6} {task.interval_minutes:<10}")
    
    print(f"{'='*100}")
    print(f"总计: {len(tasks)} 个任务")


def cmd_list_countries(args):
    """列出所有国家"""
    scheduler = NewsScheduler()
    countries = scheduler.get_all_countries()
    
    print("\n所有国家/地区:")
    print(f"{'='*50}")
    
    for country in countries:
        tasks = scheduler.get_tasks_by_country(country)
        enabled = sum(1 for t in tasks if t.enabled)
        print(f"{country:<20} 总计: {len(tasks)}, 启用: {enabled}")
    
    print(f"{'='*50}")
    print(f"总计: {len(countries)} 个国家/地区")


def cmd_history(args):
    """查看爬取历史"""
    scheduler = NewsScheduler()
    
    if args.source_id:
        task = scheduler.db.get_task_by_source_id(args.source_id)
        if not task:
            print(f"未找到任务: {args.source_id}")
            return
        history_list = scheduler.db.get_history_by_task_id(task.id, limit=args.limit)
        print(f"\n任务历史: {task.source_name} ({args.source_id})")
    else:
        history_list = scheduler.db.get_recent_history(limit=args.limit)
        print(f"\n最近爬取历史:")
    
    print(f"{'='*120}")
    print(f"{'ID':<5} {'新闻源ID':<15} {'状态':<8} {'文章数':<8} {'耗时(秒)':<10} {'时间':<20} {'错误信息':<40}")
    print(f"{'='*120}")
    
    for history in history_list:
        error_msg = (history.error_message[:37] + '...') if history.error_message and len(history.error_message) > 40 else (history.error_message or '')
        print(f"{history.id:<5} {history.source_id:<15} {history.status:<8} "
              f"{history.articles_count:<8} {history.duration_seconds:<10.2f} "
              f"{history.crawl_time.strftime('%Y-%m-%d %H:%M:%S'):<20} {error_msg:<40}")
    
    print(f"{'='*120}")
    print(f"总计: {len(history_list)} 条记录")


def cmd_stats(args):
    """统计信息"""
    scheduler = NewsScheduler()
    stats = scheduler.get_task_statistics()
    
    print("\n调度器统计信息:")
    print(f"{'='*50}")
    print(f"总任务数:        {stats['total_tasks']}")
    print(f"启用任务数:      {stats['enabled_tasks']}")
    print(f"禁用任务数:      {stats['disabled_tasks']}")
    print(f"国家/地区数:     {stats['countries']}")
    print(f"最近成功次数:    {stats['recent_success']}")
    print(f"最近失败次数:    {stats['recent_failed']}")
    print(f"{'='*50}")


def cmd_enable(args):
    """启用任务"""
    scheduler = NewsScheduler()
    task = scheduler.db.get_task_by_source_id(args.source_id)
    
    if not task:
        print(f"未找到任务: {args.source_id}")
        return
    
    task.enabled = True
    scheduler.db.update_task(task)
    print(f"已启用任务: {task.source_name} ({args.source_id})")


def cmd_disable(args):
    """禁用任务"""
    scheduler = NewsScheduler()
    task = scheduler.db.get_task_by_source_id(args.source_id)
    
    if not task:
        print(f"未找到任务: {args.source_id}")
        return
    
    task.enabled = False
    scheduler.db.update_task(task)
    print(f"已禁用任务: {task.source_name} ({args.source_id})")


def cmd_set_interval(args):
    """设置任务间隔"""
    scheduler = NewsScheduler()
    task = scheduler.db.get_task_by_source_id(args.source_id)
    
    if not task:
        print(f"未找到任务: {args.source_id}")
        return
    
    task.interval_minutes = args.interval
    scheduler.db.update_task(task)
    print(f"已设置任务间隔: {task.source_name} ({args.source_id}) -> {args.interval} 分钟")


def main():
    parser = argparse.ArgumentParser(
        description='新闻爬虫调度器 - 支持多国家/地区新闻源的定时爬取',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 初始化任务（从配置文件加载）
  python scheduler_cli.py init --interval 60
  
  # 启动调度器
  python scheduler_cli.py start
  
  # 列出所有任务
  python scheduler_cli.py list
  
  # 列出指定国家的任务
  python scheduler_cli.py list --country 台湾
  
  # 列出所有国家
  python scheduler_cli.py countries
  
  # 手动执行单个任务
  python scheduler_cli.py run --source-id zaobao
  
  # 查看爬取历史
  python scheduler_cli.py history --limit 20
  
  # 查看统计信息
  python scheduler_cli.py stats
  
  # 启用/禁用任务
  python scheduler_cli.py enable --source-id zaobao
  python scheduler_cli.py disable --source-id zaobao
  
  # 设置任务间隔
  python scheduler_cli.py set-interval --source-id zaobao --interval 120
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='子命令')
    
    # init 命令
    parser_init = subparsers.add_parser('init', help='初始化任务')
    parser_init.add_argument('--interval', type=int, default=60, help='默认爬取间隔（分钟），默认60')
    parser_init.set_defaults(func=cmd_init)
    
    # start 命令
    parser_start = subparsers.add_parser('start', help='启动调度器')
    parser_start.set_defaults(func=cmd_start)
    
    # run 命令
    parser_run = subparsers.add_parser('run', help='手动执行任务')
    parser_run.add_argument('--source-id', help='指定新闻源ID，不指定则执行所有到期任务')
    parser_run.set_defaults(func=cmd_run_once)
    
    # list 命令
    parser_list = subparsers.add_parser('list', help='列出任务')
    parser_list.add_argument('--country', help='按国家/地区筛选')
    parser_list.set_defaults(func=cmd_list_tasks)
    
    # countries 命令
    parser_countries = subparsers.add_parser('countries', help='列出所有国家')
    parser_countries.set_defaults(func=cmd_list_countries)
    
    # history 命令
    parser_history = subparsers.add_parser('history', help='查看爬取历史')
    parser_history.add_argument('--source-id', help='指定新闻源ID')
    parser_history.add_argument('--limit', type=int, default=20, help='显示数量，默认20')
    parser_history.set_defaults(func=cmd_history)
    
    # stats 命令
    parser_stats = subparsers.add_parser('stats', help='统计信息')
    parser_stats.set_defaults(func=cmd_stats)
    
    # enable 命令
    parser_enable = subparsers.add_parser('enable', help='启用任务')
    parser_enable.add_argument('--source-id', required=True, help='新闻源ID')
    parser_enable.set_defaults(func=cmd_enable)
    
    # disable 命令
    parser_disable = subparsers.add_parser('disable', help='禁用任务')
    parser_disable.add_argument('--source-id', required=True, help='新闻源ID')
    parser_disable.set_defaults(func=cmd_disable)
    
    # set-interval 命令
    parser_interval = subparsers.add_parser('set-interval', help='设置任务间隔')
    parser_interval.add_argument('--source-id', required=True, help='新闻源ID')
    parser_interval.add_argument('--interval', type=int, required=True, help='间隔时间（分钟）')
    parser_interval.set_defaults(func=cmd_set_interval)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    args.func(args)


if __name__ == '__main__':
    main()
