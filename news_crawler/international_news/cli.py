"""
Command-line tool for International News Crawler

Usage:
    # Scan all sites once
    python -m news_crawler.international_news.cli scan --all
    
    # Scan specific country
    python -m news_crawler.international_news.cli scan --country 美国
    
    # Scan specific region
    python -m news_crawler.international_news.cli scan --region 东亚
    
    # Start continuous scanning
    python -m news_crawler.international_news.cli start --interval 3600
    
    # List all sites
    python -m news_crawler.international_news.cli list --country 日本
    
    # View statistics
    python -m news_crawler.international_news.cli stats --days 7
    
    # Configure site
    python -m news_crawler.international_news.cli config --site "BBC" --interval 7200 --enable
"""

import argparse
import sys
from typing import Optional

from .config_manager import ConfigManager
from .scheduler import NewsScheduler
from .configs.sites_config import get_all_countries, REGION_GROUPS


def cmd_list(args):
    """List sites command"""
    manager = ConfigManager()
    manager.load_site_configs()
    
    if args.countries:
        print("\n可用国家/地区:")
        for country in get_all_countries():
            print(f"  - {country}")
        return
    
    if args.regions:
        print("\n可用地区分组:")
        for region, countries in REGION_GROUPS.items():
            print(f"  {region}: {', '.join(countries)}")
        return
    
    sites = manager.get_sites_by_filter(
        country=args.country,
        region=args.region,
        enabled_only=not args.all
    )
    
    if not sites:
        print("未找到符合条件的网站")
        return
    
    print(f"\n找到 {len(sites)} 个网站:")
    print("-" * 80)
    
    current_country = None
    for site in sites:
        if site['country'] != current_country:
            current_country = site['country']
            print(f"\n【{current_country}】")
        
        enabled_str = "✓" if site['enabled'] else "✗"
        interval_str = f"{site['scan_interval']}s"
        last_scan = site['last_scan_time'] or "从未扫描"
        
        print(f"  [{enabled_str}] {site['site_name']}")
        print(f"      URL: {site['site_url']}")
        print(f"      扫描间隔: {interval_str}, 最后扫描: {last_scan}")


def cmd_scan(args):
    """Scan sites command"""
    manager = ConfigManager()
    manager.load_site_configs()
    
    scheduler = NewsScheduler(
        config_manager=manager,
        max_workers=args.workers
    )
    
    print("\n开始扫描新闻网站...")
    print("=" * 80)
    
    if args.all:
        print("扫描所有网站")
    elif args.country:
        print(f"扫描国家: {args.country}")
    elif args.region:
        print(f"扫描地区: {args.region}")
    
    results = scheduler.scan_all_sites(
        country=args.country,
        region=args.region,
        max_articles_per_site=args.max_articles,
        parallel=args.parallel
    )
    
    print("\n" + "=" * 80)
    print("扫描结果:")
    print("=" * 80)
    
    successful = sum(1 for r in results if r['status'] == 'success')
    failed = sum(1 for r in results if r['status'] == 'failed')
    total_new = sum(r['new_articles'] for r in results)
    total_crawled = sum(r['articles_crawled'] for r in results)
    
    print(f"\n总共扫描: {len(results)} 个网站")
    print(f"成功: {successful}, 失败: {failed}")
    print(f"发现新文章: {total_new}")
    print(f"爬取文章: {total_crawled}")
    
    if args.verbose:
        print("\n详细结果:")
        for result in results:
            status_icon = "✓" if result['status'] == 'success' else "✗"
            print(f"\n  [{status_icon}] {result['site_name']} ({result['country']})")
            print(f"      发现文章: {result['articles_found']}, 新文章: {result['new_articles']}, 已爬取: {result['articles_crawled']}")
            
            if result['status'] == 'failed':
                print(f"      错误: {result['error_message']}")
            
            if result['articles'] and args.show_articles:
                print(f"      新文章列表:")
                for article in result['articles'][:5]:  # Show first 5
                    print(f"        - {article['title']}")
                    print(f"          {article['url']}")


def cmd_start(args):
    """Start continuous scanning"""
    manager = ConfigManager()
    manager.load_site_configs()
    
    scheduler = NewsScheduler(
        config_manager=manager,
        max_workers=args.workers
    )
    
    print("\n启动持续扫描模式...")
    print("=" * 80)
    print(f"检查间隔: {args.interval} 秒")
    print(f"每个网站最多爬取: {args.max_articles} 篇文章")
    
    if args.country:
        print(f"限定国家: {args.country}")
    if args.region:
        print(f"限定地区: {args.region}")
    
    print("\n按 Ctrl+C 停止")
    print("=" * 80)
    
    try:
        scheduler.start_continuous_scanning(
            check_interval=args.interval,
            country=args.country,
            region=args.region,
            max_articles_per_site=args.max_articles
        )
    except KeyboardInterrupt:
        print("\n\n收到停止信号...")
        scheduler.stop()


