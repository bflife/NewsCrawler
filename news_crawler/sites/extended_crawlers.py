"""
更多新闻网站爬虫实现
基于通用爬虫框架，快速扩展支持更多网站
"""

from ..generic.crawler import SimpleListCrawler


# ===== 美国新闻源 =====

def create_cnn_crawler():
    """CNN"""
    return SimpleListCrawler(
        source_id="cnn",
        source_name="CNN",
        base_url="https://www.cnn.com",
        list_url="https://www.cnn.com/world",
        list_selector="div.container__item",
        title_selector="span.container__headline-text::text",
        link_selector="a.container__link::attr(href)",
        article_title_selector="h1.headline__text::text",
        article_content_selector="div.article__content p",
        article_time_selector="div.timestamp::text",
        article_author_selector="span.byline__name::text"
    )


def create_nytimes_crawler():
    """纽约时报"""
    return SimpleListCrawler(
        source_id="nytimes",
        source_name="纽约时报",
        base_url="https://www.nytimes.com",
        list_url="https://www.nytimes.com/section/world",
        list_selector="article",
        title_selector="h3::text",
        link_selector="a::attr(href)",
        article_title_selector="h1[data-testid='headline']::text",
        article_content_selector="section[name='articleBody'] p",
        article_time_selector="time::attr(datetime)",
        article_author_selector="span[itemprop='name']::text"
    )


def create_wsj_crawler():
    """华尔街日报中文网"""
    return SimpleListCrawler(
        source_id="wsj",
        source_name="华尔街日报",
        base_url="https://cn.wsj.com",
        list_url="https://cn.wsj.com/zh-hans",
        list_selector="article.WSJTheme--story",
        title_selector="h3.WSJTheme--headline::text",
        link_selector="a::attr(href)",
        article_title_selector="h1.article-headline::text",
        article_content_selector="div.article-content p",
        article_time_selector="time::attr(datetime)",
        article_author_selector="span.author-name::text"
    )


def create_bbc_crawler():
    """BBC中文网"""
    return SimpleListCrawler(
        source_id="bbc",
        source_name="BBC",
        base_url="https://www.bbc.com",
        list_url="https://www.bbc.com/zhongwen/simp",
        list_selector="div.bbc-uk8dsi",
        title_selector="h3.bbc-1h96w3y::text",
        link_selector="a::attr(href)",
        article_title_selector="h1.bbc-1rvvczj::text",
        article_content_selector="div[data-component='text-block'] p",
        article_time_selector="time::attr(datetime)",
        article_author_selector="div.ssrcss-68pt20-Text-TextContributorName::text"
    )


def create_rfa_crawler():
    """自由亚洲电台"""
    return SimpleListCrawler(
        source_id="rfa",
        source_name="自由亚洲电台",
        base_url="https://www.rfa.org",
        list_url="https://www.rfa.org/mandarin/",
        list_selector="div.sectionteaser",
        title_selector="h2 a::text",
        link_selector="h2 a::attr(href)",
        article_title_selector="h1.title::text",
        article_content_selector="div#storytext p",
        article_time_selector="span.date::text",
        article_author_selector="span.byline::text"
    )


# ===== 英国新闻源 =====

def create_reuters_crawler():
    """路透社中文网"""
    return SimpleListCrawler(
        source_id="reuters_cn",
        source_name="路透中文网",
        base_url="https://cn.reuters.com",
        list_url="https://cn.reuters.com/world",
        list_selector="div.story-content",
        title_selector="h3.story-title a::text",
        link_selector="h3.story-title a::attr(href)",
        article_title_selector="h1.ArticleHeader_headline::text",
        article_content_selector="div.StandardArticleBody_body p",
        article_time_selector="time::attr(datetime)",
        article_author_selector="div.Attribution_content span::text"
    )


