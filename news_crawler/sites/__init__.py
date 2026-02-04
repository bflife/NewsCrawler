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

from .all_crawlers import (
    CRAWLER_REGISTRY,
    CRAWLER_BY_NAME,
    get_all_crawlers,
    get_crawlers_by_country,
    get_crawler_by_name,
    get_supported_countries,
    get_statistics
)

__all__ = [
    'get_crawler',
    'register_all_crawlers',
    'CRAWLER_FACTORIES',
    'get_extended_crawler',
    'register_extended_crawlers',
    'EXTENDED_CRAWLER_FACTORIES',
    'CRAWLER_REGISTRY',
    'CRAWLER_BY_NAME',
    'get_all_crawlers',
    'get_crawlers_by_country',
    'get_crawler_by_name',
    'get_supported_countries',
    'get_statistics'
]
