"""
News Scheduler for International News Crawler

Manages scheduled crawling tasks with configurable intervals and automatic update detection.
"""

import asyncio
import logging
import time
from datetime import datetime
from typing import Optional, Dict, List, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed

from .base_crawler import InternationalNewsCrawler
from .config_manager import ConfigManager


class NewsScheduler:
    """
    Scheduler for automatic news crawling.
    
    Features:
    - Periodic scanning based on site-specific intervals
    - Update detection (only crawl new articles)
    - Parallel crawling support
    - Error handling and retry logic
    - Progress tracking and statistics
    """
    
    def __init__(
        self,
        config_manager: Optional[ConfigManager] = None,
        max_workers: int = 5,
        on_article_crawled: Optional[Callable] = None
    ):
        """
        Initialize the news scheduler.
        
        Args:
            config_manager: Configuration manager instance
            max_workers: Maximum number of concurrent crawling threads
            on_article_crawled: Callback function when an article is crawled
        """
        self.config_manager = config_manager or ConfigManager()
        self.max_workers = max_workers
        self.on_article_crawled = on_article_crawled
        self.is_running = False
        self.logger = self._setup_logger()
        
        # Statistics
        self.stats = {
            'total_sites_scanned': 0,
            'total_articles_found': 0,
            'total_articles_crawled': 0,
            'total_new_articles': 0,
            'total_errors': 0,
            'start_time': None,
            'last_scan_time': None,
        }
    
    def _setup_logger(self) -> logging.Logger:
        """Setup logger for the scheduler"""
        logger = logging.getLogger('NewsScheduler')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def scan_site(self, site_config: Dict, max_articles: int = 10) -> Dict:
        """
        Scan a single site for new articles.
        
        Args:
            site_config: Site configuration dictionary
            max_articles: Maximum number of articles to extract
        
        Returns:
            Dictionary with scan results
        """
        site_name = site_config['site_name']
        site_url = site_config['site_url']
        country = site_config['country']
        
        self.logger.info(f"Scanning {site_name} ({country}): {site_url}")
        
        result = {
            'site_name': site_name,
            'site_url': site_url,
            'country': country,
            'articles_found': 0,
            'new_articles': 0,
            'articles_crawled': 0,
            'status': 'success',
            'error_message': None,
            'articles': [],
        }
        
        try:
            # Create crawler for the site
            crawler = InternationalNewsCrawler(
                news_url=site_url,
                site_config={
                    'name': site_name,
                    'url': site_url,
                    'type': 'newspaper',  # Default type
                    'encoding': 'utf-8'
                }
            )
            
            # Extract latest articles
            articles = crawler.extract_latest_articles(max_articles=max_articles)
            result['articles_found'] = len(articles)
            
            # Check which articles are new
            new_articles = []
            for article in articles:
                if self.config_manager.check_article_is_new(site_name, article['url']):
                    new_articles.append(article)
                    # Mark as seen
                    self.config_manager.add_latest_article(
                        site_name=site_name,
                        article_url=article['url'],
                        article_title=article['title']
                    )
            
            result['new_articles'] = len(new_articles)
            result['articles'] = new_articles
            
            # Crawl new articles if any
            if new_articles:
                self.logger.info(f"Found {len(new_articles)} new articles on {site_name}")
                crawled_count = 0
                
                for article in new_articles:
                    try:
                        article_crawler = InternationalNewsCrawler(
                            news_url=article['url'],
                            site_config={
                                'name': site_name,
                                'url': site_url,
                                'type': 'newspaper',
                                'encoding': 'utf-8'
                            }
                        )
                        
                        # Crawl the article
                        news_item = article_crawler.run(persist=True)
                        crawled_count += 1
                        
                        # Record successful crawl
                        self.config_manager.record_crawl(
                            site_name=site_name,
                            site_url=site_url,
                            country=country,
                            article_url=article['url'],
                            article_title=article['title'],
                            status='success',
                            article_count=1
                        )
                        
                        # Call callback if provided
                        if self.on_article_crawled:
                            self.on_article_crawled(news_item, site_name, country)
                        
                        # Sleep briefly to avoid overwhelming the server
                        time.sleep(1)
                        
                    except Exception as e:
                        self.logger.error(f"Error crawling article {article['url']}: {str(e)}")
                        self.config_manager.record_crawl(
                            site_name=site_name,
                            site_url=site_url,
                            country=country,
                            article_url=article['url'],
                            article_title=article['title'],
                            status='failed',
                            error_message=str(e)
                        )
                
                result['articles_crawled'] = crawled_count
            else:
                # Record no update
                self.config_manager.record_crawl(
                    site_name=site_name,
                    site_url=site_url,
                    country=country,
                    status='no_update',
                    article_count=0
                )
            
            # Update last scan time
            self.config_manager.update_last_scan_time(site_name)
            
        except Exception as e:
            self.logger.error(f"Error scanning {site_name}: {str(e)}")
            result['status'] = 'failed'
            result['error_message'] = str(e)
            
            # Record failed crawl
            self.config_manager.record_crawl(
                site_name=site_name,
                site_url=site_url,
                country=country,
                status='failed',
                error_message=str(e)
            )
        
        return result
    
    def scan_all_sites(
        self,
        country: Optional[str] = None,
        region: Optional[str] = None,
        max_articles_per_site: int = 10,
        parallel: bool = True
    ) -> List[Dict]:
        """
        Scan all sites (or filtered sites) for new articles.
        
        Args:
            country: Filter by country
            region: Filter by region
            max_articles_per_site: Maximum articles to extract per site
            parallel: Use parallel processing
        
        Returns:
            List of scan results
        """
        # Get sites to scan
        sites = self.config_manager.get_sites_to_scan()
        
        # Apply filters
        if country:
            sites = [s for s in sites if s['country'] == country]
        
        if region:
            from .configs.sites_config import REGION_GROUPS
            countries = REGION_GROUPS.get(region, [])
            sites = [s for s in sites if s['country'] in countries]
        
        self.logger.info(f"Scanning {len(sites)} sites...")
        
        results = []
        
        if parallel and len(sites) > 1:
            # Parallel processing
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = {
                    executor.submit(self.scan_site, site, max_articles_per_site): site
                    for site in sites
                }
                
                for future in as_completed(futures):
                    try:
                        result = future.result()
                        results.append(result)
                        
                        # Update statistics
                        self.stats['total_sites_scanned'] += 1
                        self.stats['total_articles_found'] += result['articles_found']
                        self.stats['total_new_articles'] += result['new_articles']
                        self.stats['total_articles_crawled'] += result['articles_crawled']
                        if result['status'] == 'failed':
                            self.stats['total_errors'] += 1
                        
                    except Exception as e:
                        self.logger.error(f"Error in parallel scan: {str(e)}")
                        self.stats['total_errors'] += 1
        else:
            # Sequential processing
            for site in sites:
                result = self.scan_site(site, max_articles_per_site)
                results.append(result)
                
                # Update statistics
                self.stats['total_sites_scanned'] += 1
                self.stats['total_articles_found'] += result['articles_found']
                self.stats['total_new_articles'] += result['new_articles']
                self.stats['total_articles_crawled'] += result['articles_crawled']
                if result['status'] == 'failed':
                    self.stats['total_errors'] += 1
        
        self.stats['last_scan_time'] = datetime.now()
        
        return results
    
    def start_continuous_scanning(
        self,
        check_interval: int = 60,
        country: Optional[str] = None,
        region: Optional[str] = None,
        max_articles_per_site: int = 10
    ):
        """
        Start continuous scanning in a loop.
        
        Args:
            check_interval: How often to check for sites to scan (in seconds)
            country: Filter by country
            region: Filter by region
            max_articles_per_site: Maximum articles per site
        """
        self.is_running = True
        self.stats['start_time'] = datetime.now()
        
        self.logger.info("Starting continuous scanning...")
        self.logger.info(f"Check interval: {check_interval} seconds")
        
        try:
            while self.is_running:
                self.logger.info("Checking for sites to scan...")
                
                # Scan all sites that are due
                results = self.scan_all_sites(
                    country=country,
                    region=region,
                    max_articles_per_site=max_articles_per_site,
                    parallel=True
                )
                
                if results:
                    self.logger.info(
                        f"Scan complete. Sites: {len(results)}, "
                        f"New articles: {sum(r['new_articles'] for r in results)}, "
                        f"Crawled: {sum(r['articles_crawled'] for r in results)}"
                    )
                else:
                    self.logger.info("No sites to scan at this time.")
                
                # Sleep until next check
                self.logger.info(f"Sleeping for {check_interval} seconds...")
                time.sleep(check_interval)
                
        except KeyboardInterrupt:
            self.logger.info("Received interrupt signal, stopping...")
            self.stop()
        except Exception as e:
            self.logger.error(f"Error in continuous scanning: {str(e)}")
            self.stop()
    
    def stop(self):
        """Stop the scheduler"""
        self.is_running = False
        self.logger.info("Scheduler stopped")
        self._print_statistics()
    
    def _print_statistics(self):
        """Print crawling statistics"""
        if self.stats['start_time']:
            duration = datetime.now() - self.stats['start_time']
            self.logger.info("=" * 60)
            self.logger.info("Crawling Statistics")
            self.logger.info("=" * 60)
            self.logger.info(f"Duration: {duration}")
            self.logger.info(f"Sites scanned: {self.stats['total_sites_scanned']}")
            self.logger.info(f"Articles found: {self.stats['total_articles_found']}")
            self.logger.info(f"New articles: {self.stats['total_new_articles']}")
            self.logger.info(f"Articles crawled: {self.stats['total_articles_crawled']}")
            self.logger.info(f"Errors: {self.stats['total_errors']}")
            self.logger.info("=" * 60)
    
    def get_statistics(self) -> Dict:
        """Get current statistics"""
        stats = self.stats.copy()
        if stats['start_time']:
            stats['duration'] = str(datetime.now() - stats['start_time'])
        return stats