def create_ft_crawler():
    """金融时报中文网"""
    return SimpleListCrawler(
        source_id="ftchinese",
        source_name="金融时报中文网",
        base_url="http://www.ftchinese.com",
        list_url="http://www.ftchinese.com/channel/china.html",
        list_selector="div.story-container",
        title_selector="div.story-headline a::text",
        link_selector="div.story-headline a::attr(href)",
        article_title_selector="h1.story-headline::text",
        article_content_selector="div.story-body p",
        article_time_selector="time.story-time::text",
        article_author_selector="div.story-author a::text"
    )


def create_guardian_crawler():
    """卫报"""
    return SimpleListCrawler(
        source_id="guardian",
        source_name="卫报",
        base_url="https://www.theguardian.com",
        list_url="https://www.theguardian.com/world",
        list_selector="div.fc-item",
        title_selector="span.js-headline-text::text",
        link_selector="a.js-headline-text::attr(href)",
        article_title_selector="h1.content__headline::text",
        article_content_selector="div.content__article-body p",
        article_time_selector="time::attr(datetime)",
        article_author_selector="a.contributor::text"
    )


# ===== 台湾新闻源 =====

def create_udn_crawler():
    """联合报"""
    return SimpleListCrawler(
        source_id="udn",
        source_name="联合报",
        base_url="https://udn.com",
        list_url="https://udn.com/news/breaknews/1",
        list_selector="div.story-list__item",
        title_selector="h3::text",
        link_selector="a::attr(href)",
        article_title_selector="h1.article-content__title::text",
        article_content_selector="div.article-content__editor p",
        article_time_selector="time.article-content__time::text",
        article_author_selector="span.article-content__author::text"
    )


def create_chinatimes_crawler():
    """中时电子报"""
    return SimpleListCrawler(
        source_id="chinatimes",
        source_name="中时电子报",
        base_url="https://www.chinatimes.com",
        list_url="https://www.chinatimes.com/realtimenews/",
        list_selector="div.article-box",
        title_selector="h3.title a::text",
        link_selector="h3.title a::attr(href)",
        article_title_selector="h1.article-title::text",
        article_content_selector="div.article-body p",
        article_time_selector="time.article-date::text",
        article_author_selector="div.author a::text"
    )


def create_storm_crawler():
    """风传媒"""
    return SimpleListCrawler(
        source_id="storm",
        source_name="风传媒",
        base_url="https://www.storm.mg",
        list_url="https://www.storm.mg/articles",
        list_selector="div.card_inner",
        title_selector="h3.card_title a::text",
        link_selector="h3.card_title a::attr(href)",
        article_title_selector="h1.article_title::text",
        article_content_selector="div.article_content p",
        article_time_selector="time::attr(datetime)",
        article_author_selector="a.link_author::text"
    )


# ===== 香港新闻源 =====

def create_mingpao_crawler():
    """明报"""
    return SimpleListCrawler(
        source_id="mingpao",
        source_name="明报",
        base_url="https://www.mingpao.com",
        list_url="https://www.mingpao.com/ins/",
        list_selector="div.headline-item",
        title_selector="h3 a::text",
        link_selector="h3 a::attr(href)",
        article_title_selector="h1.article-title::text",
        article_content_selector="div.article-content p",
        article_time_selector="span.article-time::text",
        article_author_selector="span.article-author::text"
    )


def create_takungpao_crawler():
    """大公报"""
    return SimpleListCrawler(
        source_id="takungpao",
        source_name="大公报",
        base_url="http://www.takungpao.com",
        list_url="http://www.takungpao.com/news/",
        list_selector="div.news-item",
        title_selector="h3 a::text",
        link_selector="h3 a::attr(href)",
        article_title_selector="h1.title::text",
        article_content_selector="div.content p",
        article_time_selector="span.time::text",
        article_author_selector="span.source::text"
    )


# ===== 日本新闻源 =====

def create_nikkei_cn_crawler():
    """日经中文网"""
    return SimpleListCrawler(
        source_id="nikkei_cn",
        source_name="日经新闻中文版",
        base_url="https://cn.nikkei.com",
        list_url="https://cn.nikkei.com/news/",
        list_selector="div.news-item",
        title_selector="h3 a::text",
        link_selector="h3 a::attr(href)",
        article_title_selector="h1.article-title::text",
        article_content_selector="div.article-body p",
        article_time_selector="time::text",
        article_author_selector="span.author::text"
    )


