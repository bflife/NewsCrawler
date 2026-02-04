"""
更多新闻网站爬虫实现
注意：此文件已被 batch*_crawlers.py 系列文件取代
保留用于向后兼容
"""

# 所有扩展爬虫已移至 batch*_crawlers.py 文件

EXTENDED_CRAWLER_FACTORIES = {}


def get_extended_crawler(source_id: str):
    """获取扩展爬虫（已废弃）"""
    return None


def register_extended_crawlers(scheduler):
    """注册扩展爬虫（已废弃，现在统一使用 all_crawlers.py）"""
    pass