# Example usage
if __name__ == "__main__":
    # Initialize scheduler
    config_manager = ConfigManager()
    config_manager.load_site_configs()
    
    scheduler = NewsScheduler(
        config_manager=config_manager,
        max_workers=3
    )
    
    # Example 1: One-time scan of all sites
    print("\n" + "=" * 60)
    print("Example 1: Scanning all sites (one-time)")
    print("=" * 60)
    results = scheduler.scan_all_sites(max_articles_per_site=5, parallel=True)
    print(f"\nScanned {len(results)} sites")
    print(f"Found {sum(r['new_articles'] for r in results)} new articles")
    
    # Example 2: Scan sites from a specific country
    print("\n" + "=" * 60)
    print("Example 2: Scanning US sites only")
    print("=" * 60)
    results = scheduler.scan_all_sites(country="美国", max_articles_per_site=3)
    print(f"\nScanned {len(results)} US sites")
    
    # Example 3: Continuous scanning (uncomment to run)
    # print("\n" + "=" * 60)
    # print("Example 3: Starting continuous scanning")
    # print("Press Ctrl+C to stop")
    # print("=" * 60)
    # scheduler.start_continuous_scanning(
    #     check_interval=300,  # Check every 5 minutes
    #     max_articles_per_site=5
    # )