def create_kyodonews_crawler():
    """共同社中文网"""
    return SimpleListCrawler(
        source_id="kyodonews",
        source_name="共同社",
        base_url="https://china.kyodonews.net",
        list_url="https://china.kyodonews.net/news",
        list_selector="div.news-list-item",
        title_selector="h3 a::text",
        link_selector="h3 a::attr(href)",
        article_title_selector="h1.news-title::text",
        article_content_selector="div.news-content p",
        article_time_selector="time::text",
        article_author_selector="span.news-source::text"
    )


# ===== 韩国新闻源 =====

def create_yonhap_crawler():
    """韩联社中文网"""
    return SimpleListCrawler(
        source_id="yonhapnews",
        source_name="韩联社",
        base_url="https://cn.yna.co.kr",
        list_url="https://cn.yna.co.kr/news",
        list_selector="div.news-item",
        title_selector="h3 a::text",
        link_selector="h3 a::attr(href)",
        article_title_selector="h1.article-title::text",
        article_content_selector="div.article-body p",
        article_time_selector="time::text",
        article_author_selector="span.reporter::text"
    )


# ===== 马来西亚新闻源 =====

def create_chinapress_crawler():
    """中国报"""
    return SimpleListCrawler(
        source_id="chinapress",
        source_name="中国报",
        base_url="https://www.chinapress.com.my",
        list_url="https://www.chinapress.com.my/news/",
        list_selector="div.article-item",
        title_selector="h3 a::text",
        link_selector="h3 a::attr(href)",
        article_title_selector="h1.article-title::text",
        article_content_selector="div.article-content p",
        article_time_selector="time::text",
        article_author_selector="span.author::text"
    )


def create_orientaldaily_my_crawler():
    """东方日报（马来西亚）"""
    return SimpleListCrawler(
        source_id="orientaldaily_my",
        source_name="东方日报",
        base_url="https://www.orientaldaily.com.my",
        list_url="https://www.orientaldaily.com.my/news",
        list_selector="div.news-item",
        title_selector="h3 a::text",
        link_selector="h3 a::attr(href)",
        article_title_selector="h1.title::text",
        article_content_selector="div.content p",
        article_time_selector="span.date::text",
        article_author_selector="span.author::text"
    )


# ===== 更新爬虫工厂 =====

EXTENDED_CRAWLER_FACTORIES = {
    # 美国
    'cnn': create_cnn_crawler,
    'nytimes': create_nytimes_crawler,
    'wsj': create_wsj_crawler,
    'bbc': create_bbc_crawler,
    'rfa': create_rfa_crawler,
    
    # 英国
    'reuters_cn': create_reuters_crawler,
    'ftchinese': create_ft_crawler,
    'guardian': create_guardian_crawler,
    
    # 台湾
    'udn': create_udn_crawler,
    'chinatimes': create_chinatimes_crawler,
    'storm': create_storm_crawler,
    
    # 香港
    'mingpao': create_mingpao_crawler,
    'takungpao': create_takungpao_crawler,
    
    # 日本
    'nikkei_cn': create_nikkei_cn_crawler,
    'kyodonews': create_kyodonews_crawler,
    
    # 韩国
    'yonhapnews': create_yonhap_crawler,
    
    # 马来西亚
    'chinapress': create_chinapress_crawler,
    'orientaldaily_my': create_orientaldaily_my_crawler,
}


def get_extended_crawler(source_id: str):
    """获取扩展的爬虫"""
    factory = EXTENDED_CRAWLER_FACTORIES.get(source_id)
    if factory:
        return factory()
    return None


def register_extended_crawlers(scheduler):
    """注册所有扩展爬虫"""
    for source_id, factory in EXTENDED_CRAWLER_FACTORIES.items():
        crawler = factory()
        scheduler.register_crawler(source_id, crawler)
    print(f"已注册 {len(EXTENDED_CRAWLER_FACTORIES)} 个扩展爬虫")
