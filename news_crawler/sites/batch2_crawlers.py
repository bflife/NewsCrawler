"""
大规模新闻网站爬虫扩展 - 第二批
基于通用框架，添加更多全球新闻源
"""

from typing import Optional, Dict, Any, List
from news_crawler.core.base import BaseNewsCrawler
from news_crawler.core.models import NewsMetaInfo, Content
import logging

logger = logging.getLogger(__name__)

# 使用BaseNewsCrawler作为基类
class NewsCrawler(BaseNewsCrawler):
    """简化的爬虫基类（为批处理爬虫提供兼容性）"""
    pass


# ===== 阿塞拜疆新闻源 =====

def create_backchina_crawler():
    """倍可亲"""
    return SimpleListCrawler(
        source_id="backchina",
        source_name="倍可亲",
        base_url="http://news.backchina.com",
        list_url="http://news.backchina.com/rank.php",
        list_selector="div.list_content_1",
        title_selector="h2 a::text",
        link_selector="h2 a::attr(href)",
        article_title_selector="h1::text",
        article_content_selector="div.article_content p",
        article_time_selector="span.time::text",
        article_author_selector="span.author::text"
    )


def create_boxun_crawler():
    """博讯"""
    return SimpleListCrawler(
        source_id="boxun",
        source_name="博讯",
        base_url="http://www.boxun.com",
        list_url="http://www.boxun.com/",
        list_selector="div.news-item",
        title_selector="a::text",
        link_selector="a::attr(href)",
        article_title_selector="h1::text",
        article_content_selector="div.article p",
        article_time_selector="span.date::text",
        article_author_selector="span.source::text"
    )


def create_soundofhope_crawler():
    """希望之声"""
    return SimpleListCrawler(
        source_id="soundofhope",
        source_name="希望之声",
        base_url="http://www.soundofhope.org",
        list_url="http://www.soundofhope.org/",
        list_selector="div.post",
        title_selector="h3 a::text",
        link_selector="h3 a::attr(href)",
        article_title_selector="h1.entry-title::text",
        article_content_selector="div.entry-content p",
        article_time_selector="time::attr(datetime)",
        article_author_selector="span.author::text"
    )


# ===== 澳门新闻源 =====

def create_exmoo_crawler():
    """力报"""
    return SimpleListCrawler(
        source_id="exmoo",
        source_name="力报",
        base_url="http://www.exmoo.com",
        list_url="http://www.exmoo.com/",
        list_selector="div.news-list div.item",
        title_selector="h3 a::text",
        link_selector="h3 a::attr(href)",
        article_title_selector="h1.title::text",
        article_content_selector="div.content p",
        article_time_selector="span.time::text",
        article_author_selector="span.author::text"
    )


def create_macaodaily_crawler():
    """澳门日报"""
    return SimpleListCrawler(
        source_id="macaodaily",
        source_name="澳门日报",
        base_url="http://www.macaodaily.com",
        list_url="http://www.macaodaily.com/html/2014-12/23/node_2.htm",
        list_selector="div.news_list li",
        title_selector="a::text",
        link_selector="a::attr(href)",
        article_title_selector="h1::text",
        article_content_selector="div#ozoom p",
        article_time_selector="span.time::text",
        article_author_selector="span.source::text"
    )


# ===== 更多台湾新闻源 =====

def create_edn_crawler():
    """经济日报（台湾）"""
    return SimpleListCrawler(
        source_id="edn",
        source_name="经济日报",
        base_url="http://edn.udn.com",
        list_url="http://edn.udn.com/",
        list_selector="div.story-list__item",
        title_selector="h3::text",
        link_selector="a::attr(href)",
        article_title_selector="h1.article-content__title::text",
        article_content_selector="div.article-content__editor p",
        article_time_selector="time::text",
        article_author_selector="span.author::text"
    )


def create_wantdaily_crawler():
    """旺报"""
    return SimpleListCrawler(
        source_id="want_daily",
        source_name="旺报",
        base_url="http://www.want-daily.com",
        list_url="http://www.want-daily.com/portal.php",
        list_selector="div.article-list div.item",
        title_selector="h3 a::text",
        link_selector="h3 a::attr(href)",
        article_title_selector="h1.title::text",
        article_content_selector="div.content p",
        article_time_selector="span.time::text",
        article_author_selector="span.author::text"
    )


