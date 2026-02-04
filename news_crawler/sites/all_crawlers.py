"""
完整的爬虫注册中心
集成所有国际新闻网站爬虫
"""
from typing import Dict, List, Type
from news_crawler.core.base import BaseNewsCrawler as NewsCrawler

# 导入各批次爬虫
# 注意：batch2_crawlers 使用工厂函数模式，暂时不导入
# from news_crawler.sites.batch2_crawlers import ...

from news_crawler.sites.batch3_asian_crawlers import (
    # 韩国
    YonhapNewsCrawler, EpochtimesCrawler, CreadersCrawler, RenminbaoCrawler,
    # 马来西亚
    SinchewCrawler, GuangmingMalaysiaCrawler, IntimesCrawler, ChinapressCrawler,
    OrientaldailyMalaysiaCrawler, KwongwahCrawler, NanyangCrawler, OcdnCrawler,
    EunitedMalaysiaCrawler, TheStarMalaysiaCrawler,
    # 日本
    KyodoNewsCrawler, NHKNewsCrawler, Kyodo47NewsCrawler, RibenxinwenCrawler,
    NikkeiCNCrawler, NikkeiJPCrawler, JijiCrawler, AsahiCrawler,
    MainichiCrawler, SankeiCrawler, YomiuriCrawler, TokyoNPCrawler,
    NewsPostsevenCrawler, LivedoorNewsCrawler, GooNewsCrawler, YahooJapanNewsCrawler,
    SearchChinaCrawler, RecordChinaCrawler, FreeAsia2011Crawler, ChSakuraCrawler,
    GanbareNipponCrawler, Tiananmen1989Crawler, UyghurCongressJPCrawler,
    EastTurkistanGovCrawler, TibetanCommunityJPCrawler, SFTJapanCrawler,
    LUPMJapaneseCrawler, JapanTimesCrawler,
    # 新加坡
    ZaobaoCrawler, GuangmingSingaporeCrawler,
    # 新西兰
    KanzhongguoCrawler, AboluowangCrawler,
    # 印度
    HindustanTimesCrawler, TheHinduCrawler, IndianExpressCrawler,
    # 越南
    VietnamPlusCrawler, VOVWorldCrawler,
    # 缅甸
    DVBCrawler,
    # 朝鲜
    ChosenIlboCrawler,
)

from news_crawler.sites.batch4_western_crawlers import (
    # 美国
    VOACrawler, BBCChineseCrawler, ABCChineseCrawler, WSJChineseCrawler,
    WorldJournalCrawler, NYTimesChineseCrawler, NYTimesCrawler, IIPDigitalCrawler,
    LATimesCrawler, BloombergCrawler, RFIChineseCrawler, AssociatedPressCrawler,
    UPICrawler, CBSNewsCrawler, USATodayCrawler, AOLCrawler,
    TheDiplomatCrawler, OANNCrawler, EBLNewsCrawler, NewsyCrawler,
    RFACrawler, ChineseNewsNetCrawler, RightsCampaignCrawler, CanyuCrawler,
    WQWCrawler, PanChineseCrawler, NTDTVCrawler, NewCenturyNewsCrawler,
    MolihuaCrawler, MingjingNewsCrawler, ChinaAffairsCrawler, VOTCrawler,
    LiuyuanCrawler,
    # 英国
    ReutersChineseCrawler, TheTimesCrawler, FTChineseCrawler, FinancialTimesCrawler,
    TelegraphCrawler, DailyMailCrawler, GuardianCrawler, TheSunCrawler,
    # 法国
    AFPCrawler, LefigaroCrawler, LeMondeCrawler, LeParisienCrawler, LesEchosCrawler,
    # 德国
    DWChineseCrawler,
    # 俄罗斯
    EluosiCrawler, SputnikCrawler, RIANovostiCrawler, Channel1RUCrawler,
)

