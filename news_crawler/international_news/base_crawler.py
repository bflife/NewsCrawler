"""
Generic International News Crawler

Supports automatic detection and extraction of news articles from various international news websites.
Uses intelligent content extraction algorithms to adapt to different website structures.
"""

import re
import hashlib
from datetime import datetime
from typing import Optional, List, Dict
from urllib.parse import urlparse

from ..core.base import BaseNewsCrawler
from ..core.models import NewsItem, NewsMetaInfo, ContentItem, ContentType, RequestHeaders
from ..core.fetchers import FetchRequest
from parsel import Selector


class InternationalNewsCrawler(BaseNewsCrawler):
    """
    Generic crawler for international news websites.
    
    Features:
    - Automatic content detection
    - Support for multiple languages
    - Adaptive parsing strategies
    - RSS/Atom feed support
    """
    
    def __init__(
        self,
        news_url: str,
        site_config: Optional[Dict] = None,
        save_path: str = "data/international_news/",
        headers: Optional[RequestHeaders] = None,
    ):
        """
        Initialize the international news crawler.
        
        Args:
            news_url: URL of the news article or website
            site_config: Optional configuration dict with site-specific settings
            save_path: Directory to save extracted content
            headers: Optional custom request headers
        """
        super().__init__(news_url, save_path, headers)
        self.site_config = site_config or {}
        self.encoding = self.site_config.get('encoding', 'utf-8')
        self.site_name = self.site_config.get('name', 'Unknown')
        self.site_type = self.site_config.get('type', 'unknown')
        
    def get_article_id(self) -> str:
        """Generate unique article ID from URL"""
        return hashlib.md5(self.new_url.encode()).hexdigest()[:16]
    
    def parse_content(self, html: str) -> NewsItem:
        """
        Parse HTML content and extract news article.
        
        Uses multiple strategies to find the main content:
        1. Common news article selectors
        2. Semantic HTML5 tags
        3. Content density analysis
        4. RSS/Atom feed parsing (if applicable)
        """
        selector = Selector(text=html)
        
        # Extract metadata
        meta_info = self._extract_metadata(selector, html)
        
        # Extract title
        title = self._extract_title(selector)
        
        # Extract main content
        contents = self._extract_main_content(selector)
        
        # Create news item
        return self.compose_news_item(
            title=title,
            meta_info=meta_info,
            contents=contents,
            extra={
                'site_name': self.site_name,
                'site_type': self.site_type,
                'extracted_at': datetime.now().isoformat(),
            }
        )
    
    def _extract_title(self, selector: Selector) -> str:
        """Extract article title using multiple strategies"""
        # Strategy 1: Common news title selectors
        title_selectors = [
            'h1.article-title::text',
            'h1.post-title::text',
            'h1.entry-title::text',
            'h1.news-title::text',
            'h1[class*="title"]::text',
            'article h1::text',
            'h1::text',
            '//meta[@property="og:title"]/@content',
            '//meta[@name="title"]/@content',
            'title::text',
        ]
        
        for sel in title_selectors:
            if sel.startswith('//'):
                title = selector.xpath(sel).get()
            else:
                title = selector.css(sel).get()
            
            if title and title.strip():
                return title.strip()
        
        return "Untitled Article"
    
    def _extract_metadata(self, selector: Selector, html: str) -> NewsMetaInfo:
        """Extract article metadata (author, publish time, etc.)"""
        # Extract author
        author_name = self._extract_author(selector)
        
        # Extract publish time
        publish_time = self._extract_publish_time(selector, html)
        
        return NewsMetaInfo(
            author_name=author_name,
            author_url="",
            publish_time=publish_time,
        )
    
    def _extract_author(self, selector: Selector) -> str:
        """Extract author name"""
        author_selectors = [
            '//meta[@name="author"]/@content',
            '//meta[@property="article:author"]/@content',
            '//span[@class="author"]//text()',
            '//div[@class="author"]//text()',
            '//a[@rel="author"]//text()',
            '.byline::text',
            '.author-name::text',
        ]
        
        for sel in author_selectors:
            if sel.startswith('//'):
                author = selector.xpath(sel).get()
            else:
                author = selector.css(sel).get()
            
            if author and author.strip():
                return author.strip()
        
        return "Unknown"
    
    def _extract_publish_time(self, selector: Selector, html: str) -> str:
        """Extract publish time"""
        time_selectors = [
            '//meta[@property="article:published_time"]/@content',
            '//meta[@name="publishdate"]/@content',
            '//meta[@name="publish_date"]/@content',
            '//time[@datetime]/@datetime',
            '//span[@class="publish-time"]//text()',
            '//span[@class="date"]//text()',
            '.publish-date::text',
            '.post-date::text',
        ]
        
        for sel in time_selectors:
            if sel.startswith('//'):
                pub_time = selector.xpath(sel).get()
            else:
                pub_time = selector.css(sel).get()
            
            if pub_time and pub_time.strip():
                # Try to parse and standardize the time format
                return self._standardize_time(pub_time.strip())
        
        # Try regex search in HTML for common date patterns
        date_patterns = [
            r'(\d{4}[-/年]\d{1,2}[-/月]\d{1,2}[日]?)',
            r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})',
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, html)
            if match:
                return self._standardize_time(match.group(1))
        
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def _standardize_time(self, time_str: str) -> str:
        """Standardize time format to YYYY-MM-DD HH:MM:SS"""
        # Remove common Chinese characters
        time_str = time_str.replace('年', '-').replace('月', '-').replace('日', '')
        
        # Try to parse ISO format
        if 'T' in time_str:
            try:
                dt = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
                return dt.strftime("%Y-%m-%d %H:%M:%S")
            except:
                pass
        
        # Try to extract date part
        match = re.search(r'(\d{4}[-/]\d{1,2}[-/]\d{1,2})', time_str)
        if match:
            date_part = match.group(1).replace('/', '-')
            # Try to extract time part
            time_match = re.search(r'(\d{1,2}:\d{2}(?::\d{2})?)', time_str)
            if time_match:
                return f"{date_part} {time_match.group(1)}"
            return f"{date_part} 00:00:00"
        
        return time_str
    
    def _extract_main_content(self, selector: Selector) -> List[ContentItem]:
        """Extract main article content using adaptive strategies"""
        contents = []
        
        # Strategy 1: Try common article content selectors
        content_selectors = [
            'article',
            '.article-content',
            '.post-content',
            '.entry-content',
            '.news-content',
            '.content-body',
            '[class*="content"]',
            'main',
        ]
        
        content_element = None
        for sel in content_selectors:
            element = selector.css(sel)
            if element:
                content_element = element[0]
                break
        
        # If no content element found, use body
        if not content_element:
            content_element = selector.css('body')
            if content_element:
                content_element = content_element[0]
        
        if content_element:
            # Extract paragraphs
            paragraphs = content_element.css('p')
            for p in paragraphs:
                text = ' '.join(p.css('::text').getall()).strip()
                if text and len(text) > 20:  # Filter out short texts
                    contents.append(ContentItem(
                        type=ContentType.TEXT,
                        content=text,
                        desc=""
                    ))
                
                # Extract images within paragraph
                imgs = p.css('img')
                for img in imgs:
                    img_url = img.css('::attr(src)').get() or img.css('::attr(data-src)').get()
                    if img_url:
                        img_url = self._normalize_url(img_url)
                        alt = img.css('::attr(alt)').get() or ""
                        contents.append(ContentItem(
                            type=ContentType.IMAGE,
                            content=img_url,
                            desc=alt
                        ))
            
            # Extract standalone images
            imgs = content_element.css('img')
            for img in imgs:
                img_url = img.css('::attr(src)').get() or img.css('::attr(data-src)').get()
                if img_url:
                    img_url = self._normalize_url(img_url)
                    alt = img.css('::attr(alt)').get() or ""
                    # Check if already added
                    if not any(c.content == img_url for c in contents):
                        contents.append(ContentItem(
                            type=ContentType.IMAGE,
                            content=img_url,
                            desc=alt
                        ))
            
            # Extract videos
            videos = content_element.css('video source::attr(src), iframe[src*="video"]::attr(src), iframe[src*="youtube"]::attr(src)')
            for video_url in videos.getall():
                if video_url:
                    video_url = self._normalize_url(video_url)
                    contents.append(ContentItem(
                        type=ContentType.VIDEO,
                        content=video_url,
                        desc=""
                    ))
        
        # Strategy 2: If no content found, try to extract all text
        if not contents:
            all_text = selector.css('body ::text').getall()
            combined_text = ' '.join(text.strip() for text in all_text if text.strip())
            if combined_text:
                # Split into paragraphs (by newlines or sentence breaks)
                paragraphs = re.split(r'\n{2,}|。\s*(?=[^\d])', combined_text)
                for para in paragraphs:
                    para = para.strip()
                    if para and len(para) > 30:
                        contents.append(ContentItem(
                            type=ContentType.TEXT,
                            content=para,
                            desc=""
                        ))
        
        return contents
    
    def _normalize_url(self, url: str) -> str:
        """Normalize relative URLs to absolute URLs"""
        if url.startswith('//'):
            return 'https:' + url
        elif url.startswith('/'):
            parsed = urlparse(self.new_url)
            return f"{parsed.scheme}://{parsed.netloc}{url}"
        elif not url.startswith('http'):
            parsed = urlparse(self.new_url)
            base_path = '/'.join(parsed.path.split('/')[:-1])
            return f"{parsed.scheme}://{parsed.netloc}{base_path}/{url}"
        return url
    
    def extract_latest_articles(self, max_articles: int = 10) -> List[Dict]:
        """
        Extract latest articles from the news website homepage or listing page.
        
        Returns:
            List of article dictionaries with title, url, and publish_time
        """
        html = self.fetch_content()
        selector = Selector(text=html)
        
        articles = []
        
        # Common article link selectors
        article_selectors = [
            'article a[href]',
            '.article-list a[href]',
            '.news-list a[href]',
            'ul.posts li a[href]',
            '.entry-title a[href]',
        ]
        
        links = []
        for sel in article_selectors:
            found_links = selector.css(sel)
            if found_links:
                links.extend(found_links)
                break
        
        # If no specific article links found, get all links
        if not links:
            links = selector.css('a[href]')
        
        seen_urls = set()
        for link in links:
            if len(articles) >= max_articles:
                break
            
            url = link.css('::attr(href)').get()
            title = ' '.join(link.css('::text').getall()).strip()
            
            if not url or not title:
                continue
            
            # Normalize URL
            url = self._normalize_url(url)
            
            # Filter out non-article links
            if not self._is_article_url(url):
                continue
            
            # Avoid duplicates
            if url in seen_urls:
                continue
            seen_urls.add(url)
            
            articles.append({
                'title': title,
                'url': url,
                'publish_time': '',  # Will be extracted when crawling the article
                'site_name': self.site_name,
            })
        
        return articles[:max_articles]
    
    def _is_article_url(self, url: str) -> bool:
        """Check if URL is likely an article link"""
        # Filter out common non-article patterns
        exclude_patterns = [
            r'/tag/',
            r'/category/',
            r'/author/',
            r'/search',
            r'/login',
            r'/register',
            r'/about',
            r'/contact',
            r'javascript:',
            r'#',
            r'\.(jpg|jpeg|png|gif|pdf|zip|css|js)$',
        ]
        
        for pattern in exclude_patterns:
            if re.search(pattern, url, re.IGNORECASE):
                return False
        
        # Should be from the same domain or subdomain
        article_domain = urlparse(url).netloc
        site_domain = urlparse(self.new_url).netloc
        
        if article_domain and site_domain:
            # Allow subdomains
            if not (article_domain == site_domain or article_domain.endswith('.' + site_domain)):
                return False
        
        return True


# Example usage
if __name__ == "__main__":
    # Test with a sample URL
    test_url = "https://www.bbc.com/news/world"
    crawler = InternationalNewsCrawler(
        news_url=test_url,
        site_config={
            'name': 'BBC',
            'type': 'broadcast',
            'encoding': 'utf-8'
        }
    )
    
    print("Extracting latest articles...")
    articles = crawler.extract_latest_articles(max_articles=5)
    for i, article in enumerate(articles, 1):
        print(f"{i}. {article['title']}")
        print(f"   URL: {article['url']}\n")