def create_ettoday_crawler():
    """东森新闻云"""
    return SimpleListCrawler(
        source_id="ettoday",
        source_name="东森新闻云",
        base_url="http://www.ettoday.net",
        list_url="http://www.ettoday.net/",
        list_selector="div.piece",
        title_selector="h3 a::text",
        link_selector="h3 a::attr(href)",
        article_title_selector="h1.title::text",
        article_content_selector="div.story p",
        article_time_selector="time::attr(datetime)",
        article_author_selector="span.writer::text"
    )


def create_newtalk_crawler():
    """新头壳"""
    return SimpleListCrawler(
        source_id="newtalk",
        source_name="新头壳",
        base_url="http://www.newtalk.tw",
        list_url="http://www.newtalk.tw/",
        list_selector="div.news_list div.item",
        title_selector="h3 a::text",
        link_selector="h3 a::attr(href)",
        article_title_selector="h1.title::text",
        article_content_selector="div.article_content p",
        article_time_selector="time::text",
        article_author_selector="span.author::text"
    )


def create_cna_crawler():
    """中央社"""
    return SimpleListCrawler(
        source_id="cna",
        source_name="中央社",
        base_url="http://www.cna.com.tw",
        list_url="http://www.cna.com.tw/",
        list_selector="div.mainList li",
        title_selector="h2 a::text",
        link_selector="h2 a::attr(href)",
        article_title_selector="h1.title::text",
        article_content_selector="div.article_content p",
        article_time_selector="time::attr(datetime)",
        article_author_selector="span.source::text"
    )


# ===== 更多香港新闻源 =====

def create_wenweipo_crawler():
    """文汇报"""
    return SimpleListCrawler(
        source_id="wenweipo",
        source_name="文汇报",
        base_url="http://www.wenweipo.com",
        list_url="http://www.wenweipo.com/",
        list_selector="div.news_list li",
        title_selector="a::text",
        link_selector="a::attr(href)",
        article_title_selector="h1::text",
        article_content_selector="div#artibody p",
        article_time_selector="span.time::text",
        article_author_selector="span.source::text"
    )


def create_stheadline_crawler():
    """星岛日报"""
    return SimpleListCrawler(
        source_id="stheadline",
        source_name="星岛日报",
        base_url="http://std.stheadline.com",
        list_url="http://std.stheadline.com/index.html",
        list_selector="div.news-item",
        title_selector="h3 a::text",
        link_selector="h3 a::attr(href)",
        article_title_selector="h1.article-title::text",
        article_content_selector="div.article-content p",
        article_time_selector="span.date::text",
        article_author_selector="span.author::text"
    )


def create_scmp_enhanced_crawler():
    """南华早报（增强版）"""
    return SimpleListCrawler(
        source_id="scmp",
        source_name="南华早报",
        base_url="http://www.scmp.com",
        list_url="http://www.scmp.com/",
        list_selector="div.card",
        title_selector="h2.card__headline a::text",
        link_selector="h2.card__headline a::attr(href)",
        article_title_selector="h1.article-headline::text",
        article_content_selector="div.article-body p",
        article_time_selector="time::attr(datetime)",
        article_author_selector="span.author::text"
    )


def create_hket_crawler():
    """香港经济日报"""
    return SimpleListCrawler(
        source_id="hket",
        source_name="香港经济日报",
        base_url="http://www.hket.com",
        list_url="http://www.hket.com/",
        list_selector="div.article-list div.item",
        title_selector="h3 a::text",
        link_selector="h3 a::attr(href)",
        article_title_selector="h1.title::text",
        article_content_selector="div.article-detail p",
        article_time_selector="time::text",
        article_author_selector="span.author::text"
    )


