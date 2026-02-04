"""
示例：创建几个具体的新闻网站爬虫
注意：此文件保留用于向后兼容，新的爬虫请使用 batch*_crawlers.py 系列文件
"""

from typing import Optional


# ===== 中文新闻源 =====
# 注意：这些工厂函数已被废弃，请使用 all_crawlers.py 中的新爬虫类

# ===== 爬虫工厂函数 =====

CRAWLER_FACTORIES = {}


def get_crawler(source_id: str):
    """获取指定新闻源的爬虫（已废弃，请使用 all_crawlers.py）"""
    return None


def register_all_crawlers(scheduler):
    """将所有爬虫注册到调度器"""
    # 使用新的爬虫注册系统
    from .all_crawlers import get_all_crawlers
    
    all_crawlers = get_all_crawlers()
    registered_count = 0
    
    for crawler_class in all_crawlers:
        try:
            # 实例化爬虫并注册
            crawler_instance = crawler_class()
            scheduler.register_crawler(crawler_class.name, crawler_instance)
            registered_count += 1
        except Exception as e:
            print(f"注册爬虫 {crawler_class.name} 失败: {e}")
    
    print(f"已注册 {registered_count} 个爬虫")
    return registered_count
