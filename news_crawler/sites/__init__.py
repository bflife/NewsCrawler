"""
具体网站爬虫实现
"""

from .crawlers import (
    get_crawler,
    register_all_crawlers,
    CRAWLER_FACTORIES
)

__all__ = [
    'get_crawler',
    'register_all_crawlers',
    'CRAWLER_FACTORIES'
]