def create_thestandnews_crawler():
    """立场新闻"""
    return SimpleListCrawler(
        source_id="thestandnews",
        source_name="立场新闻",
        base_url="http://www.thestandnews.com",
        list_url="http://www.thestandnews.com/",
        list_selector="div.article-card",
        title_selector="h3 a::text",
        link_selector="h3 a::attr(href)",
        article_title_selector="h1.article-title::text",
        article_content_selector="div.article-content p",
        article_time_selector="time::attr(datetime)",
        article_author_selector="span.author::text"
    )


# ===== 更多日本新闻源 =====

def create_asahi_enhanced_crawler():
    """朝日新闻（增强版）"""
    return SimpleListCrawler(
        source_id="asahi",
        source_name="朝日新闻",
        base_url="http://www.asahi.com",
        list_url="http://www.asahi.com/news/",
        list_selector="div.List",
        title_selector="h3.Title a::text",
        link_selector="h3.Title a::attr(href)",
        article_title_selector="h1.Title::text",
        article_content_selector="div.ArticleText p",
        article_time_selector="time::attr(datetime)",
        article_author_selector="span.Author::text"
    )


def create_mainichi_crawler():
    """每日新闻"""
    return SimpleListCrawler(
        source_id="mainichi",
        source_name="每日新闻",
        base_url="http://mainichi.jp",
        list_url="http://mainichi.jp/",
        list_selector="div.articlelist li",
        title_selector="h3 a::text",
        link_selector="h3 a::attr(href)",
        article_title_selector="h1.title::text",
        article_content_selector="div.article p",
        article_time_selector="time::text",
        article_author_selector="span.writer::text"
    )


def create_yomiuri_crawler():
    """读卖新闻"""
    return SimpleListCrawler(
        source_id="yomiuri",
        source_name="读卖新闻",
        base_url="http://www.yomiuri.co.jp",
        list_url="http://www.yomiuri.co.jp/",
        list_selector="div.list-items li",
        title_selector="h3 a::text",
        link_selector="h3 a::attr(href)",
        article_title_selector="h1.title::text",
        article_content_selector="div.article-body p",
        article_time_selector="time::text",
        article_author_selector="span.author::text"
    )


def create_sankei_crawler():
    """产经新闻"""
    return SimpleListCrawler(
        source_id="sankei",
        source_name="产经新闻",
        base_url="http://www.sankei.com",
        list_url="http://www.sankei.com/",
        list_selector="div.story",
        title_selector="h3 a::text",
        link_selector="h3 a::attr(href)",
        article_title_selector="h1.title::text",
        article_content_selector="div.article-body p",
        article_time_selector="time::text",
        article_author_selector="span.byline::text"
    )


def create_tokyonp_crawler():
    """东京新闻"""
    return SimpleListCrawler(
        source_id="tokyo_np",
        source_name="东京新闻",
        base_url="http://www.tokyo-np.co.jp",
        list_url="http://www.tokyo-np.co.jp/",
        list_selector="div.newslist li",
        title_selector="a::text",
        link_selector="a::attr(href)",
        article_title_selector="h1::text",
        article_content_selector="div.article p",
        article_time_selector="span.date::text",
        article_author_selector="span.author::text"
    )


def create_japantimes_crawler():
    """日本时报"""
    return SimpleListCrawler(
        source_id="japantimes",
        source_name="日本时报",
        base_url="http://www.japantimes.co.jp",
        list_url="http://www.japantimes.co.jp/",
        list_selector="div.article-card",
        title_selector="h3 a::text",
        link_selector="h3 a::attr(href)",
        article_title_selector="h1.entry-title::text",
        article_content_selector="div.entry-content p",
        article_time_selector="time::attr(datetime)",
        article_author_selector="span.author::text"
    )


# ===== 德国新闻源 =====

def create_dw_crawler():
    """德国之声"""
    return SimpleListCrawler(
        source_id="dw",
        source_name="德国之声",
        base_url="http://www.dw.com",
        list_url="http://www.dw.com/zh/",
        list_selector="div.news",
        title_selector="h2 a::text",
        link_selector="h2 a::attr(href)",
        article_title_selector="h1::text",
        article_content_selector="div.longText p",
        article_time_selector="time::attr(datetime)",
        article_author_selector="span.author::text"
    )


