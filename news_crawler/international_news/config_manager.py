"""
Configuration Manager for International News Crawler

Manages site configurations, crawling schedules, and update tracking.
"""

import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

from .configs.sites_config import (
    NEWS_SITES_CONFIG,
    REGION_GROUPS,
    get_all_countries,
    get_sites_by_country,
    get_sites_by_region,
    get_all_sites,
)


class ConfigManager:
    """
    Manages configurations and tracking for international news crawling.
    
    Features:
    - Site configuration management
    - Crawl history tracking
    - Update detection
    - Schedule management
    """
    
    def __init__(self, db_path: str = "data/international_news/crawl_history.db"):
        """Initialize the configuration manager"""
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()
    
    def _init_database(self):
        """Initialize SQLite database for tracking crawl history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Table for crawl history
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS crawl_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                site_name TEXT NOT NULL,
                site_url TEXT NOT NULL,
                country TEXT NOT NULL,
                article_url TEXT,
                article_title TEXT,
                crawl_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'success',
                error_message TEXT,
                article_count INTEGER DEFAULT 0
            )
        """)
        
        # Table for site configurations
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS site_configs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                site_name TEXT UNIQUE NOT NULL,
                site_url TEXT NOT NULL,
                country TEXT NOT NULL,
                enabled BOOLEAN DEFAULT 1,
                scan_interval INTEGER DEFAULT 3600,
                last_scan_time TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Table for latest articles (for update detection)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS latest_articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                site_name TEXT NOT NULL,
                article_url TEXT NOT NULL,
                article_title TEXT,
                publish_time TEXT,
                first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(site_name, article_url)
            )
        """)
        
        # Create indexes for performance
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_crawl_history_site 
            ON crawl_history(site_name, crawl_time)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_latest_articles_site 
            ON latest_articles(site_name, first_seen)
        """)
        
        conn.commit()
        conn.close()
    
    def load_site_configs(self):
        """Load all site configurations from the static config and sync to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for country, sites in NEWS_SITES_CONFIG.items():
            for site in sites:
                cursor.execute("""
                    INSERT OR IGNORE INTO site_configs 
                    (site_name, site_url, country, enabled, scan_interval)
                    VALUES (?, ?, ?, 1, 3600)
                """, (site['name'], site['url'], country))
        
        conn.commit()
        conn.close()
    
    def get_sites_by_filter(
        self,
        country: Optional[str] = None,
        region: Optional[str] = None,
        enabled_only: bool = True
    ) -> List[Dict]:
        """
        Get sites by filter criteria.
        
        Args:
            country: Filter by country name
            region: Filter by region name
            enabled_only: Only return enabled sites
        
        Returns:
            List of site configuration dictionaries
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = "SELECT * FROM site_configs WHERE 1=1"
        params = []
        
        if country:
            query += " AND country = ?"
            params.append(country)
        
        if region:
            # Get countries in the region
            countries = REGION_GROUPS.get(region, [])
            if countries:
                placeholders = ','.join('?' * len(countries))
                query += f" AND country IN ({placeholders})"
                params.extend(countries)
        
        if enabled_only:
            query += " AND enabled = 1"
        
        query += " ORDER BY country, site_name"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_sites_to_scan(self) -> List[Dict]:
        """
        Get sites that need to be scanned based on their scan interval.
        
        Returns:
            List of sites that should be scanned now
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get sites where last_scan_time is NULL or older than scan_interval
        query = """
            SELECT * FROM site_configs 
            WHERE enabled = 1 
            AND (
                last_scan_time IS NULL 
                OR datetime(last_scan_time, '+' || scan_interval || ' seconds') <= datetime('now')
            )
            ORDER BY last_scan_time ASC NULLS FIRST
        """
        
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def update_site_config(
        self,
        site_name: str,
        enabled: Optional[bool] = None,
        scan_interval: Optional[int] = None
    ):
        """
        Update site configuration.
        
        Args:
            site_name: Name of the site to update
            enabled: Whether the site is enabled for crawling
            scan_interval: Scan interval in seconds
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        updates = []
        params = []
        
        if enabled is not None:
            updates.append("enabled = ?")
            params.append(1 if enabled else 0)
        
        if scan_interval is not None:
            updates.append("scan_interval = ?")
            params.append(scan_interval)
        
        if updates:
            updates.append("updated_at = CURRENT_TIMESTAMP")
            query = f"UPDATE site_configs SET {', '.join(updates)} WHERE site_name = ?"
            params.append(site_name)
            cursor.execute(query, params)
            conn.commit()
        
        conn.close()
    
    def update_last_scan_time(self, site_name: str):
        """Update the last scan time for a site"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE site_configs 
            SET last_scan_time = CURRENT_TIMESTAMP 
            WHERE site_name = ?
        """, (site_name,))
        
        conn.commit()
        conn.close()
    
    def record_crawl(
        self,
        site_name: str,
        site_url: str,
        country: str,
        article_url: Optional[str] = None,
        article_title: Optional[str] = None,
        status: str = "success",
        error_message: Optional[str] = None,
        article_count: int = 0
    ):
        """
        Record a crawl attempt in the history.
        
        Args:
            site_name: Name of the site
            site_url: URL of the site
            country: Country of the site
            article_url: URL of the article (if crawling single article)
            article_title: Title of the article
            status: Status of the crawl ('success', 'failed', 'no_update')
            error_message: Error message if failed
            article_count: Number of articles crawled
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO crawl_history 
            (site_name, site_url, country, article_url, article_title, status, error_message, article_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (site_name, site_url, country, article_url, article_title, status, error_message, article_count))
        
        conn.commit()
        conn.close()
    
    def check_article_is_new(self, site_name: str, article_url: str) -> bool:
        """
        Check if an article is new (not seen before).
        
        Args:
            site_name: Name of the site
            article_url: URL of the article
        
        Returns:
            True if the article is new, False otherwise
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT COUNT(*) FROM latest_articles 
            WHERE site_name = ? AND article_url = ?
        """, (site_name, article_url))
        
        count = cursor.fetchone()[0]
        conn.close()
        
        return count == 0
    
    def add_latest_article(
        self,
        site_name: str,
        article_url: str,
        article_title: Optional[str] = None,
        publish_time: Optional[str] = None
    ):
        """
        Add an article to the latest articles tracking.
        
        Args:
            site_name: Name of the site
            article_url: URL of the article
            article_title: Title of the article
            publish_time: Publish time of the article
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO latest_articles 
            (site_name, article_url, article_title, publish_time)
            VALUES (?, ?, ?, ?)
        """, (site_name, article_url, article_title, publish_time))
        
        conn.commit()
        conn.close()
    
    def get_crawl_history(
        self,
        site_name: Optional[str] = None,
        country: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict]:
        """
        Get crawl history.
        
        Args:
            site_name: Filter by site name
            country: Filter by country
            limit: Maximum number of records to return
        
        Returns:
            List of crawl history records
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = "SELECT * FROM crawl_history WHERE 1=1"
        params = []
        
        if site_name:
            query += " AND site_name = ?"
            params.append(site_name)
        
        if country:
            query += " AND country = ?"
            params.append(country)
        
        query += " ORDER BY crawl_time DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_crawl_statistics(self, days: int = 7) -> Dict:
        """
        Get crawl statistics for the last N days.
        
        Args:
            days: Number of days to look back
        
        Returns:
            Dictionary with statistics
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cutoff_date = datetime.now() - timedelta(days=days)
        cutoff_str = cutoff_date.strftime("%Y-%m-%d %H:%M:%S")
        
        # Total crawls
        cursor.execute("""
            SELECT COUNT(*) FROM crawl_history 
            WHERE crawl_time >= ?
        """, (cutoff_str,))
        total_crawls = cursor.fetchone()[0]
        
        # Successful crawls
        cursor.execute("""
            SELECT COUNT(*) FROM crawl_history 
            WHERE crawl_time >= ? AND status = 'success'
        """, (cutoff_str,))
        successful_crawls = cursor.fetchone()[0]
        
        # Failed crawls
        cursor.execute("""
            SELECT COUNT(*) FROM crawl_history 
            WHERE crawl_time >= ? AND status = 'failed'
        """, (cutoff_str,))
        failed_crawls = cursor.fetchone()[0]
        
        # Total articles crawled
        cursor.execute("""
            SELECT SUM(article_count) FROM crawl_history 
            WHERE crawl_time >= ? AND status = 'success'
        """, (cutoff_str,))
        total_articles = cursor.fetchone()[0] or 0
        
        # Crawls by country
        cursor.execute("""
            SELECT country, COUNT(*) as count 
            FROM crawl_history 
            WHERE crawl_time >= ?
            GROUP BY country 
            ORDER BY count DESC
        """, (cutoff_str,))
        by_country = {row[0]: row[1] for row in cursor.fetchall()}
        
        conn.close()
        
        return {
            'days': days,
            'total_crawls': total_crawls,
            'successful_crawls': successful_crawls,
            'failed_crawls': failed_crawls,
            'total_articles': total_articles,
            'success_rate': f"{(successful_crawls / total_crawls * 100) if total_crawls > 0 else 0:.1f}%",
            'by_country': by_country,
        }
    
    def cleanup_old_articles(self, days: int = 30):
        """
        Clean up old articles from the latest_articles table.
        
        Args:
            days: Keep articles from the last N days
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cutoff_date = datetime.now() - timedelta(days=days)
        cutoff_str = cutoff_date.strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute("""
            DELETE FROM latest_articles 
            WHERE first_seen < ?
        """, (cutoff_str,))
        
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        return deleted_count


# Example usage
if __name__ == "__main__":
    # Initialize config manager
    manager = ConfigManager()
    
    # Load site configs
    print("Loading site configurations...")
    manager.load_site_configs()
    
    # Get sites by country
    print("\nSites in 美国:")
    us_sites = manager.get_sites_by_filter(country="美国")
    for site in us_sites[:5]:
        print(f"  - {site['site_name']}: {site['site_url']}")
    
    # Get sites to scan
    print("\nSites to scan:")
    to_scan = manager.get_sites_to_scan()
    print(f"  Total: {len(to_scan)} sites")
    
    # Get statistics
    print("\nCrawl statistics (last 7 days):")
    stats = manager.get_crawl_statistics(days=7)
    print(f"  Total crawls: {stats['total_crawls']}")
    print(f"  Successful: {stats['successful_crawls']}")
    print(f"  Failed: {stats['failed_crawls']}")
    print(f"  Success rate: {stats['success_rate']}")
    print(f"  Total articles: {stats['total_articles']}")
