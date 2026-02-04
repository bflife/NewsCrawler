"""
主要新闻网站的选择器配置
为常见新闻网站提供预配置的选择器
"""
from news_crawler.core.enhanced import SelectorConfig, AntiCrawlerConfig


# ========== 美国新闻网站 ==========

CNN_CONFIG = SelectorConfig(
    article_title='h1.headline__text, h1',
    article_content='div.article__content, div.zn-body__paragraph',
    article_author='span.byline__name',
    article_date='div.timestamp',
    article_images='img.media__image',
    remove_selectors=[
        'script', 'style', 'iframe', '.ad', '.advertisement',
        '.social-share', '.related-content'
    ]
)

NYT_CONFIG = SelectorConfig(
    article_title='h1[data-testid="headline"], h1.css-1d7o96w',
    article_content='section[name="articleBody"], div.article-body',
    article_author='span[itemprop="name"], p.css-1n7hynb',
    article_date='time',
    article_images='figure img',
    remove_selectors=[
        'script', 'style', 'iframe', 'aside', '.ad',
        '.css-xqjis6'  # 订阅提示
    ]
)

WSJ_CONFIG = SelectorConfig(
    article_title='h1.wsj-article-headline, h1',
    article_content='div.article-content, div.wsj-snippet-body',
    article_author='span.author-name',
    article_date='time.timestamp',
    article_images='figure img',
    remove_selectors=[
        'script', 'style', 'iframe', '.wsj-ad',
        '.article-share-tools'
    ]
)

BLOOMBERG_CONFIG = SelectorConfig(
    article_title='h1.lede-text-v2__hed',
    article_content='div.body-content',
    article_author='div.author-v2',
    article_date='time',
    remove_selectors=[
        'script', 'style', 'iframe', '.ad-container',
        '.paywall-banner'
    ]
)

VOA_CONFIG = SelectorConfig(
    article_title='h1.title',
    article_content='div.wsw, div.body-container',
    article_author='div.author',
    article_date='time.published',
    article_images='div.media-block img',
    remove_selectors=['script', 'style', 'iframe', '.ad']
)

# ========== 英国新闻网站 ==========

BBC_CONFIG = SelectorConfig(
    article_title='h1#main-heading, h1',
    article_content='div[data-component="text-block"], article',
    article_date='time',
    article_images='figure img',
    remove_selectors=[
        'script', 'style', 'iframe', '.ssrcss-1q0x1qg-Promo',
        'aside'
    ]
)

REUTERS_CONFIG = SelectorConfig(
    article_title='h1.ArticleHeader_headline',
    article_content='div.StandardArticleBody_body',
    article_author='div.BylineBar_byline',
    article_date='time.ArticleHeader_date',
    article_images='figure img',
    remove_selectors=['script', 'style', 'iframe', '.ad-slot']
)

GUARDIAN_CONFIG = SelectorConfig(
    article_title='h1.dcr-1aw8r8j',
    article_content='div.article-body-commercial-selector',
    article_author='a[rel="author"]',
    article_date='time',
    article_images='figure img',
    remove_selectors=[
        'script', 'style', 'iframe', '.ad-slot',
        '.submeta'
    ]
)

FT_CONFIG = SelectorConfig(
    article_title='h1.o-topper__headline',
    article_content='div.article__content-body',
    article_author='a.n-content-tag--author',
    article_date='time.article__timestamp',
    remove_selectors=[
        'script', 'style', 'iframe', '.n-content-related-box'
    ]
)

# ========== 日本新闻网站 ==========

NHK_CONFIG = SelectorConfig(
    article_title='h1.content--title, h1',
    article_content='div.content--detail-body, div.body',
    article_date='div.content--date, time',
    article_images='figure img',
    remove_selectors=['script', 'style', 'iframe', '.ad']
)

ASAHI_CONFIG = SelectorConfig(
    article_title='h1.Title, h1',
    article_content='div.ArticleText, div.article-body',
    article_author='span.Author',
    article_date='time.time, time',
    article_images='figure img',
    remove_selectors=['script', 'style', 'iframe', '.ad', '.Banner']
)

NIKKEI_CONFIG = SelectorConfig(
    article_title='h1.article_headline, h1',
    article_content='div.article_body, div.content',
    article_date='time.article_date, time',
    article_images='figure img',
    remove_selectors=['script', 'style', 'iframe', '.ad-area']
)

YOMIURI_CONFIG = SelectorConfig(
    article_title='h1.p-main-title',
    article_content='div.p-main-text',
    article_date='time.p-article-date',
    remove_selectors=['script', 'style', 'iframe', '.ad']
)

# ========== 中文新闻网站 ==========

ZAOBAO_CONFIG = SelectorConfig(
    article_title='h1.headline, h1',
    article_content='div.article-content, div.field-content',
    article_author='span.author',
    article_date='time.timestamp',
    article_images='figure img',
    remove_selectors=['script', 'style', 'iframe', '.ad']
)

SINCHEW_CONFIG = SelectorConfig(
    article_title='h1.article-title, h1',
    article_content='div.article-body, div.content',
    article_author='span.author',
    article_date='time.timestamp, time',
    article_images='figure img, div.img-wrap img',
    remove_selectors=['script', 'style', 'iframe', '.ad']
)