# ===== 法国新闻源 =====

def create_afp_crawler():
    """法新社"""
    return SimpleListCrawler(
        source_id="afp",
        source_name="法新社",
        base_url="https://www.afp.com",
        list_url="https://www.afp.com/en/home",
        list_selector="div.card-article",
        title_selector="h3.card-title a::text",
        link_selector="h3.card-title a::attr(href)",
        article_title_selector="h1.article-title::text",
        article_content_selector="div.article-content p",
        article_time_selector="time::attr(datetime)",
        article_author_selector="span.author::text"
    )


def create_lefigaro_crawler():
    """费加罗报"""
    return SimpleListCrawler(
        source_id="lefigaro",
        source_name="费加罗报",
        base_url="https://www.lefigaro.fr",
        list_url="https://www.lefigaro.fr/",
        list_selector="article.fig-profile",
        title_selector="h2 a::text",
        link_selector="h2 a::attr(href)",
        article_title_selector="h1.fig-headline::text",
        article_content_selector="div.fig-content-body p",
        article_time_selector="time::attr(datetime)",
        article_author_selector="span.fig-content-author::text"
    )


def create_lemonde_crawler():
    """世界报"""
    return SimpleListCrawler(
        source_id="lemonde",
        source_name="世界报",
        base_url="https://www.lemonde.fr",
        list_url="https://www.lemonde.fr/",
        list_selector="div.teaser",
        title_selector="h3 a::text",
        link_selector="h3 a::attr(href)",
        article_title_selector="h1.article__title::text",
        article_content_selector="div.article__content p",
        article_time_selector="time::attr(datetime)",
        article_author_selector="span.author::text"
    )


# ===== 俄罗斯新闻源 =====

def create_eluosi_crawler():
    """俄罗斯中文网"""
    return SimpleListCrawler(
        source_id="eluosi",
        source_name="俄罗斯中文网",
        base_url="http://eluosi.cn",
        list_url="http://eluosi.cn/",
        list_selector="div.news-list div.item",
        title_selector="h3 a::text",
        link_selector="h3 a::attr(href)",
        article_title_selector="h1.title::text",
        article_content_selector="div.content p",
        article_time_selector="span.time::text",
        article_author_selector="span.author::text"
    )


def create_sputniknews_crawler():
    """俄罗斯卫星通讯社"""
    return SimpleListCrawler(
        source_id="sputniknews",
        source_name="俄罗斯卫星通讯社",
        base_url="http://sputniknews.cn",
        list_url="http://sputniknews.cn/",
        list_selector="div.list__item",
        title_selector="a.list__title::text",
        link_selector="a.list__title::attr(href)",
        article_title_selector="h1.article__title::text",
        article_content_selector="div.article__body p",
        article_time_selector="time::attr(datetime)",
        article_author_selector="span.article__author::text"
    )


# ===== 更多美国新闻源 =====

def create_latimes_crawler():
    """洛杉矶时报"""
    return SimpleListCrawler(
        source_id="latimes",
        source_name="洛杉矶时报",
        base_url="http://www.latimes.com",
        list_url="http://www.latimes.com/",
        list_selector="div.promo-wrapper",
        title_selector="h3.promo-title a::text",
        link_selector="h3.promo-title a::attr(href)",
        article_title_selector="h1.headline::text",
        article_content_selector="div.rich-text-body p",
        article_time_selector="time::attr(datetime)",
        article_author_selector="span.author-name::text"
    )


def create_bloomberg_crawler():
    """彭博社"""
    return SimpleListCrawler(
        source_id="bloomberg",
        source_name="彭博社",
        base_url="http://www.bloomberg.com",
        list_url="http://www.bloomberg.com/",
        list_selector="div.story-package-module__story",
        title_selector="a.story-package-module__story-link::text",
        link_selector="a.story-package-module__story-link::attr(href)",
        article_title_selector="h1.headline::text",
        article_content_selector="div.body-copy p",
        article_time_selector="time::attr(datetime)",
        article_author_selector="span.author::text"
    )


