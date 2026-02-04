"""
International News Crawler Module

Supports crawling news from international news websites across different countries/regions.
"""

# Lazy imports to avoid loading heavy dependencies when just importing configs
__all__ = [
    'InternationalNewsCrawler',
    'NewsScheduler',
    'ConfigManager',
]


def __getattr__(name):
    """Lazy import to avoid loading dependencies at module import time"""
    if name == 'InternationalNewsCrawler':
        from .base_crawler import InternationalNewsCrawler
        return InternationalNewsCrawler
    elif name == 'NewsScheduler':
        from .scheduler import NewsScheduler
        return NewsScheduler
    elif name == 'ConfigManager':
        from .config_manager import ConfigManager
        return ConfigManager
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
