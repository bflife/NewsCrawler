"""
亚洲地区新闻网站爬虫 - 批次3
包括：韩国、马来西亚、日本、新加坡、印度、越南等
"""
from typing import Optional, Dict, Any, List
from news_crawler.core.base import BaseNewsCrawler as NewsCrawler
from news_crawler.core.models import NewsMetaInfo, ContentItem
import logging

logger = logging.getLogger(__name__)


class YonhapNewsCrawler(NewsCrawler):
    """韩国 - 韩联社中文网"""
    name = "yonhap_news"
    base_url = "https://cn.yna.co.kr"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class EpochtimesCrawler(NewsCrawler):
    """韩国 - 大纪元"""
    name = "epochtimes"
    base_url = "https://www.epochtimes.com"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class CreadersCrawler(NewsCrawler):
    """韩国 - 万维读者网"""
    name = "creaders"
    base_url = "http://news.creaders.net"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class RenminbaoCrawler(NewsCrawler):
    """韩国 - 人民报"""
    name = "renminbao"
    base_url = "http://renminbao.com"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class SinchewCrawler(NewsCrawler):
    """马来西亚 - 星洲日报"""
    name = "sinchew"
    base_url = "http://www.sinchew.com.my"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class GuangmingMalaysiaCrawler(NewsCrawler):
    """马来西亚 - 光明日报"""
    name = "guangming_malaysia"
    base_url = "http://www.guangming.com.my"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class IntimesCrawler(NewsCrawler):
    """马来西亚 - 国际时报"""
    name = "intimes"
    base_url = "http://www.intimes.com.my"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class ChinapressCrawler(NewsCrawler):
    """马来西亚 - 中国报"""
    name = "chinapress"
    base_url = "http://www.chinapress.com.my"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class OrientaldailyMalaysiaCrawler(NewsCrawler):
    """马来西亚 - 东方日报"""
    name = "orientaldaily_malaysia"
    base_url = "http://www.orientaldaily.com.my"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class KwongwahCrawler(NewsCrawler):
    """马来西亚 - 光华日报"""
    name = "kwongwah"
    base_url = "http://www.kwongwah.com.my"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class NanyangCrawler(NewsCrawler):
    """马来西亚 - 南洋商报"""
    name = "nanyang"
    base_url = "http://www.nanyang.com"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class OcdnCrawler(NewsCrawler):
    """马来西亚 - 华侨日报"""
    name = "ocdn"
    base_url = "http://www.ocdn.com.my"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class EunitedMalaysiaCrawler(NewsCrawler):
    """马来西亚 - 联合日报"""
    name = "eunited_malaysia"
    base_url = "http://www.eunited.com.my"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class TheStarMalaysiaCrawler(NewsCrawler):
    """马来西亚 - The Star Online"""
    name = "thestar_malaysia"
    base_url = "http://www.thestar.com.my"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class KyodoNewsCrawler(NewsCrawler):
    """日本 - 共同社中文网"""
    name = "kyodo_news"
    base_url = "https://china.kyodonews.net"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class NHKNewsCrawler(NewsCrawler):
    """日本 - NHK新闻网"""
    name = "nhk_news"
    base_url = "http://www3.nhk.or.jp/news"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class Kyodo47NewsCrawler(NewsCrawler):
    """日本 - 共同社日文网"""
    name = "kyodo_47news"
    base_url = "http://www.47news.jp"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class RibenxinwenCrawler(NewsCrawler):
    """日本 - 日本新闻网"""
    name = "ribenxinwen"
    base_url = "http://www.ribenxinwen.com"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class NikkeiCNCrawler(NewsCrawler):
    """日本 - 日经新闻中文版"""
    name = "nikkei_cn"
    base_url = "http://cn.nikkei.com"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class NikkeiJPCrawler(NewsCrawler):
    """日本 - 日经新闻日文版"""
    name = "nikkei_jp"
    base_url = "http://www.nikkei.com"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class JijiCrawler(NewsCrawler):
    """日本 - 时事通讯社"""
    name = "jiji"
    base_url = "http://www.jiji.com"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class AsahiCrawler(NewsCrawler):
    """日本 - 朝日新闻"""
    name = "asahi"
    base_url = "http://www.asahi.com"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class MainichiCrawler(NewsCrawler):
    """日本 - 每日新闻"""
    name = "mainichi"
    base_url = "http://mainichi.jp"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class SankeiCrawler(NewsCrawler):
    """日本 - 产经新闻"""
    name = "sankei"
    base_url = "http://www.sankei.com"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class YomiuriCrawler(NewsCrawler):
    """日本 - 读卖新闻"""
    name = "yomiuri"
    base_url = "http://www.yomiuri.co.jp"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class TokyoNPCrawler(NewsCrawler):
    """日本 - 东京新闻"""
    name = "tokyo_np"
    base_url = "http://www.tokyo-np.co.jp"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class NewsPostsevenCrawler(NewsCrawler):
    """日本 - news-postseven"""
    name = "news_postseven"
    base_url = "http://www.news-postseven.com"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class LivedoorNewsCrawler(NewsCrawler):
    """日本 - livedoor"""
    name = "livedoor_news"
    base_url = "http://news.livedoor.com"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class GooNewsCrawler(NewsCrawler):
    """日本 - goo"""
    name = "goo_news"
    base_url = "http://news.goo.ne.jp"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class YahooJapanNewsCrawler(NewsCrawler):
    """日本 - 日本雅虎"""
    name = "yahoo_japan_news"
    base_url = "http://news.yahoo.co.jp"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class SearchChinaCrawler(NewsCrawler):
    """日本 - searchChina"""
    name = "searchina"
    base_url = "http://news.searchina.net"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class RecordChinaCrawler(NewsCrawler):
    """日本 - RecordChina"""
    name = "recordchina"
    base_url = "http://www.recordchina.co.jp"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class FreeAsia2011Crawler(NewsCrawler):
    """日本 - 亚洲自由民主连带协议会"""
    name = "freeasia2011"
    base_url = "http://freeasia2011.org/japan"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class ChSakuraCrawler(NewsCrawler):
    """日本 - 樱花频道"""
    name = "ch_sakura"
    base_url = "http://www.ch-sakura.jp"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class GanbareNipponCrawler(NewsCrawler):
    """日本 - 日本全国行动委员会"""
    name = "ganbare_nippon"
    base_url = "http://www.ganbare-nippon.net"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class Tiananmen1989Crawler(NewsCrawler):
    """日本 - 天安门事件—天下围城"""
    name = "tiananmen1989"
    base_url = "http://www.tiananmen1989.net"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class UyghurCongressJPCrawler(NewsCrawler):
    """日本 - 日维会"""
    name = "uyghurcongress_jp"
    base_url = "http://www.uyghurcongress.org/jp"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class EastTurkistanGovCrawler(NewsCrawler):
    """日本 - 东突流亡政府"""
    name = "eastturkistan_gov"
    base_url = "http://eastturkistan-government.org"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class TibetanCommunityJPCrawler(NewsCrawler):
    """日本 - 日本藏人社区"""
    name = "tibetancommunity_jp"
    base_url = "http://www.tibetancommunity.jp"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class SFTJapanCrawler(NewsCrawler):
    """日本 - 日本自由西藏学生运动"""
    name = "sft_japan"
    base_url = "http://www.sftjapan.org"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class LUPMJapaneseCrawler(NewsCrawler):
    """日本 - 日本蒙古自由联盟党"""
    name = "lupm_japanese"
    base_url = "http://lupm.org/japanese2"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class JapanTimesCrawler(NewsCrawler):
    """日本 - 日本时报"""
    name = "japantimes"
    base_url = "http://www.japantimes.co.jp"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class ZaobaoCrawler(NewsCrawler):
    """新加坡 - 联合早报"""
    name = "zaobao"
    base_url = "http://www.zaobao.com.sg"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class GuangmingSingaporeCrawler(NewsCrawler):
    """新加坡 - 光明日报"""
    name = "guangming_singapore"
    base_url = "http://www.guangming.com.my"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class KanzhongguoCrawler(NewsCrawler):
    """新西兰 - 看中国"""
    name = "kanzhongguo"
    base_url = "http://www.kanzhongguo.com"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class AboluowangCrawler(NewsCrawler):
    """新西兰 - 阿波罗网"""
    name = "aboluowang"
    base_url = "http://www.aboluowang.com"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class HindustanTimesCrawler(NewsCrawler):
    """印度 - 印度斯坦时报"""
    name = "hindustan_times"
    base_url = "http://www.worldpress.org/newspapers/ASIA/India.cfm"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class TheHinduCrawler(NewsCrawler):
    """印度 - 印度教徒报"""
    name = "thehindu"
    base_url = "http://www.thehindu.com"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class IndianExpressCrawler(NewsCrawler):
    """印度 - 印度快报"""
    name = "indian_express"
    base_url = "http://indianexpress.com"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class VietnamPlusCrawler(NewsCrawler):
    """越南 - 越南通讯社"""
    name = "vietnamplus"
    base_url = "http://cn.vietnamplus.vn"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class VOVWorldCrawler(NewsCrawler):
    """越南 - 越南之声广播电台"""
    name = "vovworld"
    base_url = "http://vovworld.vn/zh-cn.vov"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class DVBCrawler(NewsCrawler):
    """缅甸 - 缅甸民主之声"""
    name = "dvb_burmese"
    base_url = "http://burmese.dvb.no"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