from news_crawler.sites.batch5_taiwan_hk_crawlers import (
    # 台湾
    LTNCrawler, AppleTaiwanCrawler, UDNCrawler, EDNCrawler,
    WantDailyCrawler, UDNEveningCrawler, EunitedTaiwanCrawler, ChinatimesCrawler,
    NownewsCrawler, ETtodayCrawler, IDNCrawler, NewtalkCrawler,
    TWGreatNewsCrawler, FreedomNewsTWCrawler, TWPowerNewsCrawler, StormMGCrawler,
    CNACrawler, UpmediaCrawler,
    # 香港
    TakungpaoCrawler, KKPCrawler, AppleHKCrawler, SingpaoCrawler,
    OrientaldailyHKCrawler, STHeadlineCrawler, WenweipoCrawler, HKCDCrawler,
    HKETCrawler, SCMPCrawler, MetroHKCrawler, HKHeadlineCrawler,
    AM730Crawler, SkypostCrawler, ChinaReviewNewsCrawler, HKETETICrawler,
    APDNewsCrawler, HK01Crawler, TheStandNewsCrawler, BastillePostCrawler,
    HKEJCrawler, NextDigitalCrawler,
    # 其他
    TibetanReviewCrawler,
)


# 爬虫注册表 - 按国家/地区分类
CRAWLER_REGISTRY: Dict[str, List[Type[NewsCrawler]]] = {
    # 注意：batch2中的爬虫使用工厂函数，暂未迁移到此处
    # 以下列出batch3、batch4、batch5中的所有爬虫（共145个）
    
    "阿塞拜疆": [
        # 将在后续版本中添加
    ],
    
    "爱尔兰": [
        # 将在后续版本中添加
    ],
    
    "澳大利亚": [
        # 将在后续版本中添加
    ],
    
    "澳门": [
        # 将在后续版本中添加
    ],
    
    "朝鲜": [
        ChosenIlboCrawler,     # 朝鲜日报
    ],
    
    "德国": [
        DWChineseCrawler,      # 德国之声
    ],
    
    "俄罗斯": [
        EluosiCrawler,         # 俄罗斯中文网
        SputnikCrawler,        # 俄罗斯卫星通讯社
        RIANovostiCrawler,     # 俄罗斯新闻社
        Channel1RUCrawler,     # 俄罗斯第一频道
    ],
    
    "法国": [
        AFPCrawler,            # 法新社
        LefigaroCrawler,       # 费加罗报
        LeMondeCrawler,        # 世界报
        LeParisienCrawler,     # 巴黎人报
        LesEchosCrawler,       # 回声报
    ],
    
    "韩国": [
        YonhapNewsCrawler,     # 韩联社
        EpochtimesCrawler,     # 大纪元
        CreadersCrawler,       # 万维读者网
        RenminbaoCrawler,      # 人民报
    ],
    
    "马来西亚": [
        SinchewCrawler,                # 星洲日报
        GuangmingMalaysiaCrawler,      # 光明日报
        IntimesCrawler,                # 国际时报
        ChinapressCrawler,             # 中国报
        OrientaldailyMalaysiaCrawler,  # 东方日报
        KwongwahCrawler,               # 光华日报
        NanyangCrawler,                # 南洋商报
        OcdnCrawler,                   # 华侨日报
        EunitedMalaysiaCrawler,        # 联合日报
        TheStarMalaysiaCrawler,        # The Star Online
    ],
    
    "美国": [
        VOACrawler,                # 美国之音
        BBCChineseCrawler,         # BBC中文网
        ABCChineseCrawler,         # ABC中文网
        WSJChineseCrawler,         # 华尔街日报中文网
        WorldJournalCrawler,       # 世界新闻网
        NYTimesChineseCrawler,     # 纽约时报中文网
        NYTimesCrawler,            # 纽约时报
        IIPDigitalCrawler,         # 美国参考
        LATimesCrawler,            # 洛杉矶时报
        BloombergCrawler,          # 彭博社
        RFIChineseCrawler,         # 法广中文网
        AssociatedPressCrawler,    # 美联社
        UPICrawler,                # 合众社
        CBSNewsCrawler,            # 哥伦比亚广播公司/60 Minutes
        USATodayCrawler,           # 今日美国
        AOLCrawler,                # 美国在线
        TheDiplomatCrawler,        # 外交家杂志
        OANNCrawler,               # 一个美国新闻网
        EBLNewsCrawler,            # EBL新闻
        NewsyCrawler,              # 新闻懒人包
        RFACrawler,                # 自由亚洲电台
        ChineseNewsNetCrawler,     # 多维新闻网
        RightsCampaignCrawler,     # 权利运动
        CanyuCrawler,              # 参与
        WQWCrawler,                # 维权网
        PanChineseCrawler,         # 泛华网
        NTDTVCrawler,              # 新唐人电视台
        NewCenturyNewsCrawler,     # 新世纪新闻网
        MolihuaCrawler,            # 中国茉莉花革命
        MingjingNewsCrawler,       # 明镜
        ChinaAffairsCrawler,       # 中国事务
        VOTCrawler,                # 西藏之声
        LiuyuanCrawler,            # 留园论坛
    ],
    
    "缅甸": [
        DVBCrawler,            # 缅甸民主之声
    ],
    
    "日本": [
        KyodoNewsCrawler,          # 共同社中文网
        NHKNewsCrawler,            # NHK新闻网
        Kyodo47NewsCrawler,        # 共同社日文网
        RibenxinwenCrawler,        # 日本新闻网
        NikkeiCNCrawler,           # 日经新闻中文版
        NikkeiJPCrawler,           # 日经新闻日文版
        JijiCrawler,               # 时事通讯社
        AsahiCrawler,              # 朝日新闻
        MainichiCrawler,           # 每日新闻
        SankeiCrawler,             # 产经新闻
        YomiuriCrawler,            # 读卖新闻
        TokyoNPCrawler,            # 东京新闻
        NewsPostsevenCrawler,      # news-postseven
        LivedoorNewsCrawler,       # livedoor
        GooNewsCrawler,            # goo
        YahooJapanNewsCrawler,     # 日本雅虎
        SearchChinaCrawler,        # searchChina
        RecordChinaCrawler,        # RecordChina
        FreeAsia2011Crawler,       # 亚洲自由民主连带协议会
        ChSakuraCrawler,           # 樱花频道
        GanbareNipponCrawler,      # 日本全国行动委员会
        Tiananmen1989Crawler,      # 天安门事件—天下围城
        UyghurCongressJPCrawler,   # 日维会
        EastTurkistanGovCrawler,   # 东突流亡政府
        TibetanCommunityJPCrawler, # 日本藏人社区
        SFTJapanCrawler,           # 日本自由西藏学生运动
        LUPMJapaneseCrawler,       # 日本蒙古自由联盟党
        JapanTimesCrawler,         # 日本时报
    ],
    
    "台湾": [
        LTNCrawler,                # 自由时报
        AppleTaiwanCrawler,        # 苹果日报（台湾）
        UDNCrawler,                # 联合报
        EDNCrawler,                # 经济日报
        WantDailyCrawler,          # 旺报
        UDNEveningCrawler,         # 联合晚报
        EunitedTaiwanCrawler,      # 联合日报
        ChinatimesCrawler,         # 中时电子报
        NownewsCrawler,            # 今日新闻网
        ETtodayCrawler,            # 东森新闻云
        IDNCrawler,                # 自立晚报
        NewtalkCrawler,            # 新头壳
        TWGreatNewsCrawler,        # 大成报
        FreedomNewsTWCrawler,      # 自由新闻报
        TWPowerNewsCrawler,        # 劲报
        StormMGCrawler,            # 风传媒
        CNACrawler,                # 中央社
        UpmediaCrawler,            # 上报
    ],
    
    "香港": [
        TakungpaoCrawler,          # 大公报
        KKPCrawler,                # 公教报
        AppleHKCrawler,            # 苹果日报
        SingpaoCrawler,            # 成报
        OrientaldailyHKCrawler,    # 东方日报
        STHeadlineCrawler,         # 星岛日报
        WenweipoCrawler,           # 文汇报
        HKCDCrawler,               # 香港商报
        HKETCrawler,               # 经济日报
        SCMPCrawler,               # 南华早报
        MetroHKCrawler,            # 都市日报
        HKHeadlineCrawler,         # 头条日报
        AM730Crawler,              # am730
        SkypostCrawler,            # 晴报
        ChinaReviewNewsCrawler,    # 中评社
        HKETETICrawler,            # 香港经济日报
        APDNewsCrawler,            # 亚太日报
        HK01Crawler,               # 香港01
        TheStandNewsCrawler,       # 立场新闻
        BastillePostCrawler,       # 巴士的报
        HKEJCrawler,               # 信报
        NextDigitalCrawler,        # 壹传媒
    ],
    
    "新加坡": [
        ZaobaoCrawler,             # 联合早报
        GuangmingSingaporeCrawler, # 光明日报
    ],
    
    "新西兰": [
        KanzhongguoCrawler,        # 看中国
        AboluowangCrawler,         # 阿波罗网
    ],
    
    "印度": [
        HindustanTimesCrawler,     # 印度斯坦时报
        TheHinduCrawler,           # 印度教徒报
        IndianExpressCrawler,      # 印度快报
    ],
    
    "英国": [
        ReutersChineseCrawler,     # 路透中文网
        TheTimesCrawler,           # 泰晤士报
        FTChineseCrawler,          # 金融时报中文网
        FinancialTimesCrawler,     # 金融时报
        TelegraphCrawler,          # 每日电讯
        DailyMailCrawler,          # 英国每日邮报
        GuardianCrawler,           # 卫报
        TheSunCrawler,             # 太阳报
    ],
    
    "越南": [
        VietnamPlusCrawler,        # 越南通讯社
        VOVWorldCrawler,           # 越南之声广播电台
    ],
    
    "其他": [
        TibetanReviewCrawler,      # 西藏评论
    ],
}


