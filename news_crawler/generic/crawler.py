"""
通用新闻网站爬虫基类
"""

import re
import hashlib
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional, Dict, Any
from urllib.parse import urljoin, urlparse

from parsel import Selector
from curl_cffi import requests
from tenacity import retry, stop_after_attempt, wait_fixed

from ..core.models import NewsItem, NewsMetaInfo, ContentItem, ContentType


class GenericNewsCrawler(ABC):
    """通用新闻爬虫基类"""

    def __init__(
        self,
        source_id: str,
        source_name: str,
        base_url: str,
        list_url: str = None,
        headers: Dict[str, str] = None
    ):
        """
        Args:
            source_id: 新闻源ID
            source_name: 新闻源名称
            base_url: 基础URL
            list_url: 文章列表URL（如果与base_url不同）
            headers: 自定义请求头
        """
        self.source_id = source_id
        self.source_name = source_name
        self.base_url = base_url
        self.list_url = list_url or base_url
        self.headers = headers or self._default_headers()

    def _default_headers(self) -> Dict[str, str]:
        """默认请求头"""
        return {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def fetch_html(self, url: str) -> str:
        """
        获取网页HTML内容
        
        Args:
            url: 目标URL
            
        Returns:
            HTML内容字符串
        """
        response = requests.get(
            url,
            headers=self.headers,
            timeout=30,
            impersonate="chrome120"
        )
        response.raise_for_status()
        return response.text

    @abstractmethod
    def get_article_list_selector(self) -> str:
        """
        获取文章列表的CSS/XPath选择器
        
        Returns:
            选择器字符串
        """
        pass

    @abstractmethod
    def parse_article_item(self, element: Selector) -> Optional[Dict[str, str]]:
        """
        解析单个文章元素
        
        Args:
            element: Selector元素
            
        Returns:
            包含title和url的字典，如果解析失败返回None
        """
        pass

    @abstractmethod
    def parse_article_content(self, html: str, url: str) -> NewsItem:
        """
        解析文章详情页内容
        
        Args:
            html: HTML内容
            url: 文章URL
            
        Returns:
            NewsItem对象
        """
        pass

    def get_article_list(self, limit: int = 20) -> List[Dict[str, str]]:
        """
        获取文章列表
        
        Args:
            limit: 最多获取的文章数
            
        Returns:
            文章列表，每个元素包含title和url
        """
        try:
            html = self.fetch_html(self.list_url)
            selector = Selector(html)
            
            # 使用子类提供的选择器
            list_selector = self.get_article_list_selector()
            elements = selector.css(list_selector) if '::' in list_selector or '[' in list_selector \
                else selector.xpath(list_selector)
            
            articles = []
            for element in elements[:limit]:
                article_info = self.parse_article_item(element)
                if article_info and article_info.get('url'):
                    # 确保URL是完整的
                    article_info['url'] = urljoin(self.base_url, article_info['url'])
                    articles.append(article_info)
            
            return articles
        except Exception as e:
            print(f"获取文章列表失败: {e}")
            return []

    def crawl_article(self, url: str) -> Optional[NewsItem]:
        """
        爬取单篇文章
        
        Args:
            url: 文章URL
            
        Returns:
            NewsItem对象或None
        """
        try:
            html = self.fetch_html(url)
            return self.parse_article_content(html, url)
        except Exception as e:
            print(f"爬取文章失败 {url}: {e}")
            return None

    def generate_article_id(self, url: str, title: str = "") -> str:
        """
        生成文章唯一ID
        
        Args:
            url: 文章URL
            title: 文章标题
            
        Returns:
            MD5哈希ID
        """
        content = f"{url}_{title}"
        return hashlib.md5(content.encode()).hexdigest()

    def extract_text_from_element(self, element: Selector) -> str:
        """
        从元素中提取纯文本
        
        Args:
            element: Selector元素
            
        Returns:
            纯文本字符串
        """
        return ' '.join(element.xpath('.//text()').getall()).strip()

    def clean_text(self, text: str) -> str:
        """
        清理文本内容
        
        Args:
            text: 原始文本
            
        Returns:
            清理后的文本
        """
        # 去除多余空白
        text = re.sub(r'\s+', ' ', text)
        # 去除首尾空白
        text = text.strip()
        return text

    def parse_time(self, time_str: str) -> Optional[str]:
        """
        解析时间字符串
        
        Args:
            time_str: 时间字符串
            
        Returns:
            ISO格式时间字符串或None
        """
        if not time_str:
            return None
        
        try:
            # 尝试多种日期格式
            formats = [
                '%Y-%m-%d %H:%M:%S',
                '%Y-%m-%d %H:%M',
                '%Y-%m-%d',
                '%Y/%m/%d %H:%M:%S',
                '%Y/%m/%d %H:%M',
                '%Y/%m/%d',
                '%Y年%m月%d日 %H:%M:%S',
                '%Y年%m月%d日 %H:%M',
                '%Y年%m月%d日',
            ]
            
            for fmt in formats:
                try:
                    dt = datetime.strptime(time_str.strip(), fmt)
                    return dt.isoformat()
                except ValueError:
                    continue
            
            # 如果都失败了，尝试提取数字
            numbers = re.findall(r'\d+', time_str)
            if len(numbers) >= 3:
                year = int(numbers[0])
                month = int(numbers[1])
                day = int(numbers[2])
                hour = int(numbers[3]) if len(numbers) > 3 else 0
                minute = int(numbers[4]) if len(numbers) > 4 else 0
                second = int(numbers[5]) if len(numbers) > 5 else 0
                dt = datetime(year, month, day, hour, minute, second)
                return dt.isoformat()
            
        except Exception as e:
            print(f"解析时间失败: {time_str}, 错误: {e}")
        
        return None

    def run(self, limit: int = 20) -> List[NewsItem]:
        """
        执行爬取任务
        
        Args:
            limit: 最多爬取的文章数
            
        Returns:
            NewsItem列表
        """
        print(f"开始爬取 {self.source_name} ({self.source_id})...")
        
        # 获取文章列表
        article_list = self.get_article_list(limit)
        print(f"获取到 {len(article_list)} 篇文章")
        
        # 爬取文章详情
        news_items = []
        for i, article_info in enumerate(article_list, 1):
            print(f"正在爬取第 {i}/{len(article_list)} 篇: {article_info.get('title', 'Unknown')}")
            news_item = self.crawl_article(article_info['url'])
            if news_item:
                news_items.append(news_item)
        
        print(f"爬取完成，成功 {len(news_items)} 篇")
        return news_items


class SimpleListCrawler(GenericNewsCrawler):
    """
    简单列表式新闻爬虫
    适用于标准的新闻列表页 + 详情页结构
    """

    def __init__(
        self,
        source_id: str,
        source_name: str,
        base_url: str,
        list_url: str = None,
        list_selector: str = None,
        title_selector: str = None,
        link_selector: str = None,
        article_title_selector: str = None,
        article_content_selector: str = None,
        article_time_selector: str = None,
        article_author_selector: str = None,
        headers: Dict[str, str] = None
    ):
        """
        Args:
            source_id: 新闻源ID
            source_name: 新闻源名称
            base_url: 基础URL
            list_url: 文章列表URL
            list_selector: 文章列表项选择器
            title_selector: 标题选择器（相对于列表项）
            link_selector: 链接选择器（相对于列表项）
            article_title_selector: 文章页标题选择器
            article_content_selector: 文章页内容选择器
            article_time_selector: 文章页时间选择器
            article_author_selector: 文章页作者选择器
            headers: 自定义请求头
        """
        super().__init__(source_id, source_name, base_url, list_url, headers)
        self.list_selector = list_selector
        self.title_selector = title_selector
        self.link_selector = link_selector
        self.article_title_selector = article_title_selector
        self.article_content_selector = article_content_selector
        self.article_time_selector = article_time_selector
        self.article_author_selector = article_author_selector

    def get_article_list_selector(self) -> str:
        return self.list_selector

    def parse_article_item(self, element: Selector) -> Optional[Dict[str, str]]:
        try:
            title = element.css(self.title_selector).get() if '::' in self.title_selector \
                else element.xpath(self.title_selector).get()
            link = element.css(self.link_selector).get() if '::' in self.link_selector \
                else element.xpath(self.link_selector).get()
            
            if title and link:
                return {
                    'title': self.clean_text(title),
                    'url': link
                }
        except Exception as e:
            print(f"解析文章项失败: {e}")
        return None

    def parse_article_content(self, html: str, url: str) -> NewsItem:
        selector = Selector(html)
        
        # 提取标题
        title = selector.css(self.article_title_selector).get() \
            if '::' in self.article_title_selector \
            else selector.xpath(self.article_title_selector).get()
        title = self.clean_text(title) if title else "无标题"
        
        # 提取内容
        content_elements = selector.css(self.article_content_selector) \
            if '::' in self.article_content_selector \
            else selector.xpath(self.article_content_selector)
        
        contents = []
        texts = []
        images = []
        
        for element in content_elements:
            # 提取文本
            text = self.extract_text_from_element(element)
            if text:
                contents.append(ContentItem(
                    type=ContentType.TEXT,
                    content=text,
                    desc=""
                ))
                texts.append(text)
            
            # 提取图片
            imgs = element.xpath('.//img/@src').getall()
            for img in imgs:
                img_url = urljoin(self.base_url, img)
                contents.append(ContentItem(
                    type=ContentType.IMAGE,
                    content=img_url,
                    desc=""
                ))
                images.append(img_url)
        
        # 提取元信息
        author = ""
        publish_time = ""
        
        if self.article_author_selector:
            author = selector.css(self.article_author_selector).get() \
                if '::' in self.article_author_selector \
                else selector.xpath(self.article_author_selector).get()
            author = self.clean_text(author) if author else ""
        
        if self.article_time_selector:
            time_str = selector.css(self.article_time_selector).get() \
                if '::' in self.article_time_selector \
                else selector.xpath(self.article_time_selector).get()
            if time_str:
                publish_time = self.parse_time(time_str) or time_str
        
        meta_info = NewsMetaInfo(
            author_name=author,
            author_url="",
            publish_time=publish_time
        )
        
        return NewsItem(
            title=title,
            news_url=url,
            news_id=self.generate_article_id(url, title),
            meta_info=meta_info,
            contents=contents,
            texts=texts,
            images=images,
            videos=[]
        )