class ChosenIlboCrawler(NewsCrawler):
    """朝鲜 - 朝鲜日报"""
    name = "chosun"
    base_url = "http://chn.chosun.com"
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        html = await self.get_html(url)
        if not html:
            return None
        return self.parse_html_to_news_meta(html, url)


# 导出所有爬虫类
ASIAN_CRAWLERS = [
    # 韩国
    YonhapNewsCrawler,
    EpochtimesCrawler,
    CreadersCrawler,
    RenminbaoCrawler,
    
    # 马来西亚
    SinchewCrawler,
    GuangmingMalaysiaCrawler,
    IntimesCrawler,
    ChinapressCrawler,
    OrientaldailyMalaysiaCrawler,
    KwongwahCrawler,
    NanyangCrawler,
    OcdnCrawler,
    EunitedMalaysiaCrawler,
    TheStarMalaysiaCrawler,
    
    # 日本
    KyodoNewsCrawler,
    NHKNewsCrawler,
    Kyodo47NewsCrawler,
    RibenxinwenCrawler,
    NikkeiCNCrawler,
    NikkeiJPCrawler,
    JijiCrawler,
    AsahiCrawler,
    MainichiCrawler,
    SankeiCrawler,
    YomiuriCrawler,
    TokyoNPCrawler,
    NewsPostsevenCrawler,
    LivedoorNewsCrawler,
    GooNewsCrawler,
    YahooJapanNewsCrawler,
    SearchChinaCrawler,
    RecordChinaCrawler,
    FreeAsia2011Crawler,
    ChSakuraCrawler,
    GanbareNipponCrawler,
    Tiananmen1989Crawler,
    UyghurCongressJPCrawler,
    EastTurkistanGovCrawler,
    TibetanCommunityJPCrawler,
    SFTJapanCrawler,
    LUPMJapaneseCrawler,
    JapanTimesCrawler,
    
    # 新加坡
    ZaobaoCrawler,
    GuangmingSingaporeCrawler,
    
    # 新西兰
    KanzhongguoCrawler,
    AboluowangCrawler,
    
    # 印度
    HindustanTimesCrawler,
    TheHinduCrawler,
    IndianExpressCrawler,
    
    # 越南
    VietnamPlusCrawler,
    VOVWorldCrawler,
    
    # 缅甸
    DVBCrawler,
    
    # 朝鲜
    ChosenIlboCrawler,
]