def create_ap_crawler():
    """美联社"""
    return SimpleListCrawler(
        source_id="ap",
        source_name="美联社",
        base_url="http://www.ap.org",
        list_url="http://www.ap.org/",
        list_selector="div.FeedCard",
        title_selector="h3.headline a::text",
        link_selector="h3.headline a::attr(href)",
        article_title_selector="h1.headline::text",
        article_content_selector="div.Article p",
        article_time_selector="time::attr(datetime)",
        article_author_selector="span.byline::text"
    )


def create_usatoday_crawler():
    """今日美国"""
    return SimpleListCrawler(
        source_id="usatoday",
        source_name="今日美国",
        base_url="http://www.usatoday.com",
        list_url="http://www.usatoday.com/",
        list_selector="div.gnt_m_flm_a",
        title_selector="a.gnt_m_flm_a_h::text",
        link_selector="a.gnt_m_flm_a_h::attr(href)",
        article_title_selector="h1.gnt_ar_hl::text",
        article_content_selector="div.gnt_ar_b p",
        article_time_selector="time::attr(datetime)",
        article_author_selector="span.gnt_ar_by::text"
    )


def create_worldjournal_crawler():
    """世界新闻网"""
    return SimpleListCrawler(
        source_id="worldjournal",
        source_name="世界新闻网",
        base_url="http://www.worldjournal.com",
        list_url="http://www.worldjournal.com",
        list_selector="div.article-list div.item",
        title_selector="h3 a::text",
        link_selector="h3 a::attr(href)",
        article_title_selector="h1.article-title::text",
        article_content_selector="div.article-content p",
        article_time_selector="time::text",
        article_author_selector="span.author::text"
    )


# ===== 更多马来西亚新闻源 =====

def create_guangming_my_crawler():
    """光明日报（马来西亚）"""
    return SimpleListCrawler(
        source_id="guangming_my",
        source_name="光明日报",
        base_url="http://www.guangming.com.my",
        list_url="http://www.guangming.com.my/",
        list_selector="div.news-list div.item",
        title_selector="h3 a::text",
        link_selector="h3 a::attr(href)",
        article_title_selector="h1.title::text",
        article_content_selector="div.content p",
        article_time_selector="span.time::text",
        article_author_selector="span.author::text"
    )


def create_nanyang_crawler():
    """南洋商报"""
    return SimpleListCrawler(
        source_id="nanyang",
        source_name="南洋商报",
        base_url="http://www.nanyang.com",
        list_url="http://www.nanyang.com/",
        list_selector="div.article-list div.item",
        title_selector="h3 a::text",
        link_selector="h3 a::attr(href)",
        article_title_selector="h1.title::text",
        article_content_selector="div.article-body p",
        article_time_selector="time::text",
        article_author_selector="span.author::text"
    )


def create_kwongwah_crawler():
    """光华日报"""
    return SimpleListCrawler(
        source_id="kwongwah",
        source_name="光华日报",
        base_url="http://www.kwongwah.com.my",
        list_url="http://www.kwongwah.com.my/",
        list_selector="div.news-item",
        title_selector="h3 a::text",
        link_selector="h3 a::attr(href)",
        article_title_selector="h1.article-title::text",
        article_content_selector="div.article-content p",
        article_time_selector="span.date::text",
        article_author_selector="span.author::text"
    )


def create_thestar_my_crawler():
    """The Star Online"""
    return SimpleListCrawler(
        source_id="thestar_my",
        source_name="The Star Online",
        base_url="http://www.thestar.com.my",
        list_url="http://www.thestar.com.my/",
        list_selector="div.story",
        title_selector="h2 a::text",
        link_selector="h2 a::attr(href)",
        article_title_selector="h1.headline::text",
        article_content_selector="div.story-body p",
        article_time_selector="time::attr(datetime)",
        article_author_selector="span.author::text"
    )


# ===== 新西兰新闻源 =====