HK01_CONFIG = SelectorConfig(
    article_title='h1.article-detail-title, h1',
    article_content='div.article-content, div.article-detail-body',
    article_author='span.author',
    article_date='time.timestamp',
    article_images='figure img',
    remove_selectors=['script', 'style', 'iframe', '.ad', '.related']
)

LTN_CONFIG = SelectorConfig(
    article_title='h1, div.whitecon h1',
    article_content='div.text, div.content',
    article_author='span.reporter',
    article_date='span.time, time',
    article_images='div.image img',
    remove_selectors=['script', 'style', 'iframe', '.ad', '.boxTitle']
)

UDN_CONFIG = SelectorConfig(
    article_title='h1.article-title, h1',
    article_content='div.article-content, section.article-body',
    article_author='span.article-author',
    article_date='time, span.article-date',
    article_images='figure img',
    remove_selectors=['script', 'style', 'iframe', '.ad']
)

CHINATIMES_CONFIG = SelectorConfig(
    article_title='h1.article-title, h1',
    article_content='div.article-body, div.article-content',
    article_author='span.author',
    article_date='time, span.date',
    article_images='figure img',
    remove_selectors=['script', 'style', 'iframe', '.ad', '.box-fb']
)

SCMP_CONFIG = SelectorConfig(
    article_title='h1.article-headline, h1',
    article_content='div.article-body, section.article-content',
    article_author='span.author',
    article_date='time',
    article_images='figure img',
    remove_selectors=['script', 'style', 'iframe', '.ad']
)

TAKUNGPAO_CONFIG = SelectorConfig(
    article_title='h1.title, h1',
    article_content='div.content, div.article-content',
    article_date='span.time, time',
    remove_selectors=['script', 'style', 'iframe', '.ad']
)

# ========== 配置映射表 ==========

SELECTOR_CONFIGS = {
    # 美国
    'cnn': CNN_CONFIG,
    'nytimes': NYT_CONFIG,
    'nytimes_chinese': NYT_CONFIG,
    'wsj_chinese': WSJ_CONFIG,
    'bloomberg': BLOOMBERG_CONFIG,
    'voa': VOA_CONFIG,
    
    # 英国
    'bbc_chinese': BBC_CONFIG,
    'reuters_chinese': REUTERS_CONFIG,
    'guardian': GUARDIAN_CONFIG,
    'ft': FT_CONFIG,
    'ft_chinese': FT_CONFIG,
    
    # 日本
    'nhk_news': NHK_CONFIG,
    'asahi': ASAHI_CONFIG,
    'nikkei_cn': NIKKEI_CONFIG,
    'nikkei_jp': NIKKEI_CONFIG,
    'yomiuri': YOMIURI_CONFIG,
    
    # 中文
    'zaobao': ZAOBAO_CONFIG,
    'sinchew': SINCHEW_CONFIG,
    'hk01': HK01_CONFIG,
    'ltn': LTN_CONFIG,
    'udn': UDN_CONFIG,
    'chinatimes': CHINATIMES_CONFIG,
    'scmp': SCMP_CONFIG,
    'takungpao': TAKUNGPAO_CONFIG,
}


def get_selector_config(crawler_name: str) -> SelectorConfig:
    """
    获取指定爬虫的选择器配置
    
    Args:
        crawler_name: 爬虫名称
        
    Returns:
        SelectorConfig: 选择器配置，如果未找到则返回默认配置
    """
    return SELECTOR_CONFIGS.get(crawler_name, SelectorConfig())


# ========== 反爬配置 ==========

# 通用反爬配置
DEFAULT_ANTI_CRAWLER_CONFIG = AntiCrawlerConfig(
    min_delay=1.0,
    max_delay=3.0,
    max_retries=3,
    retry_delay=2.0
)

# 严格的反爬配置（用于反爬较严的网站）
STRICT_ANTI_CRAWLER_CONFIG = AntiCrawlerConfig(
    min_delay=2.0,
    max_delay=5.0,
    max_retries=5,
    retry_delay=3.0,
    use_random_referer=True,
    referer_list=[
        'https://www.google.com/',
        'https://www.bing.com/',
        'https://www.yahoo.com/',
    ]
)

# 宽松的反爬配置（用于反爬较松的网站）
RELAXED_ANTI_CRAWLER_CONFIG = AntiCrawlerConfig(
    min_delay=0.5,
    max_delay=1.5,
    max_retries=2,
    retry_delay=1.0
)

ANTI_CRAWLER_CONFIGS = {
    # 需要严格反爬的网站
    'nytimes': STRICT_ANTI_CRAWLER_CONFIG,
    'wsj_chinese': STRICT_ANTI_CRAWLER_CONFIG,
    'ft': STRICT_ANTI_CRAWLER_CONFIG,
    
    # 默认配置
    'default': DEFAULT_ANTI_CRAWLER_CONFIG,
}


def get_anti_crawler_config(crawler_name: str) -> AntiCrawlerConfig:
    """
    获取指定爬虫的反爬配置
    
    Args:
        crawler_name: 爬虫名称
        
    Returns:
        AntiCrawlerConfig: 反爬配置
    """
    return ANTI_CRAWLER_CONFIGS.get(crawler_name, DEFAULT_ANTI_CRAWLER_CONFIG)
