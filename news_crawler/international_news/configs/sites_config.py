"""
International News Websites Configuration

Organized by country/region with their major news websites.
"""

# News website configurations by country/region
NEWS_SITES_CONFIG = {
    "阿塞拜疆": [
        {"name": "倍可亲", "url": "http://news.backchina.com/rank.php", "encoding": "utf-8", "type": "ranking"},
        {"name": "博讯", "url": "http://www.boxun.com/", "encoding": "utf-8", "type": "portal"},
        {"name": "希望之声", "url": "http://www.soundofhope.org/", "encoding": "utf-8", "type": "portal"},
    ],
    "爱尔兰": [
        {"name": "开放杂志", "url": "http://www.open.com.hk/", "encoding": "utf-8", "type": "magazine"},
    ],
    "澳大利亚": [
        {"name": "澳大利亚广播公司", "url": "http://www.australiaplus.com/international/", "encoding": "utf-8", "type": "broadcast"},
        {"name": "澳洲日报", "url": "http://www.1688.com.au/site1/news/cn/index.shtml", "encoding": "utf-8", "type": "newspaper"},
        {"name": "每日电讯报", "url": "http://www.dailytelegraph.com.au/", "encoding": "utf-8", "type": "newspaper"},
    ],
    "澳门": [
        {"name": "力报", "url": "http://www.exmoo.com/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "正报", "url": "http://www.chengpou.com.mo/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "大众报", "url": "http://www.taichungdaily.com/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "华侨报", "url": "http://www.vakiodaily.com/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "新华濠报", "url": "http://www.waou.com.mo/main.htm", "encoding": "utf-8", "type": "newspaper"},
        {"name": "市民日报", "url": "http://www.shimindaily.net/v1/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "濠江日报", "url": "http://www.houkongdaily.com/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "澳门日报", "url": "http://www.macaodaily.com/html/2014-12/23/node_2.htm", "encoding": "utf-8", "type": "newspaper"},
        {"name": "现代澳门日报", "url": "http://www.todaymacao.com/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "澳门邮报", "url": "http://www.macaupostdaily.com/editiorial.php", "encoding": "utf-8", "type": "newspaper"},
        {"name": "澳门每日时报", "url": "http://www.macaudailytimes.com.mo/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "澳门商业日报", "url": "http://macaubusinessdaily.com/", "encoding": "utf-8", "type": "newspaper"},
    ],
    "朝鲜": [
        {"name": "朝鲜日报", "url": "http://chn.chosun.com/", "encoding": "utf-8", "type": "newspaper"},
    ],
    "德国": [
        {"name": "德国之声", "url": "http://www.dw.com/zh/", "encoding": "utf-8", "type": "broadcast"},
    ],
    "俄罗斯": [
        {"name": "俄罗斯中文网", "url": "http://eluosi.cn/", "encoding": "utf-8", "type": "portal"},
        {"name": "俄罗斯卫星通讯社", "url": "http://sputniknews.cn/", "encoding": "utf-8", "type": "news_agency"},
        {"name": "俄罗斯新闻社", "url": "https://ria.ru/", "encoding": "utf-8", "type": "news_agency"},
        {"name": "俄罗斯第一频道", "url": "http://www.1tv.ru/", "encoding": "utf-8", "type": "tv"},
    ],
    "法国": [
        {"name": "法新社", "url": "https://www.afp.com/en/home", "encoding": "utf-8", "type": "news_agency"},
        {"name": "费加罗报", "url": "https://www.lefigaro.fr/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "世界报", "url": "https://www.lemonde.fr/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "巴黎人报", "url": "http://www.leparisien.fr/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "回声报", "url": "https://www.lesechos.fr/", "encoding": "utf-8", "type": "newspaper"},
    ],
    "韩国": [
        {"name": "韩联社", "url": "http://chinese.yonhapnews.co.kr/", "encoding": "utf-8", "type": "news_agency"},
        {"name": "大纪元", "url": "http://www.epochtimes.com/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "万维读者网", "url": "http://news.creaders.net", "encoding": "utf-8", "type": "portal"},
        {"name": "人民报", "url": "http://renminbao.com/rmb/shishi/index.html", "encoding": "utf-8", "type": "newspaper"},
    ],
    "马来西亚": [
        {"name": "星洲日报", "url": "http://www.sinchew.com.my/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "光明日报", "url": "http://www.guangming.com.my/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "国际时报", "url": "http://www.intimes.com.my/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "中国报", "url": "http://www.chinapress.com.my/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "东方日报", "url": "http://www.orientaldaily.com.my/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "光华日报", "url": "http://www.kwongwah.com.my/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "南洋商报", "url": "http://www.nanyang.com/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "华侨日报", "url": "http://www.ocdn.com.my/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "联合日报", "url": "http://www.eunited.com.my/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "The Star Online", "url": "http://www.thestar.com.my/", "encoding": "utf-8", "type": "newspaper"},
    ],
    "美国": [
        {"name": "美国之音", "url": "http://www.voafanti.com/", "encoding": "utf-8", "type": "broadcast"},
        {"name": "BBC", "url": "http://www.bbc.co.uk/chinese/", "encoding": "utf-8", "type": "broadcast"},
        {"name": "ABC", "url": "https://www.abc.net.au/chinese/", "encoding": "utf-8", "type": "broadcast"},
        {"name": "华尔街日报", "url": "http://www.chinese.wsj.com/gb/index.asp", "encoding": "utf-8", "type": "newspaper"},
        {"name": "世界新闻网", "url": "http://www.worldjournal.com", "encoding": "utf-8", "type": "portal"},
        {"name": "纽约时报中文网", "url": "http://cn.nytimes.com/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "纽约时报", "url": "http://www.nytimes.com/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "洛杉矶时报", "url": "http://www.latimes.com/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "彭博社", "url": "http://www.bloomberg.com/", "encoding": "utf-8", "type": "news_agency"},
        {"name": "法广中文网", "url": "http://www.chinese.rfi.fr/", "encoding": "utf-8", "type": "broadcast"},
        {"name": "美联社", "url": "http://www.ap.org/", "encoding": "utf-8", "type": "news_agency"},
        {"name": "合众社", "url": "http://www.upi.com/", "encoding": "utf-8", "type": "news_agency"},
        {"name": "哥伦比亚广播公司", "url": "http://www.cbs.com/", "encoding": "utf-8", "type": "tv"},
        {"name": "今日美国", "url": "http://www.usatoday.com/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "美国在线", "url": "https://www.aol.com/", "encoding": "utf-8", "type": "portal"},
        {"name": "外交家杂志", "url": "https://thediplomat.com/", "encoding": "utf-8", "type": "magazine"},
        {"name": "CNN", "url": "https://www.cnn.com/", "encoding": "utf-8", "type": "tv"},
        {"name": "自由亚洲电台", "url": "http://www.rfa.org/mandarin", "encoding": "utf-8", "type": "radio"},
        {"name": "多维新闻网", "url": "http://www.chinesenewsnet.com/", "encoding": "utf-8", "type": "portal"},
        {"name": "新唐人电视台", "url": "http://www.ntdtv.com/xtr/gb/index.html", "encoding": "utf-8", "type": "tv"},
        {"name": "明镜", "url": "http://www.mingjingnews.com/", "encoding": "utf-8", "type": "magazine"},
        {"name": "留园论坛", "url": "http://site.6park.com/", "encoding": "utf-8", "type": "forum"},
    ],
    "缅甸": [
        {"name": "缅甸民主之声", "url": "http://burmese.dvb.no/", "encoding": "utf-8", "type": "radio"},
    ],
    "日本": [
        {"name": "共同社", "url": "https://china.kyodonews.net/", "encoding": "utf-8", "type": "news_agency"},
        {"name": "NHK新闻网", "url": "http://www3.nhk.or.jp/news", "encoding": "utf-8", "type": "tv"},
        {"name": "共同社中文网", "url": "https://china.kyodonews.jp/", "encoding": "utf-8", "type": "news_agency"},
        {"name": "共同社日文网", "url": "http://www.47news.jp/", "encoding": "utf-8", "type": "news_agency"},
        {"name": "日本新闻网", "url": "http://www.ribenxinwen.com", "encoding": "utf-8", "type": "portal"},
        {"name": "日经新闻中文版", "url": "http://cn.nikkei.com/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "日经新闻日文版", "url": "http://www.nikkei.com/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "时事通讯社", "url": "http://www.jiji.com/", "encoding": "utf-8", "type": "news_agency"},
        {"name": "朝日新闻", "url": "http://www.asahi.com/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "每日新闻", "url": "http://mainichi.jp/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "产经新闻", "url": "http://www.sankei.com/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "读卖新闻", "url": "http://www.yomiuri.co.jp/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "东京新闻", "url": "http://www.tokyo-np.co.jp/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "日本时报", "url": "http://www.japantimes.co.jp", "encoding": "utf-8", "type": "newspaper"},
    ],
    "台湾": [
        {"name": "自由时报", "url": "http://www.ltn.com.tw/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "苹果日报（台湾）", "url": "http://www.appledaily.com.tw/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "联合报", "url": "http://udn.com/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "经济日报", "url": "http://edn.udn.com/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "旺报", "url": "http://www.want-daily.com/portal.php", "encoding": "utf-8", "type": "newspaper"},
        {"name": "中时电子报", "url": "http://www.chinatimes.com/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "今日新闻网", "url": "http://www.nownews.com/", "encoding": "utf-8", "type": "portal"},
        {"name": "东森新闻云", "url": "http://www.ettoday.net/", "encoding": "utf-8", "type": "portal"},
        {"name": "自立晚报", "url": "http://www.idn.com.tw/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "新头壳", "url": "http://www.newtalk.tw/", "encoding": "utf-8", "type": "portal"},
        {"name": "风传媒", "url": "https://www.storm.mg/", "encoding": "utf-8", "type": "magazine"},
        {"name": "中央社", "url": "http://www.cna.com.tw/", "encoding": "utf-8", "type": "news_agency"},
        {"name": "上报", "url": "http://www.upmedia.mg/", "encoding": "utf-8", "type": "portal"},
    ],
    "香港": [
        {"name": "大公报", "url": "http://www.takungpao.com/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "公教报", "url": "http://kkp.org.hk/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "苹果日报", "url": "http://hk.apple.nextmedia.com/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "成报", "url": "http://www.singpao.com/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "东方日报", "url": "http://orientaldaily.on.cc/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "星岛日报", "url": "http://std.stheadline.com/index.html", "encoding": "utf-8", "type": "newspaper"},
        {"name": "文汇报", "url": "http://www.wenweipo.com/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "香港商报", "url": "http://www.hkcd.com.hk/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "经济日报", "url": "http://www.hket.com/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "南华早报", "url": "http://www.scmp.com/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "都市日报", "url": "http://www.metrohk.com.hk/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "头条日报", "url": "http://www.hkheadline.com/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "am730", "url": "http://www.am730.com.hk/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "晴报", "url": "http://www.skypost.hk/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "中评社", "url": "http://gb.chinareviewnews.com/", "encoding": "utf-8", "type": "news_agency"},
        {"name": "香港经济日报", "url": "http://www.hket.com/eti/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "亚太日报", "url": "http://zh.apdnews.com/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "香港01", "url": "https://www.hk01.com/", "encoding": "utf-8", "type": "portal"},
        {"name": "立场新闻", "url": "http://www.thestandnews.com/", "encoding": "utf-8", "type": "portal"},
        {"name": "巴士的报", "url": "https://www.bastillepost.com/hongkong/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "信报", "url": "https://www2.hkej.com/landing/index", "encoding": "utf-8", "type": "newspaper"},
    ],
    "新加坡": [
        {"name": "联合早报", "url": "http://www.zaobao.com.sg/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "光明日报", "url": "http://www.guangming.com.my/", "encoding": "utf-8", "type": "newspaper"},
    ],
    "新西兰": [
        {"name": "看中国", "url": "http://www.kanzhongguo.com/", "encoding": "utf-8", "type": "portal"},
        {"name": "阿波罗网", "url": "http://www.aboluowang.com/", "encoding": "utf-8", "type": "portal"},
    ],
    "印度": [
        {"name": "印度斯坦时报", "url": "http://www.hindustantimes.com/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "印度教徒报", "url": "http://www.thehindu.com/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "印度快报", "url": "http://indianexpress.com/", "encoding": "utf-8", "type": "newspaper"},
    ],
    "英国": [
        {"name": "路透中文网", "url": "http://cn.reuters.com/", "encoding": "utf-8", "type": "news_agency"},
        {"name": "泰晤士报", "url": "http://www.timesonline.co.uk/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "金融时报中文网", "url": "http://www.ftchinese.com/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "金融时报", "url": "http://www.ft.com/home/uk", "encoding": "utf-8", "type": "newspaper"},
        {"name": "每日电讯", "url": "http://www.telegraph.co.uk/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "英国每日邮报", "url": "http://www.dailymail.co.uk/ushome/index.html", "encoding": "utf-8", "type": "newspaper"},
        {"name": "卫报", "url": "http://www.guardiannews.com/", "encoding": "utf-8", "type": "newspaper"},
        {"name": "太阳报", "url": "https://www.thesun.co.uk/", "encoding": "utf-8", "type": "newspaper"},
    ],
    "越南": [
        {"name": "越南通讯社", "url": "http://cn.vietnamplus.vn/", "encoding": "utf-8", "type": "news_agency"},
        {"name": "越南之声广播电台", "url": "http://vovworld.vn/zh-cn.vov", "encoding": "utf-8", "type": "radio"},
    ],
}

# Region groupings for easier management
REGION_GROUPS = {
    "东亚": ["日本", "韩国", "朝鲜"],
    "东南亚": ["马来西亚", "新加坡", "越南", "缅甸"],
    "大中华": ["香港", "澳门", "台湾"],
    "欧洲": ["英国", "法国", "德国", "爱尔兰", "俄罗斯"],
    "北美": ["美国"],
    "大洋洲": ["澳大利亚", "新西兰"],
    "南亚": ["印度"],
    "其他": ["阿塞拜疆"],
}


def get_all_countries():
    """Get all countries"""
    return list(NEWS_SITES_CONFIG.keys())


def get_sites_by_country(country: str):
    """Get news sites by country"""
    return NEWS_SITES_CONFIG.get(country, [])


def get_sites_by_region(region: str):
    """Get all news sites in a region"""
    countries = REGION_GROUPS.get(region, [])
    sites = []
    for country in countries:
        sites.extend(get_sites_by_country(country))
    return sites


def get_all_sites():
    """Get all news sites"""
    sites = []
    for country_sites in NEWS_SITES_CONFIG.values():
        sites.extend(country_sites)
    return sites