def create_kanzhongguo_crawler():
    """看中国"""
    return SimpleListCrawler(
        source_id="kanzhongguo",
        source_name="看中国",
        base_url="http://www.kanzhongguo.com",
        list_url="http://www.kanzhongguo.com/",
        list_selector="div.article-list div.item",
        title_selector="h3 a::text",
        link_selector="h3 a::attr(href)",
        article_title_selector="h1.title::text",
        article_content_selector="div.article-content p",
        article_time_selector="span.time::text",
        article_author_selector="span.author::text"
    )


def create_aboluowang_crawler():
    """阿波罗网"""
    return SimpleListCrawler(
        source_id="aboluowang",
        source_name="阿波罗网",
        base_url="http://www.aboluowang.com",
        list_url="http://www.aboluowang.com/",
        list_selector="div.news-list div.item",
        title_selector="h3 a::text",
        link_selector="h3 a::attr(href)",
        article_title_selector="h1.article-title::text",
        article_content_selector="div.article-body p",
        article_time_selector="span.date::text",
        article_author_selector="span.source::text"
    )


# ===== 印度新闻源 =====

def create_thehindu_crawler():
    """印度教徒报"""
    return SimpleListCrawler(
        source_id="thehindu",
        source_name="印度教徒报",
        base_url="http://www.thehindu.com",
        list_url="http://www.thehindu.com/",
        list_selector="div.story-card",
        title_selector="h3 a::text",
        link_selector="h3 a::attr(href)",
        article_title_selector="h1.title::text",
        article_content_selector="div.article-body p",
        article_time_selector="time::attr(datetime)",
        article_author_selector="span.author::text"
    )


def create_indianexpress_crawler():
    """印度快报"""
    return SimpleListCrawler(
        source_id="indianexpress",
        source_name="印度快报",
        base_url="http://indianexpress.com",
        list_url="http://indianexpress.com/",
        list_selector="div.articles",
        title_selector="h3 a::text",
        link_selector="h3 a::attr(href)",
        article_title_selector="h1.heading-part::text",
        article_content_selector="div.full-details p",
        article_time_selector="time::attr(datetime)",
        article_author_selector="span.editor::text"
    )


# ===== 越南新闻源 =====

def create_vietnamplus_crawler():
    """越南通讯社"""
    return SimpleListCrawler(
        source_id="vietnamplus",
        source_name="越南通讯社",
        base_url="http://cn.vietnamplus.vn",
        list_url="http://cn.vietnamplus.vn/",
        list_selector="div.article-item",
        title_selector="h3 a::text",
        link_selector="h3 a::attr(href)",
        article_title_selector="h1.article-title::text",
        article_content_selector="div.article-content p",
        article_time_selector="time::text",
        article_author_selector="span.author::text"
    )


def create_vovworld_crawler():
    """越南之声广播电台"""
    return SimpleListCrawler(
        source_id="vovworld",
        source_name="越南之声广播电台",
        base_url="http://vovworld.vn",
        list_url="http://vovworld.vn/zh-cn.vov",
        list_selector="div.news-item",
        title_selector="h3 a::text",
        link_selector="h3 a::attr(href)",
        article_title_selector="h1.title::text",
        article_content_selector="div.content-detail p",
        article_time_selector="span.time::text",
        article_author_selector="span.author::text"
    )


# ===== 更多韩国新闻源 =====

def create_epochtimes_crawler():
    """大纪元"""
    return SimpleListCrawler(
        source_id="epochtimes",
        source_name="大纪元",
        base_url="http://www.epochtimes.com",
        list_url="http://www.epochtimes.com/",
        list_selector="div.article-list div.item",
        title_selector="h3 a::text",
        link_selector="h3 a::attr(href)",
        article_title_selector="h1#artitle::text",
        article_content_selector="div#artbody p",
        article_time_selector="time::text",
        article_author_selector="span.author::text"
    )


def create_creaders_crawler():
    """万维读者网"""
    return SimpleListCrawler(
        source_id="creaders",
        source_name="万维读者网",
        base_url="http://news.creaders.net",
        list_url="http://news.creaders.net",
        list_selector="div.news-list div.item",
        title_selector="h3 a::text",
        link_selector="h3 a::attr(href)",
        article_title_selector="h1.title::text",
        article_content_selector="div.content p",
        article_time_selector="span.time::text",
        article_author_selector="span.source::text"
    )


