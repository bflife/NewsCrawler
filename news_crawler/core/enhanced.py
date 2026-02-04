"""
增强型爬虫基类 - 支持选择器配置和反爬机制
"""
from typing import Optional, Dict, Any, List, Union
from dataclasses import dataclass, field
import random
import time
import hashlib
from urllib.parse import urlparse
from bs4 import BeautifulSoup

from news_crawler.core.base import BaseNewsCrawler
from news_crawler.core.models import NewsItem, NewsMetaInfo, ContentItem, ContentType


@dataclass
class SelectorConfig:
    """选择器配置"""
    # 列表页选择器
    list_container: Optional[str] = None      # 文章列表容器
    list_item: Optional[str] = None           # 单个文章项
    list_title: Optional[str] = None          # 标题选择器
    list_link: Optional[str] = None           # 链接选择器
    list_date: Optional[str] = None           # 日期选择器
    list_summary: Optional[str] = None        # 摘要选择器
    
    # 文章页选择器
    article_title: Optional[str] = None       # 文章标题
    article_subtitle: Optional[str] = None    # 副标题
    article_content: Optional[str] = None     # 正文内容容器
    article_author: Optional[str] = None      # 作者
    article_date: Optional[str] = None        # 发布时间
    article_source: Optional[str] = None      # 来源
    article_tags: Optional[str] = None        # 标签
    article_images: Optional[str] = None      # 图片
    article_videos: Optional[str] = None      # 视频
    
    # 移除选择器（需要删除的元素）
    remove_selectors: List[str] = field(default_factory=list)
    
    # 自定义提取规则
    custom_extractors: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AntiCrawlerConfig:
    """反爬配置"""
    # User-Agent 池
    user_agents: List[str] = field(default_factory=lambda: [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
    ])
    
    # 请求延迟 (秒)
    min_delay: float = 1.0
    max_delay: float = 3.0
    
    # 重试配置
    max_retries: int = 3
    retry_delay: float = 2.0
    
    # 代理配置
    use_proxy: bool = False
    proxy_list: List[str] = field(default_factory=list)
    
    # Cookie 配置
    cookies: Optional[Dict[str, str]] = None
    
    # Referer 配置
    use_random_referer: bool = False
    referer_list: List[str] = field(default_factory=list)


