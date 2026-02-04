"""
台湾和香港地区新闻网站爬虫 - 批次5
"""
from typing import Optional, Dict, Any, List
from news_crawler.core.simple_crawler import SimpleNewsCrawler as NewsCrawler
from news_crawler.core.models import NewsMetaInfo, ContentItem
import logging

logger = logging.getLogger(__name__)


# ==================== 台湾新闻网站 ====================

class LTNCrawler(NewsCrawler):
    """台湾 - 自由时报"""
    name = "ltn"
    base_url = "http://www.ltn.com.tw"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class AppleTaiwanCrawler(NewsCrawler):
    """台湾 - 苹果日报（台湾）"""
    name = "apple_taiwan"
    base_url = "https://tw.appledaily.com"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class UDNCrawler(NewsCrawler):
    """台湾 - 联合报"""
    name = "udn"
    base_url = "http://udn.com"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class EDNCrawler(NewsCrawler):
    """台湾 - 经济日报"""
    name = "edn"
    base_url = "http://edn.udn.com"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class WantDailyCrawler(NewsCrawler):
    """台湾 - 旺报"""
    name = "want_daily"
    base_url = "http://www.want-daily.com"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class UDNEveningCrawler(NewsCrawler):
    """台湾 - 联合晚报"""
    name = "udn_evening"
    base_url = "http://reading.udn.com/reading/introduction_news.do"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class EunitedTaiwanCrawler(NewsCrawler):
    """台湾 - 联合日报"""
    name = "eunited_taiwan"
    base_url = "http://www.eunited.com.my/upaper"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class ChinatimesCrawler(NewsCrawler):
    """台湾 - 中时电子报"""
    name = "chinatimes"
    base_url = "http://www.chinatimes.com"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class NownewsCrawler(NewsCrawler):
    """台湾 - 今日新闻网"""
    name = "nownews"
    base_url = "http://www.nownews.com"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class ETtodayCrawler(NewsCrawler):
    """台湾 - 东森新闻云"""
    name = "ettoday"
    base_url = "http://www.ettoday.net"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class IDNCrawler(NewsCrawler):
    """台湾 - 自立晚报"""
    name = "idn"
    base_url = "http://www.idn.com.tw"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class NewtalkCrawler(NewsCrawler):
    """台湾 - 新头壳"""
    name = "newtalk"
    base_url = "http://www.newtalk.tw"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class TWGreatNewsCrawler(NewsCrawler):
    """台湾 - 大成报"""
    name = "twgreatnews"
    base_url = "http://www.twgreatnews.com"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class FreedomNewsTWCrawler(NewsCrawler):
    """台湾 - 自由新闻报"""
    name = "freedomnews_tw"
    base_url = "http://www.freedomnews.com.tw"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class TWPowerNewsCrawler(NewsCrawler):
    """台湾 - 劲报"""
    name = "twpowernews"
    base_url = "http://www.twpowernews.com"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class StormMGCrawler(NewsCrawler):
    """台湾 - 风传媒"""
    name = "storm"
    base_url = "https://www.storm.mg"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class CNACrawler(NewsCrawler):
    """台湾 - 中央社"""
    name = "cna"
    base_url = "http://www.cna.com.tw"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class UpmediaCrawler(NewsCrawler):
    """台湾 - 上报"""
    name = "upmedia"
    base_url = "http://www.upmedia.mg"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


# ==================== 香港新闻网站 ====================