# ===== 澳大利亚新闻源 =====

def create_abc_au_crawler():
    """澳大利亚广播公司"""
    return SimpleListCrawler(
        source_id="abc_au",
        source_name="澳大利亚广播公司",
        base_url="http://www.australiaplus.com",
        list_url="http://www.australiaplus.com/international/",
        list_selector="div.article-card",
        title_selector="h3 a::text",
        link_selector="h3 a::attr(href)",
        article_title_selector="h1.article-title::text",
        article_content_selector="div.article-body p",
        article_time_selector="time::attr(datetime)",
        article_author_selector="span.author::text"
    )


# ===== 更新爬虫工厂字典 =====

BATCH2_CRAWLER_FACTORIES = {
    # 阿塞拜疆 (3个)
    'backchina': create_backchina_crawler,
    'boxun': create_boxun_crawler,
    'soundofhope': create_soundofhope_crawler,
    
    # 澳门 (2个)
    'exmoo': create_exmoo_crawler,
    'macaodaily': create_macaodaily_crawler,
    
    # 台湾 (5个)
    'edn': create_edn_crawler,
    'want_daily': create_wantdaily_crawler,
    'ettoday': create_ettoday_crawler,
    'newtalk': create_newtalk_crawler,
    'cna': create_cna_crawler,
    
    # 香港 (5个)
    'wenweipo': create_wenweipo_crawler,
    'stheadline': create_stheadline_crawler,
    'scmp': create_scmp_enhanced_crawler,
    'hket': create_hket_crawler,
    'thestandnews': create_thestandnews_crawler,
    
    # 日本 (6个)
    'asahi': create_asahi_enhanced_crawler,
    'mainichi': create_mainichi_crawler,
    'yomiuri': create_yomiuri_crawler,
    'sankei': create_sankei_crawler,
    'tokyo_np': create_tokyonp_crawler,
    'japantimes': create_japantimes_crawler,
    
    # 德国 (1个)
    'dw': create_dw_crawler,
    
    # 法国 (3个)
    'afp': create_afp_crawler,
    'lefigaro': create_lefigaro_crawler,
    'lemonde': create_lemonde_crawler,
    
    # 俄罗斯 (2个)
    'eluosi': create_eluosi_crawler,
    'sputniknews': create_sputniknews_crawler,
    
    # 美国 (5个)
    'latimes': create_latimes_crawler,
    'bloomberg': create_bloomberg_crawler,
    'ap': create_ap_crawler,
    'usatoday': create_usatoday_crawler,
    'worldjournal': create_worldjournal_crawler,
    
    # 马来西亚 (4个)
    'guangming_my': create_guangming_my_crawler,
    'nanyang': create_nanyang_crawler,
    'kwongwah': create_kwongwah_crawler,
    'thestar_my': create_thestar_my_crawler,
    
    # 新西兰 (2个)
    'kanzhongguo': create_kanzhongguo_crawler,
    'aboluowang': create_aboluowang_crawler,
    
    # 印度 (2个)
    'thehindu': create_thehindu_crawler,
    'indianexpress': create_indianexpress_crawler,
    
    # 越南 (2个)
    'vietnamplus': create_vietnamplus_crawler,
    'vovworld': create_vovworld_crawler,
    
    # 韩国 (2个)
    'epochtimes': create_epochtimes_crawler,
    'creaders': create_creaders_crawler,
    
    # 澳大利亚 (1个)
    'abc_au': create_abc_au_crawler,
}


def get_batch2_crawler(source_id: str):
    """获取第二批爬虫"""
    factory = BATCH2_CRAWLER_FACTORIES.get(source_id)
    if factory:
        return factory()
    return None


def register_batch2_crawlers(scheduler):
    """注册第二批所有爬虫"""
    for source_id, factory in BATCH2_CRAWLER_FACTORIES.items():
        crawler = factory()
        scheduler.register_crawler(source_id, crawler)
    print(f"已注册第二批 {len(BATCH2_CRAWLER_FACTORIES)} 个爬虫")