# 按名称索引的爬虫字典
CRAWLER_BY_NAME: Dict[str, Type[NewsCrawler]] = {}
for country, crawlers in CRAWLER_REGISTRY.items():
    for crawler_class in crawlers:
        CRAWLER_BY_NAME[crawler_class.name] = crawler_class


# 获取所有爬虫类
def get_all_crawlers() -> List[Type[NewsCrawler]]:
    """获取所有注册的爬虫类"""
    all_crawlers = []
    for crawlers in CRAWLER_REGISTRY.values():
        all_crawlers.extend(crawlers)
    return all_crawlers


# 根据国家获取爬虫
def get_crawlers_by_country(country: str) -> List[Type[NewsCrawler]]:
    """根据国家/地区获取爬虫列表"""
    return CRAWLER_REGISTRY.get(country, [])


# 根据名称获取爬虫
def get_crawler_by_name(name: str) -> Type[NewsCrawler]:
    """根据爬虫名称获取爬虫类"""
    return CRAWLER_BY_NAME.get(name)


# 获取所有支持的国家/地区列表
def get_supported_countries() -> List[str]:
    """获取所有支持的国家/地区列表"""
    return list(CRAWLER_REGISTRY.keys())


# 统计信息
def get_statistics() -> Dict[str, int]:
    """获取爬虫统计信息"""
    return {
        "total_crawlers": len(CRAWLER_BY_NAME),
        "total_countries": len(CRAWLER_REGISTRY),
        "crawlers_per_country": {
            country: len(crawlers) 
            for country, crawlers in CRAWLER_REGISTRY.items()
        }
    }


# 打印统计信息
if __name__ == "__main__":
    stats = get_statistics()
    print(f"总爬虫数: {stats['total_crawlers']}")
    print(f"覆盖国家/地区数: {stats['total_countries']}")
    print("\n各国家/地区爬虫数量:")
    for country, count in sorted(stats['crawlers_per_country'].items(), key=lambda x: x[1], reverse=True):
        print(f"  {country}: {count}")
