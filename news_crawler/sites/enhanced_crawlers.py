"""
使用增强基类重构的主要新闻爬虫
这些爬虫使用预配置的选择器，可直接使用
"""
from news_crawler.core.enhanced import EnhancedNewsCrawler
from news_crawler.core.selector_configs import (
    get_selector_config,
    get_anti_crawler_config
)


# ========== 美国新闻网站 ==========

class CNNCrawler(EnhancedNewsCrawler):
    """CNN新闻爬虫"""
    name = "cnn"
    base_url = "https://www.cnn.com"
    
    def __init__(self, *args, **kwargs):
        self.selector_config = get_selector_config('cnn')
        self.anti_crawler_config = get_anti_crawler_config('cnn')
        super().__init__(*args, **kwargs)


class NYTimesCrawler(EnhancedNewsCrawler):
    """纽约时报爬虫"""
    name = "nytimes"
    base_url = "https://www.nytimes.com"
    
    def __init__(self, *args, **kwargs):
        self.selector_config = get_selector_config('nytimes')
        self.anti_crawler_config = get_anti_crawler_config('nytimes')
        super().__init__(*args, **kwargs)


class NYTimesChineseCrawler(EnhancedNewsCrawler):
    """纽约时报中文网爬虫"""
    name = "nytimes_chinese"
    base_url = "https://cn.nytimes.com"
    
    def __init__(self, *args, **kwargs):
        self.selector_config = get_selector_config('nytimes_chinese')
        self.anti_crawler_config = get_anti_crawler_config('nytimes')
        super().__init__(*args, **kwargs)


class WSJChineseCrawler(EnhancedNewsCrawler):
    """华尔街日报中文网爬虫"""
    name = "wsj_chinese"
    base_url = "https://cn.wsj.com"
    
    def __init__(self, *args, **kwargs):
        self.selector_config = get_selector_config('wsj_chinese')
        self.anti_crawler_config = get_anti_crawler_config('wsj_chinese')
        super().__init__(*args, **kwargs)


class BloombergCrawler(EnhancedNewsCrawler):
    """彭博社爬虫"""
    name = "bloomberg"
    base_url = "https://www.bloomberg.com"
    
    def __init__(self, *args, **kwargs):
        self.selector_config = get_selector_config('bloomberg')
        self.anti_crawler_config = get_anti_crawler_config('bloomberg')
        super().__init__(*args, **kwargs)


class VOACrawler(EnhancedNewsCrawler):
    """美国之音爬虫"""
    name = "voa"
    base_url = "https://www.voachinese.com"
    
    def __init__(self, *args, **kwargs):
        self.selector_config = get_selector_config('voa')
        self.anti_crawler_config = get_anti_crawler_config('voa')
        super().__init__(*args, **kwargs)


# ========== 英国新闻网站 ==========

class BBCChineseCrawler(EnhancedNewsCrawler):
    """BBC中文网爬虫"""
    name = "bbc_chinese"
    base_url = "https://www.bbc.com/zhongwen/simp"
    
    def __init__(self, *args, **kwargs):
        self.selector_config = get_selector_config('bbc_chinese')
        self.anti_crawler_config = get_anti_crawler_config('bbc_chinese')
        super().__init__(*args, **kwargs)


class ReutersChineseCrawler(EnhancedNewsCrawler):
    """路透中文网爬虫"""
    name = "reuters_chinese"
    base_url = "https://cn.reuters.com"
    
    def __init__(self, *args, **kwargs):
        self.selector_config = get_selector_config('reuters_chinese')
        self.anti_crawler_config = get_anti_crawler_config('reuters_chinese')
        super().__init__(*args, **kwargs)


class GuardianCrawler(EnhancedNewsCrawler):
    """卫报爬虫"""
    name = "guardian"
    base_url = "https://www.theguardian.com"
    
    def __init__(self, *args, **kwargs):
        self.selector_config = get_selector_config('guardian')
        self.anti_crawler_config = get_anti_crawler_config('guardian')
        super().__init__(*args, **kwargs)


class FinancialTimesCrawler(EnhancedNewsCrawler):
    """金融时报爬虫"""
    name = "ft"
    base_url = "https://www.ft.com"
    
    def __init__(self, *args, **kwargs):
        self.selector_config = get_selector_config('ft')
        self.anti_crawler_config = get_anti_crawler_config('ft')
        super().__init__(*args, **kwargs)


class FTChineseCrawler(EnhancedNewsCrawler):
    """金融时报中文网爬虫"""
    name = "ft_chinese"
    base_url = "http://www.ftchinese.com"
    
    def __init__(self, *args, **kwargs):
        self.selector_config = get_selector_config('ft_chinese')
        self.anti_crawler_config = get_anti_crawler_config('ft')
        super().__init__(*args, **kwargs)


# ========== 日本新闻网站 ==========

class NHKNewsCrawler(EnhancedNewsCrawler):
    """NHK新闻网爬虫"""
    name = "nhk_news"
    base_url = "http://www3.nhk.or.jp/news"
    
    def __init__(self, *args, **kwargs):
        self.selector_config = get_selector_config('nhk_news')
        self.anti_crawler_config = get_anti_crawler_config('nhk_news')
        super().__init__(*args, **kwargs)


