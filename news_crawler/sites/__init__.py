"""
具体网站爬虫实现
"""

from .crawlers import (
    get_crawler,
    register_all_crawlers,
    CRAWLER_FACTORIES
)

from .extended_crawlers import (
    get_extended_crawler,
    register_extended_crawlers,
    EXTENDED_CRAWLER_FACTORIES
)

__all__ = [
    'get_crawler',
    'register_all_crawlers',
    'CRAWLER_FACTORIES',
    'get_extended_crawler',
    'register_extended_crawlers',
    'EXTENDED_CRAWLER_FACTORIES'
]
