#!/usr/bin/env python3
"""
测试所有爬虫注册
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, '/home/user/webapp')

from news_crawler.sites.all_crawlers import (
    get_all_crawlers,
    get_supported_countries,
    get_statistics
)

def main():
    """测试爬虫注册"""
    print("=" * 80)
    print("新闻爬虫注册统计")
    print("=" * 80)
    
    # 获取统计信息
    stats = get_statistics()
    
    print(f"\n总爬虫数量: {stats['total_crawlers']}")
    print(f"覆盖国家/地区: {stats['total_countries']}")
    
    print("\n各国家/地区爬虫分布:")
    print("-" * 80)
    
    for country, count in sorted(
        stats['crawlers_per_country'].items(), 
        key=lambda x: x[1], 
        reverse=True
    ):
        print(f"  {country:20s}: {count:3d} 个爬虫")
    
    # 列出所有爬虫
    print("\n" + "=" * 80)
    print("所有已注册爬虫列表:")
    print("=" * 80)
    
    all_crawlers = get_all_crawlers()
    for i, crawler_class in enumerate(all_crawlers, 1):
        print(f"{i:3d}. {crawler_class.name:30s} - {crawler_class.base_url}")
    
    print("\n" + "=" * 80)
    print(f"总计: {len(all_crawlers)} 个爬虫已注册")
    print("=" * 80)

if __name__ == "__main__":
    main()
