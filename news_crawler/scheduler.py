"""
新闻爬虫调度器
管理多个爬虫的定时任务
"""
import logging
import time
import threading
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class CrawlerTask:
    """爬虫任务"""
    id: int
    source_id: str
    source_name: str
    url: str
    country: str
    enabled: bool = True
    interval_minutes: int = 60
    last_crawl_time: Optional[datetime] = None
    next_crawl_time: Optional[datetime] = None
    created_at: datetime = None
    updated_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()


@dataclass
class CrawlerHistory:
    """爬取历史记录"""
    id: int
    task_id: int
    source_id: str
    url: str
    status: str
    articles_count: int
    error_message: Optional[str]
    crawl_time: datetime
    duration_seconds: float


@dataclass
class Article:
    """文章数据"""
    id: int
    source_id: str
    article_id: str
    title: str
    url: str
    author: Optional[str]
    publish_time: Optional[datetime]
    summary: Optional[str]
    category: Optional[str]
    created_at: datetime


class SimpleDB:
    """简化的内存数据库（用于测试）"""
    
    def __init__(self):
        self.tasks: Dict[int, CrawlerTask] = {}
        self.history: List[CrawlerHistory] = []
        self.articles: List[Article] = []
        self._next_task_id = 1
        self._next_history_id = 1
        self._next_article_id = 1
    
    def add_task(self, task: CrawlerTask) -> CrawlerTask:
        """添加任务"""
        task.id = self._next_task_id
        self._next_task_id += 1
        self.tasks[task.id] = task
        return task
    
    def get_task_by_source_id(self, source_id: str) -> Optional[CrawlerTask]:
        """根据source_id获取任务"""
        for task in self.tasks.values():
            if task.source_id == source_id:
                return task
        return None
    
    def get_all_tasks(self) -> List[CrawlerTask]:
        """获取所有任务"""
        return list(self.tasks.values())
    
    def update_task(self, task: CrawlerTask):
        """更新任务"""
        task.updated_at = datetime.now()
        if task.id in self.tasks:
            self.tasks[task.id] = task
    
    def add_history(self, history: CrawlerHistory) -> CrawlerHistory:
        """添加历史记录"""
        history.id = self._next_history_id
        self._next_history_id += 1
        self.history.append(history)
        return history
    
    def get_history_by_task_id(self, task_id: int, limit: int = 50) -> List[CrawlerHistory]:
        """获取任务的历史记录"""
        result = [h for h in self.history if h.task_id == task_id]
        result.sort(key=lambda x: x.crawl_time, reverse=True)
        return result[:limit]
    
    def get_recent_history(self, limit: int = 50) -> List[CrawlerHistory]:
        """获取最近的历史记录"""
        result = sorted(self.history, key=lambda x: x.crawl_time, reverse=True)
        return result[:limit]
    
    def add_article(self, article: Article) -> Article:
        """添加文章"""
        article.id = self._next_article_id
        self._next_article_id += 1
        self.articles.append(article)
        return article
    
    def get_articles_by_source(self, source_id: str, limit: int = 50) -> List[Article]:
        """获取指定源的文章"""
        result = [a for a in self.articles if a.source_id == source_id]
        result.sort(key=lambda x: x.created_at, reverse=True)
        return result[:limit]