class AsahiCrawler(EnhancedNewsCrawler):
    """朝日新闻爬虫"""
    name = "asahi"
    base_url = "http://www.asahi.com"
    
    def __init__(self, *args, **kwargs):
        self.selector_config = get_selector_config('asahi')
        self.anti_crawler_config = get_anti_crawler_config('asahi')
        super().__init__(*args, **kwargs)


class NikkeiCNCrawler(EnhancedNewsCrawler):
    """日经新闻中文版爬虫"""
    name = "nikkei_cn"
    base_url = "http://cn.nikkei.com"
    
    def __init__(self, *args, **kwargs):
        self.selector_config = get_selector_config('nikkei_cn')
        self.anti_crawler_config = get_anti_crawler_config('nikkei_cn')
        super().__init__(*args, **kwargs)


class YomiuriCrawler(EnhancedNewsCrawler):
    """读卖新闻爬虫"""
    name = "yomiuri"
    base_url = "http://www.yomiuri.co.jp"
    
    def __init__(self, *args, **kwargs):
        self.selector_config = get_selector_config('yomiuri')
        self.anti_crawler_config = get_anti_crawler_config('yomiuri')
        super().__init__(*args, **kwargs)


# ========== 中文新闻网站 ==========

class ZaobaoCrawler(EnhancedNewsCrawler):
    """联合早报爬虫"""
    name = "zaobao"
    base_url = "http://www.zaobao.com.sg"
    
    def __init__(self, *args, **kwargs):
        self.selector_config = get_selector_config('zaobao')
        self.anti_crawler_config = get_anti_crawler_config('zaobao')
        super().__init__(*args, **kwargs)


class SinchewCrawler(EnhancedNewsCrawler):
    """星洲日报爬虫"""
    name = "sinchew"
    base_url = "http://www.sinchew.com.my"
    
    def __init__(self, *args, **kwargs):
        self.selector_config = get_selector_config('sinchew')
        self.anti_crawler_config = get_anti_crawler_config('sinchew')
        super().__init__(*args, **kwargs)


class HK01Crawler(EnhancedNewsCrawler):
    """香港01爬虫"""
    name = "hk01"
    base_url = "https://www.hk01.com"
    
    def __init__(self, *args, **kwargs):
        self.selector_config = get_selector_config('hk01')
        self.anti_crawler_config = get_anti_crawler_config('hk01')
        super().__init__(*args, **kwargs)


class LTNCrawler(EnhancedNewsCrawler):
    """自由时报爬虫"""
    name = "ltn"
    base_url = "http://www.ltn.com.tw"
    
    def __init__(self, *args, **kwargs):
        self.selector_config = get_selector_config('ltn')
        self.anti_crawler_config = get_anti_crawler_config('ltn')
        super().__init__(*args, **kwargs)


class UDNCrawler(EnhancedNewsCrawler):
    """联合报爬虫"""
    name = "udn"
    base_url = "http://udn.com"
    
    def __init__(self, *args, **kwargs):
        self.selector_config = get_selector_config('udn')
        self.anti_crawler_config = get_anti_crawler_config('udn')
        super().__init__(*args, **kwargs)


class ChinatimesCrawler(EnhancedNewsCrawler):
    """中时电子报爬虫"""
    name = "chinatimes"
    base_url = "http://www.chinatimes.com"
    
    def __init__(self, *args, **kwargs):
        self.selector_config = get_selector_config('chinatimes')
        self.anti_crawler_config = get_anti_crawler_config('chinatimes')
        super().__init__(*args, **kwargs)


class SCMPCrawler(EnhancedNewsCrawler):
    """南华早报爬虫"""
    name = "scmp"
    base_url = "http://www.scmp.com"
    
    def __init__(self, *args, **kwargs):
        self.selector_config = get_selector_config('scmp')
        self.anti_crawler_config = get_anti_crawler_config('scmp')
        super().__init__(*args, **kwargs)


class TakungpaoCrawler(EnhancedNewsCrawler):
    """大公报爬虫"""
    name = "takungpao"
    base_url = "http://www.takungpao.com"
    
    def __init__(self, *args, **kwargs):
        self.selector_config = get_selector_config('takungpao')
        self.anti_crawler_config = get_anti_crawler_config('takungpao')
        super().__init__(*args, **kwargs)


# 导出所有增强版爬虫
ENHANCED_CRAWLERS = {
    # 美国
    'cnn': CNNCrawler,
    'nytimes': NYTimesCrawler,
    'nytimes_chinese': NYTimesChineseCrawler,
    'wsj_chinese': WSJChineseCrawler,
    'bloomberg': BloombergCrawler,
    'voa': VOACrawler,
    
    # 英国
    'bbc_chinese': BBCChineseCrawler,
    'reuters_chinese': ReutersChineseCrawler,
    'guardian': GuardianCrawler,
    'ft': FinancialTimesCrawler,
    'ft_chinese': FTChineseCrawler,
    
    # 日本
    'nhk_news': NHKNewsCrawler,
    'asahi': AsahiCrawler,
    'nikkei_cn': NikkeiCNCrawler,
    'yomiuri': YomiuriCrawler,
    
    # 中文
    'zaobao': ZaobaoCrawler,
    'sinchew': SinchewCrawler,
    'hk01': HK01Crawler,
    'ltn': LTNCrawler,
    'udn': UDNCrawler,
    'chinatimes': ChinatimesCrawler,
    'scmp': SCMPCrawler,
    'takungpao': TakungpaoCrawler,
}