class TakungpaoCrawler(NewsCrawler):
    """香港 - 大公报"""
    name = "takungpao"
    base_url = "http://www.takungpao.com"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class KKPCrawler(NewsCrawler):
    """香港 - 公教报"""
    name = "kkp"
    base_url = "http://kkp.org.hk"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class AppleHKCrawler(NewsCrawler):
    """香港 - 苹果日报"""
    name = "apple_hk"
    base_url = "https://hk.appledaily.com"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class SingpaoCrawler(NewsCrawler):
    """香港 - 成报"""
    name = "singpao"
    base_url = "http://www.singpao.com"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class OrientaldailyHKCrawler(NewsCrawler):
    """香港 - 东方日报"""
    name = "orientaldaily_hk"
    base_url = "http://orientaldaily.on.cc"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class STHeadlineCrawler(NewsCrawler):
    """香港 - 星岛日报"""
    name = "stheadline"
    base_url = "http://std.stheadline.com"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class WenweipoCrawler(NewsCrawler):
    """香港 - 文汇报"""
    name = "wenweipo"
    base_url = "http://www.wenweipo.com"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class HKCDCrawler(NewsCrawler):
    """香港 - 香港商报"""
    name = "hkcd"
    base_url = "http://www.hkcd.com.hk"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class HKETCrawler(NewsCrawler):
    """香港 - 经济日报"""
    name = "hket"
    base_url = "http://www.hket.com"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class SCMPCrawler(NewsCrawler):
    """香港 - 南华早报"""
    name = "scmp"
    base_url = "http://www.scmp.com"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class MetroHKCrawler(NewsCrawler):
    """香港 - 都市日报"""
    name = "metrohk"
    base_url = "http://www.metrohk.com.hk"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class HKHeadlineCrawler(NewsCrawler):
    """香港 - 头条日报"""
    name = "hkheadline"
    base_url = "http://www.hkheadline.com"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class AM730Crawler(NewsCrawler):
    """香港 - am730"""
    name = "am730"
    base_url = "http://www.am730.com.hk"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class SkypostCrawler(NewsCrawler):
    """香港 - 晴报"""
    name = "skypost"
    base_url = "http://www.skypost.hk"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class ChinaReviewNewsCrawler(NewsCrawler):
    """香港 - 中评社"""
    name = "chinareviewnews"
    base_url = "http://gb.chinareviewnews.com"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class HKETETICrawler(NewsCrawler):
    """香港 - 香港经济日报"""
    name = "hket_eti"
    base_url = "http://www.hket.com/eti"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class APDNewsCrawler(NewsCrawler):
    """香港 - 亚太日报"""
    name = "apdnews"
    base_url = "http://zh.apdnews.com"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class HK01Crawler(NewsCrawler):
    """香港 - 香港01"""
    name = "hk01"
    base_url = "https://www.hk01.com"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class TheStandNewsCrawler(NewsCrawler):
    """香港 - 立场新闻"""
    name = "thestandnews"
    base_url = "http://www.thestandnews.com"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class BastillePostCrawler(NewsCrawler):
    """香港 - 巴士的报"""
    name = "bastillepost"
    base_url = "https://www.bastillepost.com/hongkong"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class HKEJCrawler(NewsCrawler):
    """香港 - 信报"""
    name = "hkej"
    base_url = "https://www2.hkej.com"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class NextDigitalCrawler(NewsCrawler):
    """香港 - 壹传媒"""
    name = "nextdigital"
    base_url = "https://www.nextdigital.com.hk"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


# 其他
class TibetanReviewCrawler(NewsCrawler):
    """未知 - 西藏评论"""
    name = "tibetanreview"
    base_url = "http://www.tibetanreview.net"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


# 导出所有爬虫类
TAIWAN_HK_CRAWLERS = [
    # 台湾 (18个)
    LTNCrawler,
    AppleTaiwanCrawler,
    UDNCrawler,
    EDNCrawler,
    WantDailyCrawler,
    UDNEveningCrawler,
    EunitedTaiwanCrawler,
    ChinatimesCrawler,
    NownewsCrawler,
    ETtodayCrawler,
    IDNCrawler,
    NewtalkCrawler,
    TWGreatNewsCrawler,
    FreedomNewsTWCrawler,
    TWPowerNewsCrawler,
    StormMGCrawler,
    CNACrawler,
    UpmediaCrawler,
    
    # 香港 (23个)
    TakungpaoCrawler,
    KKPCrawler,
    AppleHKCrawler,
    SingpaoCrawler,
    OrientaldailyHKCrawler,
    STHeadlineCrawler,
    WenweipoCrawler,
    HKCDCrawler,
    HKETCrawler,
    SCMPCrawler,
    MetroHKCrawler,
    HKHeadlineCrawler,
    AM730Crawler,
    SkypostCrawler,
    ChinaReviewNewsCrawler,
    HKETETICrawler,
    APDNewsCrawler,
    HK01Crawler,
    TheStandNewsCrawler,
    BastillePostCrawler,
    HKEJCrawler,
    NextDigitalCrawler,
    
    # 其他 (1个)
    TibetanReviewCrawler,
]
