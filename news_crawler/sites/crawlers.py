"""
示例：创建几个具体的新闻网站爬虫
"""

from ..generic.crawler import SimpleListCrawler


# ===== 中文新闻源 =====

def create_zaobao_crawler():
    """联合早报（新加坡）"""
    return SimpleListCrawler(
        source_id="zaobao",
        source_name="联合早报",
        base_url="https://www.zaobao.com.sg",
        list_url="https://www.zaobao.com.sg/news/china",
        list_selector="article.article-list__item",
        title_selector="h3.article-list__title::text",
        link_selector="a.article-list__link::attr(href)",
        article_title_selector="h1.headline::text",
        article_content_selector="div.article-content p",
        article_time_selector="time.timestamp::attr(datetime)",
        article_author_selector="span.author::text"
    )


def create_sinchew_crawler():
    """星洲日报（马来西亚）"""
    return SimpleListCrawler(
        source_id="sinchew",
        source_name="星洲日报",
        base_url="https://www.sinchew.com.my",
        list_url="https://www.sinchew.com.my/news",
        list_selector="div.article-item",
        title_selector="h3.title a::text",
        link_selector="h3.title a::attr(href)",
        article_title_selector="h1.article-title::text",
        article_content_selector="div.article-body p",
        article_time_selector="time.timestamp::text",
        article_author_selector="span.author::text"
    )


def create_hk01_crawler():
    """香港01"""
    return SimpleListCrawler(
        source_id="hk01",
        source_name="香港01",
        base_url="https://www.hk01.com",
        list_url="https://www.hk01.com/zone/1/%E5%8D%B3%E6%99%82",
        list_selector="article.article-card",
        title_selector="h2.article-title a::text",
        link_selector="h2.article-title a::attr(href)",
        article_title_selector="h1.article-detail-title::text",
        article_content_selector="div.article-content p",
        article_time_selector="time.timestamp::attr(datetime)",
        article_author_selector="span.author::text"
    )


def create_ltn_crawler():
    """自由时报（台湾）"""
    return SimpleListCrawler(
        source_id="ltn",
        source_name="自由时报",
        base_url="https://www.ltn.com.tw",
        list_url="https://www.ltn.com.tw/list/breakingnews",
        list_selector="li.row",
        title_selector="p.title a::text",
        link_selector="p.title a::attr(href)",
        article_title_selector="h1::text",
        article_content_selector="div.text p",
        article_time_selector="span.time::text",
        article_author_selector="span.reporter::text"
    )


# ===== 日本新闻源 =====

def create_nhk_crawler():
    """NHK新闻"""
    return SimpleListCrawler(
        source_id="nhk",
        source_name="NHK新闻网",
        base_url="https://www3.nhk.or.jp",
        list_url="https://www3.nhk.or.jp/news/",
        list_selector="li.article-card",
        title_selector="h3.article-title::text",
        link_selector="a.article-link::attr(href)",
        article_title_selector="h1.article-title::text",
        article_content_selector="div.article-body p",
        article_time_selector="time.timestamp::text",
        article_author_selector="span.author::text"
    )


def create_asahi_crawler():
    """朝日新闻"""
    return SimpleListCrawler(
        source_id="asahi",
        source_name="朝日新闻",
        base_url="https://www.asahi.com",
        list_url="https://www.asahi.com/news/",
        list_selector="div.List",
        title_selector="h3.Title a::text",
        link_selector="h3.Title a::attr(href)",
        article_title_selector="h1.Title::text",
        article_content_selector="div.ArticleText p",
        article_time_selector="time.time::attr(datetime)",
        article_author_selector="span.Author::text"
    )


# ===== 英文新闻源 =====

def create_scmp_crawler():
    """南华早报（香港）"""
    return SimpleListCrawler(
        source_id="scmp",
        source_name="南华早报",
        base_url="https://www.scmp.com",
        list_url="https://www.scmp.com/news/china",
        list_selector="div.card",
        title_selector="h2.card__headline a::text",
        link_selector="h2.card__headline a::attr(href)",
        article_title_selector="h1.article-headline::text",
        article_content_selector="div.article-body p",
        article_time_selector="time::attr(datetime)",
        article_author_selector="span.author::text"
    )


def create_reuters_crawler():
    """路透社中文网"""
    return SimpleListCrawler(
        source_id="reuters_cn",
        source_name="路透中文网",
        base_url="https://cn.reuters.com",
        list_url="https://cn.reuters.com/news/archive/CNTopGenNews",
        list_selector="div.story",
        title_selector="h3.story-title a::text",
        link_selector="h3.story-title a::attr(href)",
        article_title_selector="h1.article-headline::text",
        article_content_selector="div.article-body p",
        article_time_selector="span.timestamp::text",
        article_author_selector="span.author::text"
    )


# ===== 爬虫工厂函数 =====

CRAWLER_FACTORIES = {
    'zaobao': create_zaobao_crawler,
    'sinchew': create_sinchew_crawler,
    'hk01': create_hk01_crawler,
    'ltn': create_ltn_crawler,
    'nhk': create_nhk_crawler,
    'asahi': create_asahi_crawler,
    'scmp': create_scmp_crawler,
    'reuters_cn': create_reuters_crawler,
}


def get_crawler(source_id: str):
    """获取指定新闻源的爬虫"""
    factory = CRAWLER_FACTORIES.get(source_id)
    if factory:
        return factory()
    return None


def register_all_crawlers(scheduler):
    """将所有爬虫注册到调度器"""
    # 注册基础爬虫
    for source_id, factory in CRAWLER_FACTORIES.items():
        crawler = factory()
        scheduler.register_crawler(source_id, crawler)
    
    # 注册扩展爬虫
    from .extended_crawlers import register_extended_crawlers
    register_extended_crawlers(scheduler)
    
    total = len(CRAWLER_FACTORIES) + len(scheduler.crawlers) - len(CRAWLER_FACTORIES)
    print(f"已注册 {len(scheduler.crawlers)} 个爬虫")