class EnhancedNewsCrawler(BaseNewsCrawler):
    """
    增强型新闻爬虫基类
    支持选择器配置和反爬机制
    """
    
    # 子类需要配置的属性
    name: str = "enhanced_crawler"
    base_url: str = ""
    selector_config: Optional[SelectorConfig] = None
    anti_crawler_config: Optional[AntiCrawlerConfig] = None
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 初始化配置
        if self.selector_config is None:
            self.selector_config = SelectorConfig()
        if self.anti_crawler_config is None:
            self.anti_crawler_config = AntiCrawlerConfig()
        
        # 应用反爬配置
        self._apply_anti_crawler_config()
    
    def _apply_anti_crawler_config(self):
        """应用反爬配置到headers"""
        config = self.anti_crawler_config
        
        # 随机 User-Agent
        if config.user_agents:
            self.headers['User-Agent'] = random.choice(config.user_agents)
        
        # 随机 Referer
        if config.use_random_referer and config.referer_list:
            self.headers['Referer'] = random.choice(config.referer_list)
        
        # Cookies
        if config.cookies:
            cookie_str = '; '.join([f"{k}={v}" for k, v in config.cookies.items()])
            self.headers['Cookie'] = cookie_str
    
    def _random_delay(self):
        """随机延迟"""
        config = self.anti_crawler_config
        delay = random.uniform(config.min_delay, config.max_delay)
        time.sleep(delay)
    
    def fetch_content(self) -> str:
        """重写fetch_content，添加延迟"""
        self._random_delay()
        return super().fetch_content()
    
    def parse_content(self, html: str) -> NewsItem:
        """解析HTML内容"""
        soup = BeautifulSoup(html, 'lxml')
        
        # 移除不需要的元素
        self._remove_unwanted_elements(soup)
        
        # 提取文章信息
        title = self._extract_title(soup)
        subtitle = self._extract_subtitle(soup)
        author = self._extract_author(soup)
        date = self._extract_date(soup)
        source = self._extract_source(soup)
        tags = self._extract_tags(soup)
        
        # 提取内容
        contents = self._extract_contents(soup)
        
        # 构建 meta_info
        meta_info = NewsMetaInfo(
            author_name=author,
            publish_time=date,
            source=source,
            tags=tags or []
        )
        
        # 构建 NewsItem
        news_item = self.compose_news_item(
            title=title,
            subtitle=subtitle,
            meta_info=meta_info,
            contents=contents,
            news_id=self.get_article_id()
        )
        
        return news_item
    
    def _remove_unwanted_elements(self, soup: BeautifulSoup):
        """移除不需要的元素"""
        for selector in self.selector_config.remove_selectors:
            for elem in soup.select(selector):
                elem.decompose()
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """提取标题"""
        if self.selector_config.article_title:
            elem = soup.select_one(self.selector_config.article_title)
            if elem:
                return elem.get_text(strip=True)
        
        # 默认尝试常见选择器
        for selector in ['h1.title', 'h1', '.article-title', '#article-title']:
            elem = soup.select_one(selector)
            if elem:
                return elem.get_text(strip=True)
        
        return "Untitled"
    
    def _extract_subtitle(self, soup: BeautifulSoup) -> Optional[str]:
        """提取副标题"""
        if self.selector_config.article_subtitle:
            elem = soup.select_one(self.selector_config.article_subtitle)
            if elem:
                return elem.get_text(strip=True)
        return None
    
    def _extract_author(self, soup: BeautifulSoup) -> Optional[str]:
        """提取作者"""
        if self.selector_config.article_author:
            elem = soup.select_one(self.selector_config.article_author)
            if elem:
                return elem.get_text(strip=True)
        
        # 尝试常见选择器
        for selector in ['.author', '.byline', '[itemprop="author"]', '.article-author']:
            elem = soup.select_one(selector)
            if elem:
                return elem.get_text(strip=True)
        
        return None
    
    def _extract_date(self, soup: BeautifulSoup) -> Optional[str]:
        """提取发布时间"""
        if self.selector_config.article_date:
            elem = soup.select_one(self.selector_config.article_date)
            if elem:
                # 尝试从 datetime 属性获取
                if elem.get('datetime'):
                    return elem.get('datetime')
                return elem.get_text(strip=True)
        
        # 尝试常见选择器
        for selector in ['time', '.publish-time', '.date', '[itemprop="datePublished"]']:
            elem = soup.select_one(selector)
            if elem:
                if elem.get('datetime'):
                    return elem.get('datetime')
                return elem.get_text(strip=True)
        
        return None
    
    def _extract_source(self, soup: BeautifulSoup) -> Optional[str]:
        """提取来源"""
        if self.selector_config.article_source:
            elem = soup.select_one(self.selector_config.article_source)
            if elem:
                return elem.get_text(strip=True)
        return None
    
    def _extract_tags(self, soup: BeautifulSoup) -> Optional[List[str]]:
        """提取标签"""
        if self.selector_config.article_tags:
            tags = []
            for elem in soup.select(self.selector_config.article_tags):
                tag = elem.get_text(strip=True)
                if tag:
                    tags.append(tag)
            return tags if tags else None
        return None
    
    def _extract_contents(self, soup: BeautifulSoup) -> List[ContentItem]:
        """提取文章内容"""
        contents = []
        
        # 提取正文
        if self.selector_config.article_content:
            content_elem = soup.select_one(self.selector_config.article_content)
            if content_elem:
                # 遍历内容元素，保持结构
                for elem in content_elem.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'img', 'video']):
                    if elem.name == 'img':
                        # 图片
                        src = elem.get('src') or elem.get('data-src')
                        if src:
                            # 处理相对路径
                            if src.startswith('//'):
                                src = 'https:' + src
                            elif src.startswith('/'):
                                src = self.base_url + src
                            
                            contents.append(ContentItem(
                                type=ContentType.IMAGE,
                                content=src,
                                caption=elem.get('alt', '')
                            ))
                    
                    elif elem.name == 'video':
                        # 视频
                        src = elem.get('src') or elem.find('source', src=True)
                        if src:
                            if isinstance(src, str):
                                video_url = src
                            else:
                                video_url = src.get('src')
                            
                            # 处理相对路径
                            if video_url.startswith('//'):
                                video_url = 'https:' + video_url
                            elif video_url.startswith('/'):
                                video_url = self.base_url + video_url
                            
                            contents.append(ContentItem(
                                type=ContentType.VIDEO,
                                content=video_url
                            ))
                    
                    else:
                        # 文本段落
                        text = elem.get_text(strip=True)
                        if text:
                            contents.append(ContentItem(
                                type=ContentType.TEXT,
                                content=text
                            ))
        
        return contents
    
    def get_article_id(self) -> str:
        """生成文章ID"""
        # 使用URL的hash作为ID
        url_hash = hashlib.md5(self.new_url.encode()).hexdigest()
        return f"{self.name}_{url_hash[:12]}"


class SimpleNewsCrawler(EnhancedNewsCrawler):
    """
    简化版爬虫，只需配置选择器即可使用
    用于快速创建新的网站爬虫
    """
    
    def __init__(
        self,
        url: str,
        name: str,
        base_url: str,
        selector_config: SelectorConfig,
        anti_crawler_config: Optional[AntiCrawlerConfig] = None,
        **kwargs
    ):
        self.name = name
        self.base_url = base_url
        self.selector_config = selector_config
        self.anti_crawler_config = anti_crawler_config or AntiCrawlerConfig()
        
        super().__init__(new_url=url, **kwargs)