def cmd_stats(args):
    """View statistics"""
    manager = ConfigManager()
    
    stats = manager.get_crawl_statistics(days=args.days)
    
    print("\n爬取统计信息")
    print("=" * 80)
    print(f"时间范围: 最近 {stats['days']} 天")
    print(f"总爬取次数: {stats['total_crawls']}")
    print(f"成功: {stats['successful_crawls']}")
    print(f"失败: {stats['failed_crawls']}")
    print(f"成功率: {stats['success_rate']}")
    print(f"爬取文章总数: {stats['total_articles']}")
    
    if stats['by_country']:
        print(f"\n按国家/地区统计:")
        for country, count in sorted(stats['by_country'].items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {country}: {count} 次")
    
    if args.history:
        print("\n" + "=" * 80)
        print("最近爬取历史:")
        print("=" * 80)
        
        history = manager.get_crawl_history(limit=args.limit)
        for record in history:
            status_icon = "✓" if record['status'] == 'success' else "✗"
            print(f"\n[{status_icon}] {record['site_name']} ({record['country']})")
            print(f"    时间: {record['crawl_time']}")
            print(f"    状态: {record['status']}")
            
            if record['article_title']:
                print(f"    文章: {record['article_title']}")
            if record['article_count']:
                print(f"    爬取数量: {record['article_count']}")
            if record['error_message']:
                print(f"    错误: {record['error_message']}")


def cmd_config(args):
    """Configure site settings"""
    manager = ConfigManager()
    manager.load_site_configs()
    
    if args.list_sites:
        sites = manager.get_sites_by_filter()
        print(f"\n可配置的网站 (共 {len(sites)} 个):")
        for site in sites[:50]:  # Show first 50
            enabled = "✓" if site['enabled'] else "✗"
            print(f"  [{enabled}] {site['site_name']} - 间隔: {site['scan_interval']}s")
        
        if len(sites) > 50:
            print(f"\n... 还有 {len(sites) - 50} 个网站")
        return
    
    if not args.site:
        print("错误: 需要指定 --site 参数")
        return
    
    # Update configuration
    updates = {}
    if args.enable is not None:
        updates['enabled'] = args.enable
    if args.interval is not None:
        updates['scan_interval'] = args.interval
    
    if updates:
        if 'enabled' in updates:
            manager.update_site_config(args.site, enabled=updates['enabled'])
        if 'scan_interval' in updates:
            manager.update_site_config(args.site, scan_interval=updates['scan_interval'])
        
        print(f"\n已更新网站配置: {args.site}")
        for key, value in updates.items():
            print(f"  {key}: {value}")
    else:
        print("错误: 需要指定 --enable 或 --interval 参数")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="国际新闻爬虫命令行工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # List command
    list_parser = subparsers.add_parser('list', help='列出网站')
    list_parser.add_argument('--country', help='按国家过滤')
    list_parser.add_argument('--region', help='按地区过滤')
    list_parser.add_argument('--all', action='store_true', help='包含禁用的网站')
    list_parser.add_argument('--countries', action='store_true', help='列出所有国家')
    list_parser.add_argument('--regions', action='store_true', help='列出所有地区')
    
    # Scan command
    scan_parser = subparsers.add_parser('scan', help='扫描网站')
    scan_parser.add_argument('--all', action='store_true', help='扫描所有网站')
    scan_parser.add_argument('--country', help='扫描指定国家')
    scan_parser.add_argument('--region', help='扫描指定地区')
    scan_parser.add_argument('--max-articles', type=int, default=10, help='每个网站最多爬取文章数')
    scan_parser.add_argument('--workers', type=int, default=5, help='并发线程数')
    scan_parser.add_argument('--parallel', action='store_true', default=True, help='使用并行处理')
    scan_parser.add_argument('--verbose', action='store_true', help='显示详细信息')
    scan_parser.add_argument('--show-articles', action='store_true', help='显示文章列表')
    
    # Start command
    start_parser = subparsers.add_parser('start', help='启动持续扫描')
    start_parser.add_argument('--interval', type=int, default=3600, help='检查间隔(秒)')
    start_parser.add_argument('--country', help='限定国家')
    start_parser.add_argument('--region', help='限定地区')
    start_parser.add_argument('--max-articles', type=int, default=10, help='每个网站最多爬取文章数')
    start_parser.add_argument('--workers', type=int, default=5, help='并发线程数')
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='查看统计信息')
    stats_parser.add_argument('--days', type=int, default=7, help='统计天数')
    stats_parser.add_argument('--history', action='store_true', help='显示历史记录')
    stats_parser.add_argument('--limit', type=int, default=20, help='历史记录数量')
    
    # Config command
    config_parser = subparsers.add_parser('config', help='配置网站')
    config_parser.add_argument('--site', help='网站名称')
    config_parser.add_argument('--interval', type=int, help='扫描间隔(秒)')
    config_parser.add_argument('--enable', action='store_true', help='启用网站')
    config_parser.add_argument('--disable', dest='enable', action='store_false', help='禁用网站')
    config_parser.add_argument('--list-sites', action='store_true', help='列出所有可配置网站')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Execute command
    if args.command == 'list':
        cmd_list(args)
    elif args.command == 'scan':
        cmd_scan(args)
    elif args.command == 'start':
        cmd_start(args)
    elif args.command == 'stats':
        cmd_stats(args)
    elif args.command == 'config':
        cmd_config(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
