"""
新闻爬取调度器
"""

import json
import time
import threading
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from pathlib import Path

from .database import DatabaseManager
from .models import CrawlTask, CrawlHistory, CrawlArticle
from ..generic.crawler import GenericNewsCrawler


class NewsScheduler:
    """新闻爬取调度器"""

    def __init__(
        self,
        db_path: str = "data/news_crawler.db",
        config_path: str = "news_crawler/config/news_sources.json"
    ):
        """
        Args:
            db_path: 数据库路径
            config_path: 新闻源配置文件路径
        """
        self.db = DatabaseManager(db_path)
        self.config_path = Path(config_path)
        self.running = False
        self.thread: Optional[threading.Thread] = None
        self.crawlers: Dict[str, GenericNewsCrawler] = {}

    def load_sources_config(self) -> List[Dict[str, Any]]:
        """加载新闻源配置"""
        if not self.config_path.exists():
            return []
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('sources', [])

    def init_tasks_from_config(self, interval_minutes: int = 60):
        """从配置文件初始化爬取任务"""
        sources = self.load_sources_config()
        print(f"从配置文件加载了 {len(sources)} 个新闻源")
        
        for source in sources:
            if not source.get('enabled', True):
                continue
            
            # 检查任务是否已存在
            existing_task = self.db.get_task_by_source_id(source['id'])
            if existing_task:
                continue
            
            # 创建新任务
            task = CrawlTask(
                source_id=source['id'],
                source_name=source['name'],
                url=source['url'],
                country=source['country'],
                enabled=source.get('enabled', True),
                interval_minutes=interval_minutes,
                last_crawl_time=None,
                next_crawl_time=datetime.now()
            )
            
            task_id = self.db.create_task(task)
            print(f"创建任务: {source['name']} (ID: {task_id})")

    def get_crawler_for_task(self, task: CrawlTask) -> Optional[GenericNewsCrawler]:
        """
        为任务获取对应的爬虫实例
        
        这里需要根据source_id选择合适的爬虫
        目前返回None，需要在子类或外部注册爬虫
        """
        return self.crawlers.get(task.source_id)

    def register_crawler(self, source_id: str, crawler: GenericNewsCrawler):
        """注册爬虫"""
        self.crawlers[source_id] = crawler

    def execute_task(self, task: CrawlTask) -> bool:
        """
        执行单个爬取任务
        
        Args:
            task: 爬取任务
            
        Returns:
            是否成功
        """
        start_time = time.time()
        
        try:
            print(f"\n{'='*60}")
            print(f"执行任务: {task.source_name} ({task.source_id})")
            print(f"URL: {task.url}")
            print(f"{'='*60}")
            
            # 获取爬虫
            crawler = self.get_crawler_for_task(task)
            if not crawler:
                print(f"未找到适配的爬虫: {task.source_id}")
                # 记录历史
                self.db.create_history(CrawlHistory(
                    task_id=task.id,
                    source_id=task.source_id,
                    url=task.url,
                    status="failed",
                    articles_count=0,
                    error_message="未找到适配的爬虫",
                    crawl_time=datetime.now(),
                    duration_seconds=time.time() - start_time
                ))
                return False
            
            # 执行爬取
            news_items = crawler.run(limit=20)
            
            # 保存文章
            new_articles = 0
            for news_item in news_items:
                article = CrawlArticle(
                    source_id=task.source_id,
                    article_id=news_item.news_id,
                    title=news_item.title,
                    url=news_item.news_url,
                    author=news_item.meta_info.author_name if news_item.meta_info else "",
                    publish_time=None,  # TODO: 解析publish_time
                    content="\n".join(news_item.texts),
                    summary="",
                    category="",
                    tags=[],
                    images=news_item.images,
                    videos=news_item.videos
                )
                
                article_id = self.db.create_article(article)
                if article_id:
                    new_articles += 1
            
            duration = time.time() - start_time
            
            print(f"\n任务完成:")
            print(f"  - 爬取文章: {len(news_items)} 篇")
            print(f"  - 新增文章: {new_articles} 篇")
            print(f"  - 耗时: {duration:.2f} 秒")
            
            # 更新任务状态
            task.last_crawl_time = datetime.now()
            task.next_crawl_time = datetime.now() + timedelta(minutes=task.interval_minutes)
            self.db.update_task(task)
            
            # 记录历史
            self.db.create_history(CrawlHistory(
                task_id=task.id,
                source_id=task.source_id,
                url=task.url,
                status="success",
                articles_count=new_articles,
                error_message=None,
                crawl_time=datetime.now(),
                duration_seconds=duration
            ))
            
            return True
            
        except Exception as e:
            duration = time.time() - start_time
            error_msg = f"爬取失败: {str(e)}"
            print(f"\n{error_msg}")
            
            # 更新任务状态
            task.last_crawl_time = datetime.now()
            task.next_crawl_time = datetime.now() + timedelta(minutes=task.interval_minutes)
            self.db.update_task(task)
            
            # 记录历史
            self.db.create_history(CrawlHistory(
                task_id=task.id,
                source_id=task.source_id,
                url=task.url,
                status="failed",
                articles_count=0,
                error_message=error_msg,
                crawl_time=datetime.now(),
                duration_seconds=duration
            ))
            
            return False

    def check_and_execute_tasks(self):
        """检查并执行到期的任务"""
        tasks = self.db.get_all_tasks(enabled_only=True)
        now = datetime.now()
        
        for task in tasks:
            # 检查是否需要执行
            if task.next_crawl_time is None or task.next_crawl_time <= now:
                self.execute_task(task)
                # 每个任务之间间隔一段时间，避免过于频繁
                time.sleep(5)

    def _scheduler_loop(self):
        """调度器主循环"""
        print("调度器启动...")
        
        while self.running:
            try:
                self.check_and_execute_tasks()
                # 每分钟检查一次
                time.sleep(60)
            except Exception as e:
                print(f"调度器错误: {e}")
                time.sleep(60)
        
        print("调度器停止")

    def start(self):
        """启动调度器"""
        if self.running:
            print("调度器已经在运行")
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._scheduler_loop, daemon=True)
        self.thread.start()
        print("调度器已启动（后台线程）")

    def stop(self):
        """停止调度器"""
        if not self.running:
            print("调度器未运行")
            return
        
        print("正在停止调度器...")
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        print("调度器已停止")

    def execute_task_by_source_id(self, source_id: str) -> bool:
        """手动执行指定任务"""
        task = self.db.get_task_by_source_id(source_id)
        if not task:
            print(f"未找到任务: {source_id}")
            return False
        
        return self.execute_task(task)

    def get_tasks_by_country(self, country: str) -> List[CrawlTask]:
        """获取指定国家的任务"""
        return self.db.get_tasks_by_country(country)

    def get_all_countries(self) -> List[str]:
        """获取所有国家列表"""
        tasks = self.db.get_all_tasks()
        countries = set(task.country for task in tasks)
        return sorted(countries)

    def get_task_statistics(self) -> Dict[str, Any]:
        """获取任务统计信息"""
        tasks = self.db.get_all_tasks()
        enabled_tasks = [t for t in tasks if t.enabled]
        recent_history = self.db.get_recent_history(limit=100)
        
        success_count = sum(1 for h in recent_history if h.status == "success")
        failed_count = sum(1 for h in recent_history if h.status == "failed")
        
        return {
            'total_tasks': len(tasks),
            'enabled_tasks': len(enabled_tasks),
            'disabled_tasks': len(tasks) - len(enabled_tasks),
            'recent_success': success_count,
            'recent_failed': failed_count,
            'countries': len(self.get_all_countries())
        }