class NewsScheduler:
    """新闻调度器"""
    
    def __init__(self, db_path: str = ":memory:"):
        self.crawlers: Dict[str, Any] = {}
        self.db = SimpleDB()
        self.running = False
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        logger.info(f"初始化调度器: {db_path}")
    
    def register_crawler(self, source_id: str, crawler_factory: Callable, 
                        source_name: str = "", url: str = "", country: str = ""):
        """注册爬虫"""
        self.crawlers[source_id] = {
            'factory': crawler_factory,
            'source_name': source_name,
            'url': url,
            'country': country
        }
        logger.info(f"注册爬虫: {source_id} - {source_name}")
    
    def start(self):
        """启动调度器"""
        if self.running:
            logger.warning("调度器已在运行")
            return
        
        self.running = True
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()
        logger.info("调度器已启动")
    
    def stop(self):
        """停止调度器"""
        if not self.running:
            logger.warning("调度器未运行")
            return
        
        self.running = False
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=5)
        logger.info("调度器已停止")
    
    def _run_loop(self):
        """调度循环"""
        while not self._stop_event.is_set():
            try:
                self._check_and_execute_tasks()
            except Exception as e:
                logger.error(f"调度循环错误: {e}")
            
            # 每分钟检查一次
            self._stop_event.wait(60)
    
    def _check_and_execute_tasks(self):
        """检查并执行到期的任务"""
        now = datetime.now()
        for task in self.db.get_all_tasks():
            if not task.enabled:
                continue
            
            if task.next_crawl_time and task.next_crawl_time <= now:
                self.execute_task(task)
    
    def execute_task(self, task: CrawlerTask):
        """执行爬取任务"""
        start_time = time.time()
        logger.info(f"开始执行任务: {task.source_id}")
        
        try:
            # 获取爬虫实例
            crawler_info = self.crawlers.get(task.source_id)
            if not crawler_info:
                raise Exception(f"爬虫未找到: {task.source_id}")
            
            crawler = crawler_info['factory']()
            
            # 执行爬取（这里简化处理）
            # result = crawler.run()
            
            # 记录成功
            duration = time.time() - start_time
            self.db.add_history(CrawlerHistory(
                id=0,
                task_id=task.id,
                source_id=task.source_id,
                url=task.url,
                status='success',
                articles_count=0,  # 实际应该从结果中获取
                error_message=None,
                crawl_time=datetime.now(),
                duration_seconds=duration
            ))
            
            # 更新任务状态
            task.last_crawl_time = datetime.now()
            task.next_crawl_time = datetime.now() + timedelta(minutes=task.interval_minutes)
            self.db.update_task(task)
            
            logger.info(f"任务执行成功: {task.source_id}, 耗时: {duration:.2f}秒")
            
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"任务执行失败: {task.source_id}, 错误: {e}")
            
            # 记录失败
            self.db.add_history(CrawlerHistory(
                id=0,
                task_id=task.id,
                source_id=task.source_id,
                url=task.url,
                status='failed',
                articles_count=0,
                error_message=str(e),
                crawl_time=datetime.now(),
                duration_seconds=duration
            ))
    
    def get_task_statistics(self) -> Dict[str, int]:
        """获取任务统计"""
        tasks = self.db.get_all_tasks()
        enabled_tasks = [t for t in tasks if t.enabled]
        
        # 获取最近的历史记录（24小时内）
        recent_history = self.db.get_recent_history(limit=1000)
        cutoff_time = datetime.now() - timedelta(hours=24)
        recent_history = [h for h in recent_history if h.crawl_time >= cutoff_time]
        
        success_count = sum(1 for h in recent_history if h.status == 'success')
        failed_count = sum(1 for h in recent_history if h.status == 'failed')
        
        # 统计国家数
        countries = set(t.country for t in tasks)
        
        return {
            'total_tasks': len(tasks),
            'enabled_tasks': len(enabled_tasks),
            'disabled_tasks': len(tasks) - len(enabled_tasks),
            'recent_success': success_count,
            'recent_failed': failed_count,
            'countries': len(countries)
        }
    
    def get_all_countries(self) -> List[str]:
        """获取所有国家列表"""
        countries = set()
        for task in self.db.get_all_tasks():
            if task.country:
                countries.add(task.country)
        return sorted(list(countries))
    
    def get_tasks_by_country(self, country: str) -> List[CrawlerTask]:
        """获取指定国家的任务"""
        return [t for t in self.db.get_all_tasks() if t.country == country]
    
    def init_tasks_from_config(self, interval_minutes: int = 60):
        """从配置初始化任务"""
        logger.info(f"从已注册爬虫初始化任务，默认间隔: {interval_minutes}分钟")
        
        for source_id, crawler_info in self.crawlers.items():
            # 检查任务是否已存在
            existing_task = self.db.get_task_by_source_id(source_id)
            if existing_task:
                logger.info(f"任务已存在，跳过: {source_id}")
                continue
            
            # 创建新任务
            task = CrawlerTask(
                id=0,
                source_id=source_id,
                source_name=crawler_info.get('source_name', source_id),
                url=crawler_info.get('url', ''),
                country=crawler_info.get('country', '未知'),
                enabled=True,
                interval_minutes=interval_minutes,
                next_crawl_time=datetime.now() + timedelta(minutes=interval_minutes)
            )
            
            self.db.add_task(task)
            logger.info(f"已创建任务: {source_id}")
        
        logger.info(f"任务初始化完成，共 {len(self.db.get_all_tasks())} 个任务")
