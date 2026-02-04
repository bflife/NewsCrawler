"""
简化的爬虫基类，为批量爬虫提供默认实现
"""
import hashlib
from typing import Optional
from news_crawler.core.base import BaseNewsCrawler
from news_crawler.core.models import NewsItem, ContentItem, NewsMetaInfo
import logging

logger = logging.getLogger(__name__)


class SimpleNewsCrawler(BaseNewsCrawler):
    """
    简化的新闻爬虫基类
    提供parse_content和get_article_id的默认实现
    子类只需定义name和base_url即可
    """
    
    name = "simple_crawler"
    base_url = ""
    
    def __init__(self, new_url: str = "", save_path: str = 'data/', **kwargs):
        """
        初始化爬虫
        new_url: 要爬取的URL（可选，默认使用base_url）
        save_path: 保存路径
        """
        # 如果没有提供new_url，使用base_url
        if not new_url and hasattr(self, 'base_url'):
            new_url = self.base_url
        
        super().__init__(new_url=new_url, save_path=save_path, **kwargs)
    
    def parse_content(self, html: str) -> NewsItem:
        """
        解析HTML内容
        默认实现：返回包含原始HTML的NewsItem
        子类应覆盖此方法以提供特定的解析逻辑
        """
        # 使用更稳定的文章ID生成方式
        article_id = self.get_article_id()
        
        # 简单提取标题（如果有）
        title = "未知标题"
        try:
            if "<title>" in html:
                start = html.find("<title>") + 7
                end = html.find("</title>", start)
                if end > start:
                    title = html[start:end].strip()
        except Exception as e:
            logger.warning(f"提取标题失败: {e}")
        
        # 创建内容项
        content_item = ContentItem(
            type="html",
            data=html[:1000],  # 只保存前1000字符
            format="html"
        )
        
        # 创建元信息
        meta_info = NewsMetaInfo(
            source=self.name,
            url=self.new_url if hasattr(self, 'new_url') else self.base_url
        )
        
        # 返回新闻项
        return NewsItem(
            title=title,
            subtitle="",
            meta_info=meta_info,
            contents=[content_item],
            news_id=article_id
        )
    
    def get_article_id(self) -> str:
        """
        生成文章ID
        默认实现：使用时间戳和URL的MD5哈希
        """
        import time
        # 使用基础URL和时间戳生成ID
        url = self.new_url if hasattr(self, 'new_url') else self.base_url
        timestamp = str(int(time.time() * 1000))  # 毫秒级时间戳
        unique_str = f"{self.name}_{url}_{timestamp}"
        return hashlib.md5(unique_str.encode()).hexdigest()[:16]
    
    async def fetch_content(self, url: str) -> Optional[NewsMetaInfo]:
        """
        抓取内容（兼容旧接口）
        这是一个兼容方法，用于支持旧的爬虫接口
        """
        # 对于简化爬虫，直接返回None
        # 实际的抓取逻辑应该由run()方法调用
        logger.info(f"抓取内容: {url}")
        return None
